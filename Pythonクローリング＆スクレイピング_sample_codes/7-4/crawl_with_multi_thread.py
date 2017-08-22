import sys
from concurrent.futures import ThreadPoolExecutor

import feedparser
import requests
from bs4 import BeautifulSoup


def main():
    # 人気エントリーのRSSからURLのリストを取得する。
    d = feedparser.parse('http://b.hatena.ne.jp/hotentry.rss')
    urls = [entry.link for entry in d.entries]

    # 最大3スレッドで並行処理するためのExecutorオブジェクトを作成。
    executer = ThreadPoolExecutor(max_workers=3)
    # Futureオブジェクトを格納しておくためのリスト。
    futures = []
    for url in urls:
        # 関数の実行をスケジューリングし、Futureオブジェクトを得る。
        # submit()の第2引数以降はfetch_and_scrape()関数の引数として渡される。
        future = executer.submit(fetch_and_scrape, url)
        futures.append(future)

    for future in futures:
        # Futureオブジェクトから結果（関数の戻り値）を取得して表示する。
        print(future.result())


def fetch_and_scrape(url):
    """
    引数で指定したURLのページを取得して、URLとタイトルを含むdictを返す。
    """

    print('Start downloading', url, file=sys.stderr)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    return {
        'url': url,
        'title': soup.title.text.strip(),
    }

if __name__ == '__main__':
    main()
