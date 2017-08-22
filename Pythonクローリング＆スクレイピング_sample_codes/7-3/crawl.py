import time
import re
import sys

import requests
import lxml.html
from pymongo import MongoClient
from redis import Redis
from rq import Queue


def main():
    """
    クローラーのメインの処理。
    """
    q = Queue(connection=Redis())

    client = MongoClient('localhost', 27017)  # ローカルホストのMongoDBに接続する。
    collection = client.scraping.ebook_htmls  # scrapingデータベースのebook_htmlsコレクションを得る。
    # keyで高速に検索できるように、ユニークなインデックスを作成する。
    collection.create_index('key', unique=True)

    session = requests.Session()
    response = session.get('https://gihyo.jp/dp')  # 一覧ページを取得する。
    urls = scrape_list_page(response)  # 詳細ページのURL一覧を得る。
    for url in urls:
        key = extract_key(url)  # URLからキーを取得する。

        ebook_html = collection.find_one({'key': key})  # MongoDBからkeyに該当するデータを探す。
        if not ebook_html:  # MongoDBに存在しない場合だけ、詳細ページをクロールする。
            time.sleep(1)
            print('Fetching {0}'.format(url), file=sys.stderr)
            response = session.get(url)  # 詳細ページを取得する。

            # HTMLをMongoDBに保存する。
            collection.insert_one({
                'url': url,
                'key': key,
                'html': response.content,
            })

            # キューにジョブを追加する。
            # result_ttl=0という引数はタスクの戻り値を保存しないことを意味する。
            q.enqueue('scraper_tasks.scrape', key, result_ttl=0)


def scrape_list_page(response):
    """
    一覧ページのResponseから詳細ページのURLを抜き出す。
    """
    root = lxml.html.fromstring(response.content)
    root.make_links_absolute(response.url)

    for a in root.cssselect('#listBook a[itemprop="url"]'):
        url = a.get('href')
        yield url


def extract_key(url):
    """
    URLからキー (URLの末尾のISBN) を抜き出す。
    """
    m = re.search(r'/([^/]+)$', url)
    return m.group(1)

if __name__ == '__main__':
    main()
