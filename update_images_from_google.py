#!/usr/bin/env python
"""
Fetch image search results for Artisans and Food Discovery items and update database.
This script uses Google, Bing, and DuckDuckGo image search to find high-quality images for:
- All artisans
- All local food establishments
- All artisan products
- All hidden gems
- All market stalls
"""

import os
import re
import time
import sqlite3
import urllib.parse
import unicodedata
from html import unescape
import requests

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, 'mysore_unseen.db')
STATIC_DIR = os.path.join(BASE, 'static', 'images')

# Ensure static/images directory exists
os.makedirs(STATIC_DIR, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/'
}

SESSION = requests.Session()
SESSION.headers.update(HEADERS)


def safe_filename(name):
    """Convert a name to a safe filename."""
    s = unicodedata.normalize('NFKD', name)
    s = re.sub(r'[^A-Za-z0-9]+', '_', s).strip('_')
    return s + '.jpg'


def extract_image_urls(html):
    """Extract image URLs from Google Images HTML."""
    urls = []
    html = html.replace('\\u003d', '=').replace('\\u0026', '&')
    urls += re.findall(r'"(https://[^"\n]+?\.(?:jpg|jpeg|png|webp))"', html, flags=re.IGNORECASE)
    urls += re.findall(r'\'(https://[^\'\n]+?\.(?:jpg|jpeg|png|webp))\'', html, flags=re.IGNORECASE)
    urls += re.findall(r'<img[^>]+src="(https://[^"\n]+?\.(?:jpg|jpeg|png|webp))"', html, flags=re.IGNORECASE)
    urls += re.findall(r'data-src="(https://[^"\n]+?\.(?:jpg|jpeg|png|webp))"', html, flags=re.IGNORECASE)
    urls += re.findall(r'data-iurl="(https://[^"\n]+?\.(?:jpg|jpeg|png|webp))"', html, flags=re.IGNORECASE)
    urls += re.findall(r'https://[^\s"\']+?\.(?:jpg|jpeg|png|webp)', html, flags=re.IGNORECASE)
    urls += re.findall(r'https://encrypted-tbn0\.gstatic\.com/[^\s"\']+', html, flags=re.IGNORECASE)
    urls += re.findall(r'https://lh3\.googleusercontent\.com/[^\s"\']+', html, flags=re.IGNORECASE)
    unique = []
    for url in urls:
        if url not in unique and url.startswith('https://'):
            unique.append(url)
    return unique


def download_image(url, filepath):
    try:
        resp = SESSION.get(url, timeout=30, stream=True)
        if resp.status_code != 200:
            return False
        content_type = resp.headers.get('Content-Type', '').lower()
        if not content_type.startswith('image'):
            return False
        content = resp.content
        if len(content) < 2000:
            return False
        with open(filepath, 'wb') as f:
            f.write(content)
        return True
    except Exception:
        return False


def extract_google_image_urls(html):
    if 'enablejs' in html and '/httpservice/retry/enablejs' in html:
        return []

    urls = []
    html = html.replace('\\u003d', '=').replace('\\u0026', '&')
    urls += re.findall(r'"ou"\s*:\s*"(https://[^"\n]+?\.(?:jpg|jpeg|png|webp))"', html, flags=re.IGNORECASE)
    urls += re.findall(r'"src"\s*:\s*"(https://[^"\n]+?\.(?:jpg|jpeg|png|webp))"', html, flags=re.IGNORECASE)
    urls += re.findall(r'"(https://[^"\n]+?\.(?:jpg|jpeg|png|webp))"', html, flags=re.IGNORECASE)
    urls += re.findall(r'https://encrypted-tbn0\.gstatic\.com/[^\s"\']+', html, flags=re.IGNORECASE)
    urls += re.findall(r'https://lh3\.googleusercontent\.com/[^\s"\']+', html, flags=re.IGNORECASE)
    unique = []
    for url in urls:
        if url.startswith('https://') and url not in unique:
            unique.append(url)
    return unique


def extract_bing_image_urls(html):
    urls = []
    urls += re.findall(r'"murl"\s*:\s*"([^"]+)"', html)
    urls += re.findall(r'"imageUrl"\s*:\s*"([^"]+)"', html)
    urls += re.findall(r'https://[^\s"\']+?\.(?:jpg|jpeg|png|webp)', html, flags=re.IGNORECASE)
    unique = []
    for url in urls:
        decoded = unescape(url)
        if decoded.startswith('http') and decoded not in unique:
            unique.append(decoded)
    return unique


