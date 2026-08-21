# Setup instructions:
# pip install flask flask-sqlalchemy requests
# (Optional) set GEMINI_API_KEY=your_key for AI features
# python seed_data.py
# python app.py
# Open http://localhost:5000

import os
import requests
import random
import json
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, HiddenGem, Artisan, ContactMessage, ArtisanProduct, LocalFood, StayOption, MarketStall, InquiryCart, User
from image_data import PLACE_IMAGES, ARTISAN_IMAGES, FOOD_IMAGES, DEFAULT_IMAGE, get_image
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    supabase = None

# --- APP INITIALIZATION ---
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-change-me')
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'mysore_unseen.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

try:
    with app.app_context():
        db.create_all()
except Exception as e:
    print(f"DB init error (expected on Vercel): {e}")

# --- AI INTEGRATION ---
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')

def call_gemini(prompt, fallback_type='tour'):
    if not GEMINI_API_KEY:
        return generate_fallback_response(prompt, fallback_type)
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return generate_fallback_response(prompt, fallback_type)

def generate_fallback_response(prompt, fallback_type):
    if fallback_type == 'walking_tour':
        return '''{
            "stops": [
                {"order": 1, "name": "Mysore Palace Gates", "type": "Heritage", "duration_mins": 30, "description": "Start the walk here.", "walking_from_prev": "0 mins", "lat": 12.3051, "lng": 76.6551, "tip": "Best photos early morning."},
                {"order": 2, "name": "Devaraja Market", "type": "Heritage", "duration_mins": 45, "description": "Explore the vibrant local market.", "walking_from_prev": "15 mins", "lat": 12.3086, "lng": 76.6500, "tip": "Try the local sweets."}
            ],
            "total_distance_km": "2.5 km",
            "total_time_mins": "120 mins",
            "tour_narrative": "This is a fallback generated tour because the Gemini API key is missing. Enjoy exploring Mysore!"
        }'''
    elif fallback_type == 'tour_planner':
        import re
        days_match = re.search(r'- Days:\s*(\d+)', prompt)
        days = int(days_match.group(1)) if days_match else 1
        itinerary = []
        for d in range(1, days + 1):
            itinerary.append({
                "day": d,
                "morning": f"Visit Heritage Site {d}",
                "afternoon": "Lunch and Explore local markets",
                "evening": "Artisan workshop visit",
                "meals": "Local cuisine",
                "artisan_visit": "Wood Carving Studio" if d % 2 != 0 else "Silk Weaving",
                "estimated_spend": "1500"
            })
        return json.dumps({
            "itinerary": itinerary,
            "budget_breakdown": {"accommodation": 2000*days, "food": 1000*days, "transport": 500*days, "activities": 1000*days, "artisan_purchases": 2000, "total": 6500*days},
            "budget_status": "within",
            "tips": ["Book tickets early", "Carry cash for local markets", "This is a fallback generated tour because the Gemini API key is missing."]
        })
    return "{}"


def get_image_for_item(mapping, item, name_attr='name'):
    if isinstance(item, dict):
        item_name = item.get(name_attr)
        existing_url = item.get('image_url')
    else:
        item_name = getattr(item, name_attr, None)
        existing_url = getattr(item, 'image_url', None)
    mapped_url = get_image(mapping, item_name)
    if mapped_url != DEFAULT_IMAGE:
        return mapped_url
    if existing_url:
        if existing_url.startswith('https://upload.wikimedia.org'):
            return DEFAULT_IMAGE
        return existing_url
    return DEFAULT_IMAGE

# --- CONTEXT PROCESSOR ---
@app.context_processor
def inject_user():
    return {'current_user': session.get('user')}


