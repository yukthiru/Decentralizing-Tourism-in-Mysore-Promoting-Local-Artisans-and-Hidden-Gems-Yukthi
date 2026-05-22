import requests
import re
import urllib.parse

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/'
}

query = 'Lingambudhi Lake Mysore'
url = 'https://www.google.com/search?tbm=isch&q=' + urllib.parse.quote_plus(query)
resp = requests.get(url, headers=HEADERS, timeout=30)
print('status', resp.status_code)
text = resp.text
print(text[:2000])
print('--- has https image url pattern?')
print(bool(re.search(r'"(https://[^"\n]+?\.(?:jpg|jpeg|png|webp))"', text, flags=re.IGNORECASE)))
print('--- has img src pattern?')
print(bool(re.search(r'<img[^>]+src="(https://[^"\n]+?\.(?:jpg|jpeg|png|webp))"', text, flags=re.IGNORECASE)))
print('--- found sample urls')
print(re.findall(r'"(https://[^"\n]+?\.(?:jpg|jpeg|png|webp))"', text, flags=re.IGNORECASE)[:10])
