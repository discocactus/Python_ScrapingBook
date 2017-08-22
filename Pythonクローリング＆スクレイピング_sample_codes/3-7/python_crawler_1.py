import requests
import lxml.html

response = requests.get('https://gihyo.jp/dp')
root = lxml.html.fromstring(response.content)
for a in root.cssselect('a[itemprop="url"]'):
    url = a.get('href')
    print(url)
