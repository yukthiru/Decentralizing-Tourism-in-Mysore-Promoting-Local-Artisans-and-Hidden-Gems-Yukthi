from app import app
from models import db, Artisan, StayOption
import requests, os, re, unicodedata
from urllib.parse import urlparse

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, 'static', 'images')
os.makedirs(IMAGE_DIR, exist_ok=True)

def normalize_name_key(value):
    if not value:
        return ''
    value = unicodedata.normalize('NFKD', value)
    value = re.sub(r'[^A-Za-z0-9]+', '_', value).strip('_')
    value = re.sub(r'_+', '_', value)
    return value.lower()

def download(url, dest):
    try:
        headers = {'User-Agent':'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=20, stream=True)
        if r.status_code != 200:
            return False
        ct = r.headers.get('content-type','')
        if not ct.startswith('image') and not dest.lower().endswith(('.jpg','.jpeg','.png','.webp')):
            return False
        with open(dest, 'wb') as f:
            for chunk in r.iter_content(8192):
                if chunk:
                    f.write(chunk)
        return True
    except Exception as e:
        print('Download error', e)
        return False

APPROVED = {
    ('Artisan','Sri Krishna Murthy Inlay Arts'):
        'https://thearchitectsdiary.com/wp-content/uploads/2020/02/Screenshot-2020-02-29-at-12.23.19-PM-1024x765.png',
    ('Artisan','Raghupathi Bhat'):
        'https://i.ytimg.com/vi/2TAIAE7WXKg/maxresdefault.jpg',
    ('Artisan','Mysore Sandalwood Carvers Guild'):
        'https://i.etsystatic.com/16624130/r/il/436af0/3139822690/il_1588xN.3139822690_q01q.jpg',
    ('StayOption','Sonder Hostel'):
        'https://i0.wp.com/landlopers.com/wp-content/uploads/2012/11/IMG_5691.jpg?fit=1024%2C678&ssl=1'
}

def update_record(model_name, name, local_url):
    with app.app_context():
        if model_name == 'Artisan':
            rec = Artisan.query.filter(Artisan.name.ilike(f"%{name}%")).first()
        else:
            rec = StayOption.query.filter(StayOption.name.ilike(f"%{name}%")).first()
        if not rec:
            print('No record found for', name)
            return False
        rec.image_url = local_url
        rec.image_credit = 'Selected image (downloaded)'
        db.session.commit()
        print('Updated', name, '->', local_url)
        return True

def main():
    summary = []
    for (model_name, name), url in APPROVED.items():
        print('Processing', name)
        parsed = urlparse(url)
        ext = os.path.splitext(parsed.path)[1]
        if not ext:
            ext = '.jpg'
        filename = normalize_name_key(name) + ext
        dest = os.path.join(IMAGE_DIR, filename)
        ok = download(url, dest)
        if ok:
            local = '/static/images/' + filename
            updated = update_record(model_name, name, local)
            summary.append((name, url if updated else None))
        else:
            print('Failed to download', url)
            summary.append((name, None))

    print('\nSummary:')
    for name, picked in summary:
        print('-', name, '->', picked)

if __name__ == '__main__':
    main()
