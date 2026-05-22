"""
Comprehensive image fetcher for artisans, food, and other Mysore attractions.
Fetches images from Google Images and updates the database.
"""

import os
import re
import json
import time
import sqlite3
import urllib.parse
import unicodedata
from pathlib import Path

import requests

BASE = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE, 'static', 'images')
DB_PATH = os.path.join(BASE, 'mysore_unseen.db')

if not os.path.isdir(STATIC_DIR):
    os.makedirs(STATIC_DIR)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/'
}


def safe_filename(name):
    """Convert a name to a safe filename."""
    s = unicodedata.normalize('NFKD', name)
    s = re.sub(r'[^A-Za-z0-9]+', '_', s).strip('_')
    return s + '.jpg'


def extract_image_urls(html):
    """Extract image URLs from Google Images search results."""
    urls = []
    html = html.replace('\\u003d', '=').replace('\\u0026', '&')
    urls += re.findall(r'"(https://[^"\n]+?\.(?:jpg|jpeg|png|webp))"', html, flags=re.IGNORECASE)
    urls += re.findall(r'\'(https://[^\'\n]+?\.(?:jpg|jpeg|png|webp))\'', html, flags=re.IGNORECASE)
    urls += re.findall(r'https://[^\s"\']+?\.(?:jpg|jpeg|png|webp)', html, flags=re.IGNORECASE)
    
    unique = []
    for url in urls:
        if url not in unique and url.startswith('https://'):
            unique.append(url)
    return unique


