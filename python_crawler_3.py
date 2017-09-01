
# 一覧ページからURLの一覧を抜き出す(3)
# あとで利用しやすいよう関数をつかってリファクタリングしておく

import requests
import lxml.html

def main():
    """
    クローラーのメインの処理
    """
    response = requests.get('https://gihyo.jp/dp')
    # scrape_list_page()関数を呼び出し、ジェネレーターイテレーターを取得
    urls = scrape_list_page(response)
    for url in urls: # ジェネレーターイテレーターはlistなどと同様に繰り返し可能
        print(url)

def scrape_list_page(response):
    """
    一覧ページのResponseから詳細ページのURLを抜き出すジェネレーター関数
    """
    root = lxml.html.fromstring(response.content)
    root.make_links_absolute(response.url) # すべてのリンクを絶対URLに変換する

    # id="listBook"である要素の子孫のa要素のみを取得する
    for a in root.cssselect('#listBook a[itemprop="url"]'):
        url = a.get('href')
        yield url # yield文でジェネレーターイテレーターの要素を返す
        
if __name__ == '__main__':
    main()