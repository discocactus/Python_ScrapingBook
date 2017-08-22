from scrapy.spiders import SitemapSpider


class WiredjpSpider(SitemapSpider):
    name = "wiredjp"
    allowed_domains = ["wired.jp"]

    # XMLサイトマップのURLのリスト。
    # robots.txtのURLを指定すると、SitemapディレクティブからXMLサイトマップのURLを取得する。
    sitemap_urls = [
        'http://wired.jp/robots.txt',
    ]
    # サイトマップインデックスからたどるサイトマップURLの正規表現のリスト。
    # このリストの正規表現にマッチするURLのサイトマップのみをたどる。
    # sitemap_followを指定しない場合は、すべてのサイトマップをたどる。
    sitemap_follow = [
        r'post-2015-',
    ]
    # サイトマップに含まれるURLを処理するコールバック関数を指定するルールのリスト。
    # ルールは (正規表現, 正規表現にマッチするURLを処理するコールバック関数) という2要素のタプルで指定する。
    # sitemap_rulesを指定しない場合はすべてのURLのコールバック関数はparseメソッドとなる。
    sitemap_rules = [
        (r'/2015/\d\d/\d\d/', 'parse_post'),
    ]

    def parse_post(self, response):
        # 詳細ページから投稿のタイトルを抜き出す。
        yield {
            'title': response.css('h1.post-title::text').extract_first(),
        }
