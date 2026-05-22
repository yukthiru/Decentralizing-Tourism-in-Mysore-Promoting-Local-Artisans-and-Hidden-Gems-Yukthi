import requests, urllib.parse, re
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}
q = 'Lingambudhi Lake Mysore'
url = 'https://www.bing.com/images/search?q=' + urllib.parse.quote_plus(q)
r = requests.get(url, headers=headers, timeout=30)
text = r.text
print('status', r.status_code)
for pat in [r'\\"\\,?murl\\":\\"(https?://[^\\"]+?)\\"', r'murl\\":\\"(https?://[^\\"]+?)\\"', r'murl\\":\\"(https?://[^\\"]+?\\.(?:jpg|jpeg|png|webp))\\"', r'\"murl\":\"(https?://[^\"]+?)\"']:
    m = re.search(pat, text)
    print('PAT', pat, 'FOUND', bool(m))
    if m:
        print('FIRST', m.group(1))
idx = text.find('murl')
print('--- raw excerpt ---')
print(text[idx:idx+400])
