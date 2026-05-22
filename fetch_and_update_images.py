from app import app
from models import db, Artisan, StayOption
import requests
import re
import os
import unicodedata
from urllib.parse import quote_plus, urlparse

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, 'static', 'images')


def normalize_name_key(value):
    if not value:
        return ''
    value = unicodedata.normalize('NFKD', value)
    value = re.sub(r'[^A-Za-z0-9]+', '_', value).strip('_')
    value = re.sub(r'_+', '_', value)
    return value.lower()


def choose_candidate(urls, name):
    keywords = ['mysore','india','silk','weave','weavers','weaving','inlay','ganjifa','sandalwood','hotel','hostel','mansion','artisan','craft','weaver','gallery']
    lname = name.lower()
    for u in urls:
        lu = u.lower()
        if any(k in lu for k in keywords) or any(p in lu for p in lname.split() if len(p) > 3):
            return u
    return urls[0] if urls else None


def download_image(url, dest_path):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=20, stream=True)
        ct = r.headers.get('content-type', '')
        if r.status_code != 200 or not ct.startswith('image'):
            return False
        with open(dest_path, 'wb') as f:
            for chunk in r.iter_content(10240):
                if chunk:
                    f.write(chunk)
        return True
    except Exception:
        return False


MAPPINGS = [
    ('Artisan', 'KSIC Silk Weavers', 'KSIC Silk Weavers'),
    ('Artisan', 'Sri Krishna Murthy Inlay Arts', 'Sri Krishna Murthy Inlay Arts'),
    ('Artisan', 'Raghupathi Bhat', 'Raghupathi Bhat Ganjifa'),
    ('Artisan', 'Mysore Sandalwood Carvers Guild', 'Mysore Sandalwood Carvers Guild'),
    ('Artisan', 'B.S. Yogiraj Shilpi', 'B.S. Yogiraj Shilpi'),
    ('Artisan', 'Ramu Agarbathi Rollers', 'Ramu Agarbathi Rollers'),
    ('StayOption', 'Mansion 1907', 'Mansion 1907 Mysore'),
    ('StayOption', 'Green Hotel', 'Green Hotel Mysore'),
    ('StayOption', 'Roopa Elite', 'Roopa Elite Mysore'),
    ('StayOption', 'Lalitha Mahal Palace Hotel', 'Lalitha Mahal Palace Hotel Mysore'),
    ('StayOption', 'Sonder Hostel', 'Sonder Hostel Mysore'),
    ('StayOption', 'Southern Star', 'Southern Star Hotel Mysore')
]


def fetch_bing_images(query):
    url = f'https://www.bing.com/images/async?q={quote_plus(query)}&count=50&first=0&adlt=off&safeSearch=off'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    r = requests.get(url, headers=headers, timeout=20)
    text = r.text
    matches = re.findall(r'"murl"\s*:\s*"([^"]+)"', text)
    if matches:
        return matches
    img_matches = re.findall(r'<img[^>]+src="(https?://[^"]+\.(?:jpg|jpeg|png|webp))"', text, flags=re.IGNORECASE)
    return img_matches


def update_record(model_name, record_name, local_url):
    with app.app_context():
        if model_name == 'Artisan':
            rec = Artisan.query.filter(Artisan.name.ilike(f"%{record_name}%")).first()
        else:
            rec = StayOption.query.filter(StayOption.name.ilike(f"%{record_name}%")).first()
        if not rec:
            print('No record found for', record_name)
            return False
        rec.image_url = local_url
        rec.image_credit = 'Bing image (downloaded)'
        db.session.commit()
        print('Updated', model_name, record_name, '->', local_url)
        return True


def main():
    os.makedirs(IMAGE_DIR, exist_ok=True)
    summary = []
    for model_name, record_name, query in MAPPINGS:
        print('Processing', record_name)
        candidates = fetch_bing_images(query)
        if not candidates:
            print('  No candidates for', record_name)
            summary.append((record_name, None))
            continue
        pick = choose_candidate(candidates, record_name)
        if not pick:
            print('  No pick found for', record_name)
            summary.append((record_name, None))
            continue
        ext = os.path.splitext(urlparse(pick).path)[1]
        if not ext or len(ext) > 6:
            ext = '.jpg'
        filename = normalize_name_key(record_name) + ext
        dest = os.path.join(IMAGE_DIR, filename)
        ok = download_image(pick, dest)
        if ok:
            local_url = '/static/images/' + filename
            updated = update_record(model_name, record_name, local_url)
            summary.append((record_name, pick if updated else None))
        else:
            print('  download failed for', pick)
            summary.append((record_name, None))

    print('\nSummary:')
    for name, picked in summary:
        print('-', name, '->', picked)


if __name__ == '__main__':
    main()
