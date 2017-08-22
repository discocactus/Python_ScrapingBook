import requests
import lxml.html

response = requests.get('https://gihyo.jp/dp')
root = lxml.html.fromstring(response.content)
root.make_links_absolute(response.url)  # すべてのリンクを絶対URLに変換する。

# id="listBook"である要素の子孫のa要素のみを取得する。
for a in root.cssselect('#listBook a[itemprop="url"]'):
    url = a.get('href')
    print(url)