def fetch_duckduckgo_image_urls(query):
    try:
        resp = SESSION.get('https://duckduckgo.com/', params={'q': query}, timeout=30)
        resp.raise_for_status()
        token = re.search(r"vqd=['\"]([^'\"]+)['\"]", resp.text)
        if not token:
            return []
        vqd = token.group(1)
        resp = SESSION.get('https://duckduckgo.com/i.js', params={'q': query, 'vqd': vqd, 'o': 'json', 'l': 'us-en', 'p': '1'}, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return [item.get('image') for item in data.get('results', []) if item.get('image')]
    except Exception:
        return []


def normalize_query(query):
    return re.sub(r"[&()']", ' ', query).replace('  ', ' ').strip()


def fetch_and_save_image(query, filename, overwrite=False):
    """Fetch image from Google Images and save locally."""
    filepath = os.path.join(STATIC_DIR, filename)
    
    if os.path.exists(filepath) and not overwrite:
        return f'/static/images/{filename}', 'Existing image'
    
    queries = [query]
    normalized = normalize_query(query)
    if normalized and normalized not in queries:
        queries.append(normalized)
    simple = ' '.join(query.split())
    if simple and simple not in queries:
        queries.append(simple)

    for search_query in queries:
        print(f'  >> Fetching: {search_query}')

        google_url = 'https://www.google.com/search?tbm=isch&q=' + urllib.parse.quote_plus(search_query)
        try:
            resp = SESSION.get(google_url, timeout=30)
            resp.raise_for_status()
            urls = extract_google_image_urls(resp.text)
        except Exception as e:
            print(f'    X Google search failed: {e}')
            urls = []

        if urls:
            for url in urls:
                if download_image(url, filepath):
                    print(f'    + Saved from Google: {filename}')
                    return f'/static/images/{filename}', 'Google Images'
            print('    X Google image downloads all failed')
        else:
            print('    ! No usable Google image URLs found')

        print('    >> Trying Bing search')
        bing_url = 'https://www.bing.com/images/async?q=' + urllib.parse.quote_plus(search_query) + '&count=50&first=0&adlt=off&safeSearch=off'
        try:
            resp = SESSION.get(bing_url, timeout=30)
            resp.raise_for_status()
            urls = extract_bing_image_urls(resp.text)
        except Exception as e:
            print(f'    X Bing search failed: {e}')
            urls = []

        if urls:
            for url in urls:
                if download_image(url, filepath):
                    print(f'    + Saved from Bing: {filename}')
                    return f'/static/images/{filename}', 'Bing Images'
            print('    X Bing image downloads all failed')
        else:
            print('    ! No usable Bing image URLs found')

        print('    >> Trying DuckDuckGo search')
        urls = fetch_duckduckgo_image_urls(search_query)
        if urls:
            for url in urls:
                if download_image(url, filepath):
                    print(f'    + Saved from DuckDuckGo: {filename}')
                    return f'/static/images/{filename}', 'DuckDuckGo Images'
            print('    X DuckDuckGo image downloads all failed')
        else:
            print('    ! No usable DuckDuckGo image URLs found')

        time.sleep(1.5)

    print(f'  X All search engines failed for: {query}')
    return None, None


def update_artisan_images(overwrite=False):
    """Fetch and update images for all artisans."""
    print('\n' + '='*70)
    print('UPDATING ARTISAN IMAGES')
    print('='*70)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, name, craft FROM artisan ORDER BY id')
    artisans = cursor.fetchall()
    
    for artisan_id, name, craft in artisans:
        print(f'\n[{artisan_id}] {name} ({craft})')
        
        query = f'{name} {craft} artisan Mysore craftsperson'
        filename = safe_filename(name)
        image_url, credit = fetch_and_save_image(query, filename, overwrite=overwrite)
        
        if image_url:
            cursor.execute(
                'UPDATE artisan SET image_url = ?, image_credit = ? WHERE id = ?',
                (image_url, credit or 'Search Images', artisan_id)
            )
            conn.commit()
            print(f'  + Database updated')
        
        time.sleep(1.5)
    
    conn.close()


def update_food_images(overwrite=False):
    """Fetch and update images for all food establishments."""
    print('\n' + '='*70)
    print('UPDATING LOCAL FOOD DISCOVERY IMAGES')
    print('='*70)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, name, food_type FROM local_food ORDER BY id')
    foods = cursor.fetchall()
    
    for food_id, name, food_type in foods:
        print(f'\n[{food_id}] {name} ({food_type})')
        
        query = f'{name} {food_type} Mysore food restaurant'
        filename = safe_filename(name)
        image_url, credit = fetch_and_save_image(query, filename, overwrite=overwrite)
        
        if image_url:
            cursor.execute(
                'UPDATE local_food SET image_url = ?, image_credit = ? WHERE id = ?',
                (image_url, credit or 'Search Images', food_id)
            )
            conn.commit()
            print(f'  + Database updated')
        
        time.sleep(1.5)
    
    conn.close()


def update_product_images(overwrite=False):
    """Fetch and update images for artisan products."""
    print('\n' + '='*70)
    print('UPDATING ARTISAN PRODUCT IMAGES')
    print('='*70)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT ap.id, ap.product_name, ap.category 
        FROM artisan_product ap
        ORDER BY ap.id
    ''')
    products = cursor.fetchall()
    
    for product_id, name, category in products:
        print(f'\n[{product_id}] {name} ({category})')
        
        query = f'{name} {category} Mysore India'
        filename = safe_filename(name)
        image_url, credit = fetch_and_save_image(query, filename, overwrite=overwrite)
        
        if image_url:
            cursor.execute(
                'UPDATE artisan_product SET image_url = ?, image_credit = ? WHERE id = ?',
                (image_url, credit or 'Search Images', product_id)
            )
            conn.commit()
            print(f'  + Database updated')
        
        time.sleep(1.5)
    
    conn.close()


def update_hidden_gem_images(overwrite=False):
    """Fetch and update images for hidden gems."""
    print('\n' + '='*70)
    print('UPDATING HIDDEN GEMS IMAGES')
    print('='*70)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, name, category FROM hidden_gem ORDER BY id')
    gems = cursor.fetchall()
    
    for gem_id, name, category in gems:
        print(f'\n[{gem_id}] {name} ({category})')
        
        query = f'{name} {category} Mysore destination'
        filename = safe_filename(name)
        image_url, credit = fetch_and_save_image(query, filename, overwrite=overwrite)
        
        if image_url:
            cursor.execute(
                'UPDATE hidden_gem SET image_url = ?, image_credit = ? WHERE id = ?',
                (image_url, credit or 'Search Images', gem_id)
            )
            conn.commit()
            print(f'  + Database updated')
        
        time.sleep(1.5)
    
    conn.close()


def update_market_stall_images(overwrite=False):
    """Fetch and update images for market stalls."""
    print('\n' + '='*70)
    print('UPDATING MARKET STALL IMAGES')
    print('='*70)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, stall_name, market_area FROM market_stall ORDER BY id')
    stalls = cursor.fetchall()
    
    for stall_id, name, market_area in stalls:
        print(f'\n[{stall_id}] {name} ({market_area})')
        
        query = f'{name} {market_area} Mysore market'
        filename = safe_filename(name)
        image_url, credit = fetch_and_save_image(query, filename, overwrite=overwrite)
        
        if image_url:
            cursor.execute(
                'UPDATE market_stall SET image_url = ?, image_credit = ? WHERE id = ?',
                (image_url, credit or 'Search Images', stall_id)
            )
            conn.commit()
            print(f'  + Database updated')
        
        time.sleep(1.5)
    
    conn.close()


def update_stay_option_images(overwrite=False):
    """Fetch and update images for stay options."""
    print('\n' + '='*70)
    print('UPDATING STAY OPTION IMAGES')
    print('='*70)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('SELECT id, name, location FROM stay_option ORDER BY id')
    stays = cursor.fetchall()

    for stay_id, name, location in stays:
        print(f'\n[{stay_id}] {name} ({location})')

        query = f'{name} {location} Mysore hotel heritage stay'
        filename = safe_filename(name)
        image_url, credit = fetch_and_save_image(query, filename, overwrite=overwrite)

        if image_url:
            cursor.execute(
                'UPDATE stay_option SET image_url = ?, image_credit = ? WHERE id = ?',
                (image_url, credit or 'Search Images', stay_id)
            )
            conn.commit()
            print(f'  + Database updated')

        time.sleep(1.5)

    conn.close()


def update_local_guide_images(overwrite=False):
    """Fetch and update images for local guides."""
    print('\n' + '='*70)
    print('UPDATING LOCAL GUIDE IMAGES')
    print('='*70)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('SELECT id, name, expertise FROM local_guide ORDER BY id')
    guides = cursor.fetchall()

    for guide_id, name, expertise in guides:
        print(f'\n[{guide_id}] {name} ({expertise})')

        query = f'{name} {expertise} Mysore tour guide'
        filename = safe_filename(name)
        image_url, credit = fetch_and_save_image(query, filename, overwrite=overwrite)

        if image_url:
            cursor.execute(
                'UPDATE local_guide SET image_url = ?, image_credit = ? WHERE id = ?',
                (image_url, credit or 'Search Images', guide_id)
            )
            conn.commit()
            print(f'  + Database updated')

        time.sleep(1.5)

    conn.close()


def main():
    """Run all image updates."""
    print('\n' + '='*70)
    print('MYSORE UNSEEN - IMAGE UPDATE FROM SEARCH ENGINES')
    print('='*70)
    print(f'Database: {DB_PATH}')
    print(f'Images Directory: {STATIC_DIR}')
    
    try:
        update_artisan_images(overwrite=True)
        update_food_images(overwrite=True)
        update_product_images(overwrite=True)
        update_hidden_gem_images(overwrite=True)
        update_market_stall_images(overwrite=True)
        update_stay_option_images(overwrite=True)
        update_local_guide_images(overwrite=True)
        
        print('\n' + '='*70)
        print('ALL IMAGES UPDATED SUCCESSFULLY!')
        print('='*70)
        print('\nYour application now has images for:')
        print('  All Artisans (Artisan Explore section)')
        print('  All Food Discoveries (Food Discovery section)')
        print('  All Artisan Products')
        print('  All Hidden Gems')
        print('  All Market Stalls')
        print('  All Stay Options')
        print('  All Local Guides')
        print('\nStart the app with: python app.py')
        print('='*70 + '\n')
        
    except Exception as e:
        print(f'\nX ERROR: {e}')
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == '__main__':
    import sys
    success = main()
    sys.exit(0 if success else 1)
