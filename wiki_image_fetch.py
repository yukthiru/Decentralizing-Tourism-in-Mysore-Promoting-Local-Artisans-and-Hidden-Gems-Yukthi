import requests
import urllib.parse

place_names = [
    'Shuka Vana Parrot Park Mysore',
    'Lingambudhi Lake',
    'Jayalakshmi Vilas Mansion',
    'Melody World Wax Museum',
    'Venugopala Swamy Temple Mysore',
    'Kunti Betta',
    'Tonachi Koppal',
    'Mysore rosewood inlay',
    'Raghupathi Bhat Ganjifa',
    'Sand Sculpture Museum Mysore',
    'Varuna Lake Mysore',
    'Chunchanakatte Falls',
    'Guru Sweet Mart Mysore',
    'Nandi Chamundi Hill Mysore'
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

for place in place_names:
    title = place.replace(' ', '_')
    url = f'https://en.wikipedia.org/w/api.php?action=query&format=json&prop=pageimages&piprop=original&titles={title}'
    try:
        r = requests.get(url, headers=headers, timeout=20)
        print('===', place, '=== status', r.status_code)
        print(r.text[:300])
        data = r.json()
    except Exception as e:
        print(place)
        print('  ERROR', e)
        continue
    pages = data.get('query', {}).get('pages', {})
    for pid, page in pages.items():
        if 'missing' in page:
            print(place)
            print('  MISSING')
        else:
            print(place)
            print('  title:', page.get('title'))
            print('  image:', page.get('original', {}).get('source'))
    print()
