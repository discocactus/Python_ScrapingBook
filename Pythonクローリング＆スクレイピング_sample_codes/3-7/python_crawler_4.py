import requests
import lxml.html


def main():
    session = requests.Session()  # 複数のページをクロールするのでSessionを使う。
    response = session.get('https://gihyo.jp/dp')
    urls = scrape_list_page(response)
    for url in urls:
        response = session.get(url)  # Sessionを使って詳細ページを取得する。
        ebook = scrape_detail_page(response)  # 詳細ページからスクレイピングして電子書籍の情報を得る。
        print(ebook)  # 電子書籍の情報を表示する。
        break  # まず1ページだけで試すため、break文でループを抜ける。


def scrape_list_page(response):
    root = lxml.html.fromstring(response.content)
    root.make_links_absolute(response.url)

    for a in root.cssselect('#listBook a[itemprop="url"]'):
        url = a.get('href')
        yield url


def scrape_detail_page(response):
    """
    詳細ページのResponseから電子書籍の情報をdictで取得する。
    """
    root = lxml.html.fromstring(response.content)
    ebook = {
        'url': response.url,  # URL
        'title': root.cssselect('#bookTitle')[0].text_content(),  # タイトル
        'price': root.cssselect('.buy')[0].text,  # 価格（.textで直接の子である文字列のみを取得）
        'content': [h3.text_content() for h3 in root.cssselect('#content > h3')],  # 目次
    }
    return ebook  # dictを返す。

if __name__ == '__main__':
    main()
