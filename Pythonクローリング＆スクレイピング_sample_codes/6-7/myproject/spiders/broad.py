import scrapy

from myproject.items import Page
from myproject.utils import get_content


class BroadSpider(scrapy.Spider):
    name = "broad"
    start_urls = (
        # はてなブックマークの新着エントリーページ。
        'http://b.hatena.ne.jp/entrylist',
    )

    def parse(self, response):
        """
        はてなブックマークの新着エントリーページをパースする。
        """

        # 個別のWebページへのリンクをたどる。
        for url in response.css('a.entry-link::attr("href")').extract():
            # parse_page() メソッドをコールバック関数として指定する。
            yield scrapy.Request(url, callback=self.parse_page)

        # of=の値が2桁である間のみ「次の20件」のリンクをたどる（最大5ページ目まで）。
        url_more = response.css('a::attr("href")').re_first(r'.*\?of=\d{2}$')
        if url_more:
            # url_moreの値は /entrylist で始まる相対URLなので、
            # response.urljoin()メソッドを使って絶対URLに変換する。
            # コールバック関数を指定していないので、レスポンスはデフォルト値である
            # parse()メソッドで処理される。
            yield scrapy.Request(response.urljoin(url_more))

    def parse_page(self, response):
        """
        個別のWebページをパースする。
        """

        # utils.pyに定義したget_content()関数でタイトルと本文を抽出する。
        title, content = get_content(response.text)
        # Pageオブジェクトを作成してyieldする。
        yield Page(url=response.url, title=title, content=content)
