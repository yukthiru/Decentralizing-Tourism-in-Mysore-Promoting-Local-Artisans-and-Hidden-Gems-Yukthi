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
from flask import Flask, render_template, request, jsonify
from models import db, HiddenGem, Artisan, ContactMessage, ArtisanProduct, LocalFood, StayOption, MarketStall, InquiryCart

# --- APP INITIALIZATION ---
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'mysore_unseen.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

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

# --- WEB ROUTES ---

@app.route('/')
def index():
    featured_gems = HiddenGem.query.filter_by(is_featured=True).limit(3).all()
    featured_artisans = Artisan.query.limit(3).all()
    
    food_count = LocalFood.query.count()
    featured_food = LocalFood.query.offset(random.randint(0, max(0, food_count - 1))).first() if food_count > 0 else None
        
    return render_template('index.html', featured_gems=featured_gems, featured_artisans=featured_artisans, featured_food=featured_food)

@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route('/artisans')
def artisans():
    return render_template('artisans.html', artisans=Artisan.query.all())

@app.route('/artisans/<int:artisan_id>')
def artisan_detail(artisan_id):
    return render_template('artisan_detail.html', artisan=Artisan.query.get_or_404(artisan_id))

@app.route('/contact')
def contact():
    return render_template('contact.html')

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

# --- API ROUTES ---

@app.route('/api/gems')
def api_gems():
    category = request.args.get('category', 'All')
    gems = HiddenGem.query.filter_by(category=category).all() if category and category != 'All' else HiddenGem.query.all()
    return jsonify([gem.to_dict() for gem in gems])

@app.route('/api/artisans')
def api_artisans():
    return jsonify([a.to_dict() for a in Artisan.query.all()])

@app.route('/contact', methods=['POST'])
def submit_contact():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('email') or not data.get('message'):
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400
    db.session.add(ContactMessage(name=data['name'], email=data['email'], message=data['message']))
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/products')
def api_products():
    category = request.args.get('category', 'All')
    artisan_id = request.args.get('artisan_id')
    query = ArtisanProduct.query
    if category and category != 'All': query = query.filter_by(category=category)
    if artisan_id: query = query.filter_by(artisan_id=artisan_id)
    return jsonify([p.to_dict() for p in query.all()])

@app.route('/api/gems/map')
def api_gems_map():
    return jsonify([gem.to_dict() for gem in HiddenGem.query.all()])

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
    food_type = request.args.get('type', 'All')
    veg_only = request.args.get('veg', 'false') == 'true'
    query = LocalFood.query
    if food_type and food_type != 'All': query = query.filter_by(food_type=food_type)
    if veg_only: query = query.filter_by(is_vegetarian=True)
    return jsonify([f.to_dict() for f in query.all()])

@app.route('/api/plan-tour', methods=['POST'])
def api_plan_tour():
    data = request.get_json()
    stays = StayOption.query.all()
    stay_json = [s.to_dict() for s in stays]
    
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

@app.route('/api/market-stalls')
def api_market_stalls():
    area = request.args.get('area', 'All')
    stalls = MarketStall.query.filter_by(market_area=area).all() if area and area != 'All' else MarketStall.query.all()
    return jsonify([s.to_dict() for s in stalls])

@app.route('/api/cart/add', methods=['POST'])
def api_cart_add():
    data = request.get_json()
    if not data.get('session_id'): return jsonify({'success': False}), 400
    item = InquiryCart(session_id=data['session_id'], product_id=data.get('product_id'), stall_id=data.get('stall_id'), quantity=1)
    db.session.add(item)
    db.session.commit()
    return jsonify({'success': True, 'item': item.to_dict()})

@app.route('/api/cart')
def api_cart():
    session_id = request.args.get('session_id')
    return jsonify([i.to_dict() for i in InquiryCart.query.filter_by(session_id=session_id).all()] if session_id else [])

@app.route('/api/cart/<int:item_id>', methods=['DELETE'])
def api_cart_remove(item_id):
    item = InquiryCart.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
