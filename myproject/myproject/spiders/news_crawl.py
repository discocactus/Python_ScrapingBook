from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from myproject.items import Headline # ItemのHeadlineクラスをインポート


class NewsCrawlSpider(CrawlSpider):
    name = 'news_crawl' # Spiderの名前
    # クロール対象とするドメインのリスト
    allowed_domains = ['news.yahoo.co.jp']
    # クロールを開始するURLのリスト
    # 1要素のタプルの末尾にはカンマが必要
    start_urls = (
        'http://news.yahoo.co.jp/',
    )

    # リンクをたどるためのルールのリスト
    rules = (
        # トピックスのページへのリンクをたどり、レスポンスをparse_topics()メソッドで処理する
        Rule(LinkExtractor(allow=r'/pickup/\d+$'), callback='parse_topics'),
    )

    def parse_topics(self, response):
        """
        トピックスのページからタイトルと本文を抜き出す
        """
        item = Headline() # Headlineオブジェクトを作成
        item['title'] = response.css('.newsTitle ::text').extract_first() # タイトル
        item['body'] = response.css('.hbody').xpath('string()').extract_first() # 本文
        yield item # Itemをyieldして、データを抽出する
