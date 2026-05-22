from app import app
from models import db, HiddenGem, Artisan, ArtisanProduct, LocalFood, StayOption, MarketStall, LocalGuide
import os
import re
import unicodedata

BASE = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE, 'static', 'images')

def normalize_name_key(value):
    if not value:
        return ''
    value = unicodedata.normalize('NFKD', value)
    value = re.sub(r'[^A-Za-z0-9]+', '_', value).strip('_')
    value = re.sub(r'_+', '_', value)
    return value.lower()


def safe_filename(name):
    return normalize_name_key(name) + '.jpg'


def find_local_image_url(name, default=None):
    if not name:
        return default
    fname = safe_filename(name)
    path = os.path.join(STATIC_DIR, fname)
    if os.path.exists(path):
        return '/static/images/' + fname

    key = normalize_name_key(name)
    candidates = []
    for f in os.listdir(STATIC_DIR):
        normalized = normalize_name_key(os.path.splitext(f)[0])
        if normalized.startswith(key) or key in normalized:
            candidates.append(f)
    if candidates:
        candidates.sort(key=lambda x: (len(x), x))
        return '/static/images/' + candidates[0]
    return default

with app.app_context():
    def update_model(model, name_attr='name', default=None):
        items = model.query.all()
        for it in items:
            name = getattr(it, name_attr, None)
            if not name:
                continue
            new_url = find_local_image_url(name, default)
            if new_url and getattr(it, 'image_url', None) != new_url:
                print(f'Updating {model.__name__} {name} -> {new_url}')
                it.image_url = new_url
        db.session.commit()

    update_model(HiddenGem, 'name')
    update_model(Artisan, 'name')
    update_model(ArtisanProduct, 'product_name')
    update_model(LocalFood, 'name')
    update_model(StayOption, 'name')
    update_model(MarketStall, 'stall_name')
    update_model(LocalGuide, 'name', default='/static/images/Local_Guide_Default.jpg')

    print('Database image URLs updated where local files exist')
