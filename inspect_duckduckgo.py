import requests, urllib.parse
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}
q='Shuka Vana Parrot Park Mysore'
url='https://duckduckgo.com/?q='+urllib.parse.quote_plus(q)+'&iax=images&ia=images'
print(url)
r=requests.get(url,headers=headers,timeout=30)
print('status',r.status_code)
text=r.text
print(text[:2000])
print('find vqd', text.find('vqd'))
