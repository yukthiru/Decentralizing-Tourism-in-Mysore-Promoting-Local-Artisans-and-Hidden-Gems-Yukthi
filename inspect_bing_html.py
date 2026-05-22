import requests, urllib.parse

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}
queries = ['Shuka Vana Parrot Park Mysore', 'Guru Sweet Mart Mysore', 'Chamundi Hill Nandi', 'Lingambudhi Lake Mysore']
for q in queries:
    url = 'https://www.bing.com/images/search?q=' + urllib.parse.quote_plus(q)
    print('QUERY', q)
    r = requests.get(url, headers=headers, timeout=30)
    print('status', r.status_code)
    text = r.text
    for token in ['murl', 'imgurl', 'data-src', 'data-thumburl', 'src=', 'href=']:
        idx = text.find(token)
        if idx != -1:
            print(token, text[idx:idx+300])
    print('---')
