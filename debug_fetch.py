import requests
import urllib.parse

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}
place = 'Shuka Vana Parrot Park Mysore'
query = urllib.parse.quote_plus(place)
url = f'https://www.google.com/search?q={query}&tbm=isch'
print('URL:', url)
response = requests.get(url, headers=headers, timeout=30)
print('Status:', response.status_code)
text = response.text
print(text[:2000].replace('\n', ' '))
