import requests
import urllib.parse
from html import unescape

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}
queries = [
    'Shuka Vana Parrot Park Mysore',
    'Guru Sweet Mart Mysore',
    'Venugopala Swamy Temple Mysore',
    'Sand Sculpture Museum Mysore',
    'Melody World Wax Museum Mysore',
    'Jayalakshmi Vilas Mansion Mysore',
    'Sri Nandi Temple Chamundi Hill Mysore',
]
for q in queries:
    url = 'https://www.bing.com/images/search?q=' + urllib.parse.quote_plus(q)
    print('QUERY:', q)
    r = requests.get(url, headers=headers, timeout=30)
    print('status', r.status_code)
    text = r.text
    matches = []
    idx = 0
    while True:
        idx = text.find('murl', idx)
        if idx == -1:
            break
        start = text.find('"', idx + 4) + 1
        end = text.find('"', start)
        matches.append(unescape(text[start:end]))
        idx = end + 1
        if len(matches) >= 5:
            break
    for i, m in enumerate(matches):
        print(i+1, m)
    print('---')
