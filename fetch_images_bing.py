import requests
import urllib.parse
from html import unescape
import re
import os

BASE = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE, 'static', 'images')
if not os.path.isdir(STATIC_DIR):
    os.makedirs(STATIC_DIR)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

# Read seed_data.py and extract names used in object constructors
seed_file = os.path.join(BASE, 'seed_data.py')
with open(seed_file, 'r', encoding='utf-8') as f:
    text = f.read()

# Match name="..." occurrences (simple heuristic)
names = re.findall(r'name\s*=\s*"([^"]+)"', text)
# Also match stall_name and product_name
names += re.findall(r'stall_name\s*=\s*"([^"]+)"', text)
names += re.findall(r'product_name\s*=\s*"([^"]+)"', text)
# also match guide names already covered by name

# Deduplicate while preserving order
seen = set()
unique_names = []
for n in names:
    if n not in seen:
        seen.add(n)
        unique_names.append(n)

print(f'Found {len(unique_names)} unique place names to search')

# Normalize filename
import unicodedata

def safe_filename(name):
    s = unicodedata.normalize('NFKD', name)
    s = re.sub(r'[^A-Za-z0-9]+', '_', s).strip('_')
    return s + '.jpg'


def fetch_one(query, out_path):
    print('Searching:', query)
    url = 'https://www.bing.com/images/search?q=' + urllib.parse.quote_plus(query)
    try:
        r = requests.get(url, headers=headers, timeout=30)
        if r.status_code != 200:
            print('Failed search', r.status_code)
            return False
        text = r.text
        idx = 0
        murl = None
        while True:
            idx = text.find('murl', idx)
            if idx == -1:
                break
            start = text.find('"', idx + 4) + 1
            end = text.find('"', start)
            candidate = unescape(text[start:end])
            if candidate.lower().startswith('http') and candidate.lower().endswith(('.jpg', '.jpeg', '.png')):
                murl = candidate
                break
            idx = end + 1
        if not murl:
            print('No direct image URL found for', query)
            return False
        print('Found image URL:', murl)
        img = requests.get(murl, headers=headers, timeout=30)
        if img.status_code == 200:
            with open(out_path, 'wb') as out:
                out.write(img.content)
            print('Saved', out_path)
            return True
        else:
            print('Failed to download image', img.status_code)
            return False
    except Exception as e:
        print('Error fetching', e)
        return False

# Iterate names and download if not exists
for name in unique_names:
    fname = safe_filename(name)
    out = os.path.join(STATIC_DIR, fname)
    if os.path.exists(out) and os.path.getsize(out) > 1000:
        print('Already exists:', fname)
        continue
    q = name + ' Mysore'
    ok = fetch_one(q, out)
    if not ok:
        # try without Mysore
        fetch_one(name, out)

print('Done')
