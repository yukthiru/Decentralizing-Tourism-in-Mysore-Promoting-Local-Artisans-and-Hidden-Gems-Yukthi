import requests, urllib.parse, time
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}
queries = [
    'Shuka Vana Parrot Park Mysore',
    'Lingambudhi Lake',
    'Jayalakshmi Vilas Mansion',
    'Melody World Wax Museum',
    'Venugopala Swamy Temple Mysore',
    'Kunti Betta',
    'Tonachi Koppal',
    'Raghupathi Bhat Ganjifa',
    'Sand Sculpture Museum Mysore',
    'Varuna Lake Mysore',
    'Chunchanakatte Falls',
    'Guru Sweet Mart Mysore',
    'Sri Nandi Temple Chamundi Hill Mysore'
]
for q in queries:
    print('QUERY:', q)
    search_url = 'https://en.wikipedia.org/w/api.php?action=query&list=search&format=json&srsearch=' + urllib.parse.quote_plus(q)
    r = requests.get(search_url, headers=headers, timeout=20)
    if r.status_code != 200:
        print('  search status', r.status_code)
        continue
    search_data = r.json()
    results = search_data.get('query', {}).get('search', [])
    if not results:
        print('  no search results')
        continue
    title = results[0]['title']
    print('  top title:', title)
    info_url = 'https://en.wikipedia.org/w/api.php?action=query&format=json&prop=pageimages&piprop=original&titles=' + urllib.parse.quote_plus(title)
    r2 = requests.get(info_url, headers=headers, timeout=20)
    print('  info status', r2.status_code)
    data2 = r2.json()
    pages = data2.get('query', {}).get('pages', {})
    for pid, page in pages.items():
        if 'missing' in page:
            print('  missing pageimage')
        else:
            print('  image:', page.get('original', {}).get('source'))
    time.sleep(1)
    print()