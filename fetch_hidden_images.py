import re
import requests
import urllib.parse

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}
places = [
    'Shuka Vana Parrot Park Mysore',
    'Lingambudhi Lake Mysore',
    'Jayalakshmi Vilas Mansion Folklore Museum Mysore',
    'Melody World Wax Museum Mysore',
    'Venugopala Swamy Temple Mysore',
    'Kunti Betta Mysore',
    'Sand Sculpture Museum Mysore',
    'Varuna Lake Mysore',
    'Chunchanakatte Falls Mysore',
    'Guru Sweet Mart Mysore',
    'Sri Nandi Temple Mysore'
]

patterns = [
    re.compile(r'imgurl=(https?%3A%2F%2F[^&"\s]+)'),
    re.compile(r'"(https?://[^"\s]+\.(?:jpg|jpeg|png))"'),
    re.compile(r'data-src="(https?://[^"\s]+)"'),
    re.compile(r'data-iurl="(https?://[^"\s]+)"')
]

for place in places:
    q = urllib.parse.quote_plus(place)
    url = f'https://www.google.com/search?q={q}&tbm=isch'
    print(f'\n=== {place} ===')
    r = requests.get(url, headers=headers, timeout=30)
    print('status', r.status_code)
    if r.status_code != 200:
        continue
    text = r.text
    results = []
    for pat in patterns:
        for m in pat.findall(text):
            if isinstance(m, tuple):
                m = m[0]
            if m.startswith('https%3A'):
                m = urllib.parse.unquote(m)
            if m not in results:
                results.append(m)
            if len(results) >= 10:
                break
        if len(results) >= 10:
            break
    for m in results[:10]:
        print(m)
