import requests, re, urllib.parse
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}
queries = ['Shuka Vana Parrot Park Mysore', 'Guru Sweet Mart Mysore', 'Chamundi Hill Nandi Mysore', 'Lingambudhi Lake Mysore', 'Kunti Betta Mysore', 'Venugopala Swamy Temple Mysore', 'Sand Sculpture Museum Mysore']
for q in queries:
    print('QUERY:', q)
    search_url = 'https://duckduckgo.com/?q=' + urllib.parse.quote_plus(q) + '&iax=images&ia=images'
    r = requests.get(search_url, headers=headers, timeout=30)
    html = r.text
    match = re.search(r'vqd=\'([^\']+)\'', html)
    if not match:
        match = re.search(r'vqd="([^"]+)"', html)
    if not match:
        print('  no vqd token')
        continue
    vqd = match.group(1)
    api_url = f'https://duckduckgo.com/i.js?l=us-en&o=json&q={urllib.parse.quote_plus(q)}&vqd={vqd}'
    r2 = requests.get(api_url, headers=headers, timeout=30)
    print('  api status', r2.status_code)
    print(r2.text[:1000])
    try:
        data = r2.json()
        for item in data.get('results', [])[:5]:
            print('   ', item.get('image'), item.get('thumbnail'))
    except Exception as e:
        print('  parse error', e)
    print()