def fetch_and_save_image(query, out_path, overwrite=False):
    """Fetch an image from Google Images and save it."""
    if os.path.exists(out_path) and not overwrite:
        print(f'  ✓ Image exists: {os.path.basename(out_path)}')
        return True

    print(f'  ⬇ Fetching image for: {query}')
    search_url = 'https://www.google.com/search?tbm=isch&q=' + urllib.parse.quote_plus(query)
    
    try:
        resp = requests.get(search_url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        print(f'  ✗ Search failed: {e}')
        return False

    urls = extract_image_urls(resp.text)
    if not urls:
        print(f'  ✗ No image URLs found')
        return False

    for url in urls:
        try:
            download = requests.get(url, headers=HEADERS, timeout=30)
            if download.status_code == 200 and len(download.content) > 2000:
                with open(out_path, 'wb') as f:
                    f.write(download.content)
                print(f'  ✓ Downloaded: {os.path.basename(out_path)}')
                return True
        except Exception as e:
            continue
    
    print(f'  ✗ Failed to download any valid image')
    return False


def get_db_connection():
    """Get SQLite database connection."""
    return sqlite3.connect(DB_PATH)


def fetch_artisan_images(overwrite=False):
    """Fetch and update images for artisans."""
    print('\n' + '='*60)
    print('FETCHING ARTISAN IMAGES')
    print('='*60)
    
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, name, craft FROM artisan')
    artisans = cursor.fetchall()
    
    for artisan in artisans:
        aid, name, craft = artisan['id'], artisan['name'], artisan['craft']
        
        # Check if already has a proper image
        cursor.execute('SELECT image_url FROM artisan WHERE id = ?', (aid,))
        current = cursor.fetchone()['image_url']
        
        if current and current.startswith('/static/images/') and not overwrite:
            print(f'\n[Artisan {aid}] {name} - Image already set')
            continue
        
        print(f'\n[Artisan {aid}] {name} ({craft})')
        
        # Try fetching with craft-specific query
        query = f'{name} {craft} artisan Mysore'
        filename = safe_filename(name)
        filepath = os.path.join(STATIC_DIR, filename)
        
        success = fetch_and_save_image(query, filepath, overwrite)
        
        if success:
            image_url = f'/static/images/{filename}'
            cursor.execute(
                'UPDATE artisan SET image_url = ?, image_credit = ? WHERE id = ?',
                (image_url, 'Google Images', aid)
            )
            conn.commit()
            print(f'  ✓ Updated database')
        
        time.sleep(1.5)
    
    conn.close()


def fetch_food_images(overwrite=False):
    """Fetch and update images for local food."""
    print('\n' + '='*60)
    print('FETCHING LOCAL FOOD IMAGES')
    print('='*60)
    
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, name, food_type FROM local_food')
    foods = cursor.fetchall()
    
    for food in foods:
        fid, name, food_type = food['id'], food['name'], food['food_type']
        
        # Check if already has a proper image
        cursor.execute('SELECT image_url FROM local_food WHERE id = ?', (fid,))
        current = cursor.fetchone()['image_url']
        
        if current and current.startswith('/static/images/') and not overwrite:
            print(f'\n[Food {fid}] {name} - Image already set')
            continue
        
        print(f'\n[Food {fid}] {name} ({food_type})')
        
        # Try fetching with food-specific query
        query = f'{name} {food_type} Mysore'
        filename = safe_filename(name)
        filepath = os.path.join(STATIC_DIR, filename)
        
        success = fetch_and_save_image(query, filepath, overwrite)
        
        if success:
            image_url = f'/static/images/{filename}'
            cursor.execute(
                'UPDATE local_food SET image_url = ?, image_credit = ? WHERE id = ?',
                (image_url, 'Google Images', fid)
            )
            conn.commit()
            print(f'  ✓ Updated database')
        
        time.sleep(1.5)
    
    conn.close()


def fetch_artisan_product_images(overwrite=False):
    """Fetch and update images for artisan products."""
    print('\n' + '='*60)
    print('FETCHING ARTISAN PRODUCT IMAGES')
    print('='*60)
    
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT ap.id, ap.product_name, ap.category, a.name as artisan_name 
        FROM artisan_product ap
        JOIN artisan a ON ap.artisan_id = a.id
    ''')
    products = cursor.fetchall()
    
    for product in products:
        pid = product['id']
        product_name = product['product_name']
        category = product['category']
        
        # Check if already has a proper image
        cursor.execute('SELECT image_url FROM artisan_product WHERE id = ?', (pid,))
        current = cursor.fetchone()['image_url']
        
        if current and current.startswith('/static/images/') and not overwrite:
            print(f'\n[Product {pid}] {product_name} - Image already set')
            continue
        
        print(f'\n[Product {pid}] {product_name} ({category})')
        
        # Try fetching with product-specific query
        query = f'{product_name} {category} Mysore'
        filename = safe_filename(product_name)
        filepath = os.path.join(STATIC_DIR, filename)
        
        success = fetch_and_save_image(query, filepath, overwrite)
        
        if success:
            image_url = f'/static/images/{filename}'
            cursor.execute(
                'UPDATE artisan_product SET image_url = ?, image_credit = ? WHERE id = ?',
                (image_url, 'Google Images', pid)
            )
            conn.commit()
            print(f'  ✓ Updated database')
        
        time.sleep(1.5)
    
    conn.close()


def fetch_hidden_gem_images(overwrite=False):
    """Fetch and update images for hidden gems."""
    print('\n' + '='*60)
    print('FETCHING HIDDEN GEM IMAGES')
    print('='*60)
    
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, name, category FROM hidden_gem')
    gems = cursor.fetchall()
    
    for gem in gems:
        gid, name, category = gem['id'], gem['name'], gem['category']
        
        # Check if already has a proper image
        cursor.execute('SELECT image_url FROM hidden_gem WHERE id = ?', (gid,))
        current = cursor.fetchone()['image_url']
        
        if current and current.startswith('/static/images/') and not overwrite:
            print(f'\n[Gem {gid}] {name} - Image already set')
            continue
        
        print(f'\n[Gem {gid}] {name} ({category})')
        
        # Try fetching with gem-specific query
        query = f'{name} {category} Mysore'
        filename = safe_filename(name)
        filepath = os.path.join(STATIC_DIR, filename)
        
        success = fetch_and_save_image(query, filepath, overwrite)
        
        if success:
            image_url = f'/static/images/{filename}'
            cursor.execute(
                'UPDATE hidden_gem SET image_url = ?, image_credit = ? WHERE id = ?',
                (image_url, 'Google Images', gid)
            )
            conn.commit()
            print(f'  ✓ Updated database')
        
        time.sleep(1.5)
    
    conn.close()


def fetch_market_stall_images(overwrite=False):
    """Fetch and update images for market stalls."""
    print('\n' + '='*60)
    print('FETCHING MARKET STALL IMAGES')
    print('='*60)
    
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, stall_name, market_area FROM market_stall')
    stalls = cursor.fetchall()
    
    for stall in stalls:
        sid, stall_name, market_area = stall['id'], stall['stall_name'], stall['market_area']
        
        # Check if already has a proper image
        cursor.execute('SELECT image_url FROM market_stall WHERE id = ?', (sid,))
        current = cursor.fetchone()['image_url']
        
        if current and current.startswith('/static/images/') and not overwrite:
            print(f'\n[Stall {sid}] {stall_name} - Image already set')
            continue
        
        print(f'\n[Stall {sid}] {stall_name} ({market_area})')
        
        # Try fetching with stall-specific query
        query = f'{stall_name} {market_area} Mysore'
        filename = safe_filename(stall_name)
        filepath = os.path.join(STATIC_DIR, filename)
        
        success = fetch_and_save_image(query, filepath, overwrite)
        
        if success:
            image_url = f'/static/images/{filename}'
            cursor.execute(
                'UPDATE market_stall SET image_url = ?, image_credit = ? WHERE id = ?',
                (image_url, 'Google Images', sid)
            )
            conn.commit()
            print(f'  ✓ Updated database')
        
        time.sleep(1.5)
    
    conn.close()


def main():
    """Main function to fetch all images."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Fetch Google Images for Mysore Unseen database.')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing images')
    parser.add_argument('--target', choices=['all', 'artisans', 'food', 'products', 'gems', 'stalls'], 
                       default='all', help='Which images to fetch')
    args = parser.parse_args()
    
    print('\n' + '='*60)
    print('MYSORE UNSEEN - IMAGE FETCHER')
    print('='*60)
    print(f'Database: {DB_PATH}')
    print(f'Output Directory: {STATIC_DIR}')
    print(f'Overwrite Mode: {args.overwrite}')
    print(f'Target: {args.target}')
    
    try:
        if args.target in ['all', 'artisans']:
            fetch_artisan_images(args.overwrite)
        
        if args.target in ['all', 'food']:
            fetch_food_images(args.overwrite)
        
        if args.target in ['all', 'products']:
            fetch_artisan_product_images(args.overwrite)
        
        if args.target in ['all', 'gems']:
            fetch_hidden_gem_images(args.overwrite)
        
        if args.target in ['all', 'stalls']:
            fetch_market_stall_images(args.overwrite)
        
        print('\n' + '='*60)
        print('✓ IMAGE FETCHING COMPLETE')
        print('='*60 + '\n')
        
    except Exception as e:
        print(f'\n✗ ERROR: {e}')
        raise


if __name__ == '__main__':
    main()