# --- LOGIN REQUIRED DECORATOR ---
def login_required(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get('user'):
            return redirect(url_for('login'))
        return fn(*args, **kwargs)
    return wrapper


@app.before_request
def require_sign_in():
    """Keep the application features behind the sign-in page."""
    public_endpoints = {'login', 'signup', 'static'}
    if request.endpoint in public_endpoints or session.get('user'):
        return None

    if request.path.startswith('/api/'):
        return jsonify({'error': 'Sign in required'}), 401

    return redirect(url_for('login'))


# --- WEB ROUTES ---

@app.route('/')
def index():
    if not session.get('user'):
        return redirect(url_for('login'))

    try:
        featured_gems = HiddenGem.query.filter_by(is_featured=True).limit(3).all()
        featured_artisans = Artisan.query.limit(3).all()
        food_count = LocalFood.query.count()
        featured_food = LocalFood.query.offset(random.randint(0, max(0, food_count - 1))).first() if food_count > 0 else None
        for g in featured_gems:
            try:
                g.image_url = get_image(PLACE_IMAGES, g.name)
            except:
                g.image_url = DEFAULT_IMAGE
        for a in featured_artisans:
            try:
                a.image_url = get_image(ARTISAN_IMAGES, a.name)
            except:
                a.image_url = DEFAULT_IMAGE
    except Exception as e:
        print(f"Index DB error: {e}")
        featured_gems = []
        featured_artisans = []
        featured_food = None
    return render_template('index.html', featured_gems=featured_gems, featured_artisans=featured_artisans, featured_food=featured_food)

@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route('/artisans')
def artisans():
    try:
        artisans = Artisan.query.all()
        for a in artisans:
            try:
                a.image_url = get_image(ARTISAN_IMAGES, a.name)
            except:
                a.image_url = DEFAULT_IMAGE
    except Exception as e:
        print(f"Artisans DB error: {e}")
        artisans = []
    return render_template('artisans.html', artisans=artisans)

@app.route('/artisans/<int:artisan_id>')
def artisan_detail(artisan_id):
    try:
        artisan = Artisan.query.get_or_404(artisan_id)
        try:
            artisan.image_url = get_image(ARTISAN_IMAGES, artisan.name)
        except:
            artisan.image_url = DEFAULT_IMAGE
    except Exception as e:
        print(f"Artisan detail DB error: {e}")
        return redirect(url_for('artisans'))
    return render_template('artisan_detail.html', artisan=artisan)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    form = request.form
    email = form.get('email', '').strip().lower()
    password = form.get('password', '')

    if not email or not password:
        return render_template('login.html', error='Missing email or password')

    if supabase:
        try:
            res = supabase.auth.sign_in_with_password({'email': email, 'password': password})
            user_info = None
            if isinstance(res, dict):
                user_info = res.get('user')
            else:
                user_info = getattr(res, 'user', None)

            if user_info:
                email_val = user_info.get('email') if isinstance(user_info, dict) else getattr(user_info, 'email', email)
                session['user'] = {'email': email_val}
                return redirect(url_for('index'))
        except Exception as e:
            print(f"Supabase login error: {e}")

    # Local SQLite fallback (only works locally)
    try:
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session['user'] = {'email': user.email}
            return redirect(url_for('index'))
    except Exception as e:
        print(f"Local DB login error: {e}")

    return render_template('login.html', error='Invalid email or password')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    form = request.form
    email = form.get('email', '').strip().lower()
    password = form.get('password', '')
    confirm_password = form.get('confirm_password', '')

    if not email or not password or not confirm_password:
        return render_template('signup.html', error='All fields are required')
    if password != confirm_password:
        return render_template('signup.html', error='Passwords do not match')
    if len(password) < 6:
        return render_template('signup.html', error='Password must be at least 6 characters')

    if supabase:
        try:
            signup_res = supabase.auth.sign_up({'email': email, 'password': password})
            err = None
            if isinstance(signup_res, dict):
                err = signup_res.get('error') or signup_res.get('message')
            else:
                err = getattr(signup_res, 'error', None) or getattr(signup_res, 'message', None)

            if err:
                normalized = str(err).lower()
                if 'already' in normalized:
                    return render_template('signup.html', error='Email already registered')
                return render_template('signup.html', error=str(err))

            session['user'] = {'email': email}
            return redirect(url_for('index'))

        except Exception as e:
            return render_template('signup.html', error=f'Signup failed: {str(e)}')

    # Local SQLite fallback (only works locally)
    try:
        if User.query.filter_by(email=email).first():
            return render_template('signup.html', error='Email already registered')
        user = User(email=email, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        session['user'] = {'email': email}
        return redirect(url_for('index'))
    except Exception as e:
        return render_template('signup.html', error='Signup unavailable. Please try again later.')


@app.route('/logout')
def logout():
    session.pop('user', None)
    try:
        if supabase and hasattr(supabase.auth, 'sign_out'):
            supabase.auth.sign_out()
    except Exception:
        pass
    return redirect(url_for('index'))

@app.route('/marketplace')
def marketplace():
    return render_template('marketplace.html')

@app.route('/hidden-gems')
def hidden_gems():
    return render_template('hidden_gems.html')

@app.route('/walking-tour')
def walking_tour():
    return render_template('walking_tour.html')

@app.route('/food-discovery')
def food_discovery():
    return render_template('food_discovery.html')

@app.route('/tour-planner')
def tour_planner():
    return render_template('tour_planner.html')

@app.route('/virtual-market')
def virtual_market():
    return render_template('virtual_market.html')

@app.route('/tourist-guide')
def tourist_guide():
    return render_template('tourist_guide.html')

@app.route('/my-tours')
def my_tours_page():
    if not session.get('user'):
        return redirect(url_for('login'))
    return render_template('my_tours.html')


# --- API ROUTES ---

@app.route('/api/gems')
def api_gems():
    try:
        category = request.args.get('category', 'All')
        gems = HiddenGem.query.filter_by(category=category).all() if category and category != 'All' else HiddenGem.query.all()
        gem_dicts = [gem.to_dict() for gem in gems]
        for gem in gem_dicts:
            gem['image_url'] = get_image_for_item(PLACE_IMAGES, gem, 'name')
        return jsonify(gem_dicts)
    except Exception as e:
        print(f"Gems API error: {e}")
        return jsonify([])

@app.route('/api/artisans')
def api_artisans():
    try:
        artisan_dicts = [a.to_dict() for a in Artisan.query.all()]
        for artisan in artisan_dicts:
            artisan['image_url'] = get_image_for_item(ARTISAN_IMAGES, artisan, 'name')
        return jsonify(artisan_dicts)
    except Exception as e:
        print(f"Artisans API error: {e}")
        return jsonify([])

@app.route('/contact', methods=['POST'])
def submit_contact():
    data = request.get_json() or request.form
    if hasattr(data, 'to_dict'):
        data = data.to_dict()
    if not data or not data.get('name') or not data.get('email') or not data.get('message'):
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400

    if supabase:
        try:
            supabase.table('contact_messages').insert({
                'name': data['name'],
                'email': data['email'],
                'message': data['message']
            }).execute()
        except Exception as e:
            print(f"Supabase insert error: {e}")

    try:
        db.session.add(ContactMessage(name=data['name'], email=data['email'], message=data['message']))
        db.session.commit()
    except Exception as e:
        print(f"Local DB contact error (expected on Vercel): {e}")

    return jsonify({'success': True})

@app.route('/api/products')
def api_products():
    try:
        category = request.args.get('category', 'All')
        artisan_id = request.args.get('artisan_id')
        query = ArtisanProduct.query
        if category and category != 'All': query = query.filter_by(category=category)
        if artisan_id: query = query.filter_by(artisan_id=artisan_id)
        return jsonify([p.to_dict() for p in query.all()])
    except Exception as e:
        print(f"Products API error: {e}")
        return jsonify([])

@app.route('/api/gems/map')
def api_gems_map():
    try:
        gem_dicts = [gem.to_dict() for gem in HiddenGem.query.all()]
        for gem in gem_dicts:
            gem['image_url'] = get_image_for_item(PLACE_IMAGES, gem, 'name')
        return jsonify(gem_dicts)
    except Exception as e:
        print(f"Gems map API error: {e}")
        return jsonify([])

@app.route('/api/generate-tour', methods=['POST'])
def api_generate_tour():
    data = request.get_json()
    prompt = f"""
    Create a personalized walking tour for Mysore with the following parameters:
    - Duration: {data.get('duration_hours')} hours
    - Interests: {', '.join(data.get('interests', []))}
    - Start Location: {data.get('start_location')}
    - Pace: {data.get('pace')}
    Return EXACTLY a JSON string with no markdown formatting or backticks, matching this structure:
    {{"stops": [{{"order": 1, "name": "...", "type": "Heritage/Art/Food", "duration_mins": 30, "description": "...", "walking_from_prev": "5 mins", "lat": 12.3, "lng": 76.6, "tip": "..."}}], "total_distance_km": "3.5 km", "total_time_mins": "180 mins", "tour_narrative": "..."}}
    """
    ai_response = call_gemini(prompt, 'walking_tour')
    if ai_response.startswith('```json'): ai_response = ai_response[7:-3]
    elif ai_response.startswith('```'): ai_response = ai_response[3:-3]
    return ai_response, 200, {'Content-Type': 'application/json'}

@app.route('/api/food')
def api_food():
    try:
        food_type = request.args.get('type', 'All')
        veg_only = request.args.get('veg', 'false') == 'true'
        query = LocalFood.query
        if food_type and food_type != 'All': query = query.filter_by(food_type=food_type)
        if veg_only: query = query.filter_by(is_vegetarian=True)
        food_dicts = [f.to_dict() for f in query.all()]
        for food in food_dicts:
            food_name = f"{food.get('specialty_dish','')} {food.get('name','')}"
            food['image_url'] = get_image(FOOD_IMAGES, food_name)
        return jsonify(food_dicts)
    except Exception as e:
        print(f"Food API error: {e}")
        return jsonify([])

@app.route('/api/plan-tour', methods=['POST'])
def api_plan_tour():
    data = request.get_json()
    try:
        stays = StayOption.query.all()
        stay_json = [s.to_dict() for s in stays]
    except Exception as e:
        print(f"Stay options DB error: {e}")
        stay_json = []

    prompt = f"""
    Create a full trip itinerary for Mysore:
    - Budget: ₹{data.get('budget_inr')}
    - Days: {data.get('days')}
    - Travelers: {data.get('travelers')}
    - Interests: {', '.join(data.get('interests', []))}
    - Stay Preference: {data.get('accommodation_type')}
    Return EXACTLY a JSON string with no markdown formatting or backticks, matching this structure:
    {{"itinerary": [{{"day": 1, "morning": "...", "afternoon": "...", "evening": "...", "meals": "...", "artisan_visit": "...", "estimated_spend": "1500"}}], "budget_breakdown": {{"accommodation": 0, "food": 0, "transport": 0, "activities": 0, "artisan_purchases": 0, "total": 0}}, "budget_status": "within", "tips": ["tip1"]}}
    """
    ai_response = call_gemini(prompt, 'tour_planner')
    if ai_response.startswith('```json'): ai_response = ai_response[7:-3]
    elif ai_response.startswith('```'): ai_response = ai_response[3:-3]

    try:
        resp_dict = json.loads(ai_response)
        preferred_stays = [s for s in stay_json if s['type'] == data.get('accommodation_type')]
        resp_dict['stay_suggestions'] = preferred_stays[:3] if preferred_stays else stay_json[:3]
        return jsonify(resp_dict)
    except:
        return ai_response, 200, {'Content-Type': 'application/json'}

@app.route('/api/save-tour', methods=['POST'])
def save_tour():
    if not session.get('user'):
        return jsonify({'success': False, 'error': 'Login required'}), 401

    data = request.get_json()
    if not supabase:
        return jsonify({'success': False, 'error': 'Supabase not connected'}), 500

    try:
        supabase.table('saved_tours').insert({
            'user_email': session['user']['email'],
            'days': data.get('days'),
            'budget': data.get('budget_inr'),
            'interests': ', '.join(data.get('interests', [])),
            'itinerary': json.dumps(data.get('itinerary'))
        }).execute()
        return jsonify({'success': True})
    except Exception as e:
        print(f"Save tour error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/my-tours')
def my_tours_api():
    if not session.get('user'):
        return jsonify({'success': False, 'error': 'Login required'}), 401

    if not supabase:
        return jsonify({'success': False, 'error': 'Supabase not connected'}), 500

    try:
        response = supabase.table('saved_tours')\
            .select('*')\
            .eq('user_email', session['user']['email'])\
            .order('created_at', desc=True)\
            .execute()
        return jsonify({'success': True, 'tours': response.data})
    except Exception as e:
        print(f"Fetch saved tours error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/market-stalls')
def api_market_stalls():
    try:
        area = request.args.get('area', 'All')
        stalls = MarketStall.query.filter_by(market_area=area).all() if area and area != 'All' else MarketStall.query.all()
        stall_dicts = [s.to_dict() for s in stalls]
        for stall in stall_dicts:
            stall_name = f"{stall.get('stall_name','')} {stall.get('market_area','')}"
            stall['image_url'] = get_image(PLACE_IMAGES, stall_name)
        return jsonify(stall_dicts)
    except Exception as e:
        print(f"Market stalls API error: {e}")
        return jsonify([])

@app.route('/api/cart/add', methods=['POST'])
def api_cart_add():
    try:
        data = request.get_json()
        if not data.get('session_id'): return jsonify({'success': False}), 400
        item = InquiryCart(session_id=data['session_id'], product_id=data.get('product_id'), stall_id=data.get('stall_id'), quantity=1)
        db.session.add(item)
        db.session.commit()
        return jsonify({'success': True, 'item': item.to_dict()})
    except Exception as e:
        print(f"Cart add error: {e}")
        return jsonify({'success': False}), 500

@app.route('/api/cart')
def api_cart():
    try:
        session_id = request.args.get('session_id')
        return jsonify([i.to_dict() for i in InquiryCart.query.filter_by(session_id=session_id).all()] if session_id else [])
    except Exception as e:
        print(f"Cart fetch error: {e}")
        return jsonify([])

@app.route('/api/cart/<int:item_id>', methods=['DELETE'])
def api_cart_remove(item_id):
    try:
        item = InquiryCart.query.get(item_id)
        if item:
            db.session.delete(item)
            db.session.commit()
            return jsonify({'success': True})
        return jsonify({'success': False}), 404
    except Exception as e:
        print(f"Cart remove error: {e}")
        return jsonify({'success': False}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)