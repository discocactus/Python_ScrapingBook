import sys
import asyncio

import aiohttp
import feedparser
from bs4 import BeautifulSoup

# 最大同時ダウンロード数を3に制限するためのセマフォを作成。
semaphore = asyncio.Semaphore(3)


async def main():
    # 人気エントリーのRSSからURLのリストを取得する。
    d = feedparser.parse('http://b.hatena.ne.jp/hotentry.rss')
    urls = [entry.link for entry in d.entries]

    # セッションオブジェクトを作成。
    with aiohttp.ClientSession() as session:
        # URLのリストに対応するコルーチンのリストを作成。
        coroutines = []
        for url in urls:
            coroutine = fetch_and_scrape(session, url)
            coroutines.append(coroutine)

        # コルーチンを完了した順に返す。
        for coroutine in asyncio.as_completed(coroutines):
            # コルーチンの結果を表示する。
            print(await coroutine)


async def fetch_and_scrape(session, url):
    """
    引数で指定したURLのページを取得して、URLとタイトルを含むdictを返す。
    """

    # セマフォでロックを獲得できるまで待つ。
    with await semaphore:
        print('Start downloading', url, file=sys.stderr)

        # 非同期にリクエストを送り、レスポンスヘッダを取得する。
        response = await session.get(url)
        # レスポンスボディを非同期に取得する。
        soup = BeautifulSoup(await response.read(), 'lxml')

        return {
            'url': url,
            'title': soup.title.text.strip(),
        }

if __name__ == '__main__':
    # イベントループを取得。
    loop = asyncio.get_event_loop()
    # イベントループでmain()を実行し、完了するまで待つ。
    loop.run_until_complete(main())
