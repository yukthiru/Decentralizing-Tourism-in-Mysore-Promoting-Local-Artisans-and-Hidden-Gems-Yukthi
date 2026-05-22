from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class HiddenGem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    directions_url = db.Column(db.String(200), nullable=True)
    image_url = db.Column(db.String(300), nullable=True)
    is_featured = db.Column(db.Boolean, default=False)
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)
    best_time_to_visit = db.Column(db.String(100), nullable=True)
    entry_fee = db.Column(db.String(50), nullable=True)
    local_tip = db.Column(db.String(300), nullable=True)
    average_price = db.Column(db.String(50), nullable=True)
    closed_days = db.Column(db.String(100), nullable=True)

    def to_dict(self):
        return {
            'id': self.id, 'name': self.name, 'category': self.category,
            'description': self.description, 'location': self.location,
            'directions_url': self.directions_url, 'image_url': self.image_url,
            'is_featured': self.is_featured, 'lat': self.lat, 'lng': self.lng,
            'best_time_to_visit': self.best_time_to_visit, 'entry_fee': self.entry_fee,
            'local_tip': self.local_tip, 'average_price': self.average_price,
            'closed_days': self.closed_days
        }

class Artisan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    craft = db.Column(db.String(100), nullable=False)
    years_experience = db.Column(db.Integer, nullable=False)
    short_bio = db.Column(db.String(200), nullable=False)
    bio = db.Column(db.Text, nullable=False)
    contact_email = db.Column(db.String(100), nullable=True)
    whatsapp = db.Column(db.String(20), nullable=True)
    image_url = db.Column(db.String(300), nullable=True)
    average_price = db.Column(db.String(50), nullable=True)
    closed_days = db.Column(db.String(100), nullable=True)

    def to_dict(self):
        return {
            'id': self.id, 'name': self.name, 'craft': self.craft,
            'years_experience': self.years_experience, 'short_bio': self.short_bio,
            'bio': self.bio, 'contact_email': self.contact_email,
            'whatsapp': self.whatsapp, 'image_url': self.image_url,
            'average_price': self.average_price, 'closed_days': self.closed_days
        }

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

class ArtisanProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artisan_id = db.Column(db.Integer, db.ForeignKey('artisan.id'), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price_inr = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False) 
    is_available = db.Column(db.Boolean, default=True)
    image_url = db.Column(db.String(300), nullable=True)
    artisan = db.relationship('Artisan', backref=db.backref('products', lazy=True))

    def to_dict(self):
        return {
            'id': self.id, 'artisan_id': self.artisan_id,
            'artisan_name': self.artisan.name if self.artisan else None,
            'artisan_whatsapp': self.artisan.whatsapp if self.artisan else None,
            'product_name': self.product_name, 'description': self.description,
            'price_inr': self.price_inr, 'category': self.category,
            'is_available': self.is_available, 'image_url': self.image_url
        }

class LocalFood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    food_type = db.Column(db.String(50), nullable=False) 
    description = db.Column(db.Text, nullable=False)
    specialty_dish = db.Column(db.String(100), nullable=False)
    price_range = db.Column(db.String(10), nullable=False) 
    location = db.Column(db.String(100), nullable=False)
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)
    open_hours = db.Column(db.String(100), nullable=True)
    best_dish = db.Column(db.String(100), nullable=True)
    image_url = db.Column(db.String(300), nullable=True)
    is_vegetarian = db.Column(db.Boolean, default=False)
    local_secret = db.Column(db.String(300), nullable=True)
    closed_days = db.Column(db.String(100), nullable=True)

    def to_dict(self):
        return {
            'id': self.id, 'name': self.name, 'food_type': self.food_type,
            'description': self.description, 'specialty_dish': self.specialty_dish,
            'price_range': self.price_range, 'location': self.location,
            'lat': self.lat, 'lng': self.lng, 'open_hours': self.open_hours,
            'best_dish': self.best_dish, 'image_url': self.image_url,
            'is_vegetarian': self.is_vegetarian, 'local_secret': self.local_secret,
            'closed_days': self.closed_days
        }

class StayOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False) 
    price_per_night_inr = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    amenities = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(300), nullable=True)
    booking_link = db.Column(db.String(300), nullable=True)

    def to_dict(self):
        return {
            'id': self.id, 'name': self.name, 'type': self.type,
            'price_per_night_inr': self.price_per_night_inr, 'location': self.location,
            'amenities': self.amenities, 'description': self.description,
            'image_url': self.image_url, 'booking_link': self.booking_link
        }

class MarketStall(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stall_name = db.Column(db.String(100), nullable=False)
    artisan_id = db.Column(db.Integer, db.ForeignKey('artisan.id'), nullable=True)
    market_area = db.Column(db.String(100), nullable=False)
    stall_type = db.Column(db.String(50), nullable=False)
    products_sold = db.Column(db.String(200), nullable=False)
    demo_video_url = db.Column(db.String(300), nullable=True)
    story = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(300), nullable=True)
    open_days = db.Column(db.String(100), nullable=True)
    open_time = db.Column(db.String(100), nullable=True)
    artisan = db.relationship('Artisan', backref=db.backref('market_stalls', lazy=True))

    def to_dict(self):
        return {
            'id': self.id, 'stall_name': self.stall_name, 'artisan_id': self.artisan_id,
            'artisan_name': self.artisan.name if self.artisan else None,
            'market_area': self.market_area, 'stall_type': self.stall_type,
            'products_sold': self.products_sold, 'demo_video_url': self.demo_video_url,
            'story': self.story, 'image_url': self.image_url,
            'open_days': self.open_days, 'open_time': self.open_time
        }

class InquiryCart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('artisan_product.id'), nullable=True)
    stall_id = db.Column(db.Integer, db.ForeignKey('market_stall.id'), nullable=True)
    quantity = db.Column(db.Integer, default=1)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    product = db.relationship('ArtisanProduct')
    stall = db.relationship('MarketStall')

    def to_dict(self):
        return {
            'id': self.id, 'session_id': self.session_id, 'product_id': self.product_id,
            'stall_id': self.stall_id, 'quantity': self.quantity,
            'product_name': self.product.product_name if self.product else None,
            'stall_name': self.stall.stall_name if self.stall else None,
            'added_at': self.added_at.isoformat()
        }
