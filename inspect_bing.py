import requests
import urllib.parse

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}
q = 'Shuka Vana Parrot Park Mysore'
url = 'https://www.bing.com/images/search?q=' + urllib.parse.quote_plus(q)
print('URL:', url)
r = requests.get(url, headers=headers, timeout=30)
print('status', r.status_code)
text = r.text
idx = text.find('murl')
print('idx', idx)
print(text[max(idx-200,0):idx+500])
