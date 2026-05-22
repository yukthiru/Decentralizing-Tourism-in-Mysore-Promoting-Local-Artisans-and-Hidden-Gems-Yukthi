import os
import re
import json
import time
import urllib.parse
import unicodedata
import argparse

import requests

BASE = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE, 'static', 'images')
if not os.path.isdir(STATIC_DIR):
    os.makedirs(STATIC_DIR)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/'
}


def safe_filename(name):
    s = unicodedata.normalize('NFKD', name)
    s = re.sub(r'[^A-Za-z0-9]+', '_', s).strip('_')
    return s + '.jpg'


def extract_image_urls(html):
    urls = []
    html = html.replace('\\u003d', '=').replace('\\u0026', '&')
    urls += re.findall(r'"(https://[^"\n]+?\.(?:jpg|jpeg|png|webp))"', html, flags=re.IGNORECASE)
    urls += re.findall(r'\'(https://[^\'\n]+?\.(?:jpg|jpeg|png|webp))\'', html, flags=re.IGNORECASE)
    urls += re.findall(r'https://[^\s"\']+?\.(?:jpg|jpeg|png|webp)', html, flags=re.IGNORECASE)
    unique = []
    for url in urls:
        if url not in unique:
            if url.startswith('https://'):
                unique.append(url)
    return unique


def fetch_image(query, out_path, overwrite=False):
    if os.path.exists(out_path) and not overwrite:
        print('Exists:', out_path)
        return True

    search_url = 'https://www.google.com/search?tbm=isch&q=' + urllib.parse.quote_plus(query)
    print('Searching Google Images for:', query)
    try:
        resp = requests.get(search_url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
    except Exception as exc:
        print('Failed search request:', exc)
        return False

    urls = extract_image_urls(resp.text)
    if not urls:
        print('No image URLs found in Google search results for', query)
        return False

    for url in urls:
        try:
            download = requests.get(url, headers=HEADERS, timeout=30)
            if download.status_code == 200 and len(download.content) > 2000:
                with open(out_path, 'wb') as f:
                    f.write(download.content)
                print('Downloaded:', out_path)
                return True
        except Exception as exc:
            print('Download failed for', url, exc)
    print('Unable to download any valid image for', query)
    return False


def load_place_names(seed_file):
    text = open(seed_file, 'r', encoding='utf-8').read()
    names = re.findall(r'name\s*=\s*"([^"]+)"', text)
    names += re.findall(r'stall_name\s*=\s*"([^"]+)"', text)
    names += re.findall(r'product_name\s*=\s*"([^"]+)"', text)
    # Deduplicate preserving order
    unique = []
    for n in names:
        if n not in unique:
            unique.append(n)
    return unique


def main():
    parser = argparse.ArgumentParser(description='Download Google Images for seeded place names.')
    parser.add_argument('--seed-file', default=os.path.join(BASE, 'seed_data.py'))
    parser.add_argument('--limit', type=int, default=None)
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()

    names = load_place_names(args.seed_file)
    if args.limit:
        names = names[:args.limit]

    for name in names:
        query = f'{name} Mysore'
        out_path = os.path.join(STATIC_DIR, safe_filename(name))
        fetch_image(query, out_path, overwrite=args.overwrite)
        time.sleep(1.5)

    print('Done')


if __name__ == '__main__':
    main()
