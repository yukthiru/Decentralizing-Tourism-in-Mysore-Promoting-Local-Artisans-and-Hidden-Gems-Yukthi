import requests
import urllib.parse
from html import unescape
import os
import unicodedata

BASE = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE, 'static', 'images')
if not os.path.isdir(STATIC_DIR):
    os.makedirs(STATIC_DIR)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

names = [
    'Lingambudhi Lake Mysore',
    'Shuka Vana Parrot Park Mysore',
    'Jayalakshmi Vilas Mansion Folklore Museum Mysore',
    'Melody World Wax Museum Mysore',
    'Venugopala Swamy Temple Mysore',
    'Kunti Betta Mysore'
]


def safe_filename(name):
    s = unicodedata.normalize('NFKD', name)
    s = ''.join(c if c.isalnum() else '_' for c in s).strip('_')
    return s + '.jpg'


def fetch_one(query, out_path):
    url = 'https://www.bing.com/images/search?q=' + urllib.parse.quote_plus(query)
    print('Searching:', query)
    r = requests.get(url, headers=headers, timeout=30)
    if r.status_code != 200:
        print('Search failed', r.status_code)
        return False
    text = r.text
    matches = []
    idx = 0
    while True:
        idx = text.find('murl', idx)
        if idx == -1:
            break
        start = text.find('"', idx + 4) + 1
        end = text.find('"', start)
        if start == 0 or end == -1:
            break
        candidate = unescape(text[start:end])
        idx = end + 1
        if candidate.lower().startswith('http') and candidate.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            matches.append(candidate)
            if len(matches) >= 10:
                break
    for candidate in matches:
        try:
            img = requests.get(candidate, headers=headers, timeout=30)
            if img.status_code == 200 and len(img.content) > 2000:
                with open(out_path, 'wb') as f:
                    f.write(img.content)
                print('Saved:', out_path)
                return True
        except Exception as exc:
            print('download failed', candidate, exc)
    print('No valid image found for', query)
    return False

for name in names:
    fname = safe_filename(name.replace(' Mysore', ''))
    out_path = os.path.join(STATIC_DIR, fname)
    if fetch_one(name, out_path):
        print('Completed', name)
    else:
        print('Failed', name)
