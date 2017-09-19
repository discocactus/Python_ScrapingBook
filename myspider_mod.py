
# これはScrapyのWebサイト（https://scrapy.org/）に掲載されているサンプルコードにコメントを追加したもの
# ScrapingHub社のブログの構造の変更により，リスト6.1の`myspider.py`は投稿を1件も取得できなくなった
# ScrapyのWebサイトに掲載されているサンプルコードも変更されている
# ブログの構造の変化に合わせて'`myspider.py`の時点のサンプルコードから変更

import scrapy


class BlogSpider(scrapy.Spider):
    name = 'blogspider'  # Spiderの名前。
    # クロールを開始するURLのリスト。
    start_urls = ['https://blog.scrapinghub.com']

    def parse(self, response):
        """
        ページから投稿のタイトルをすべて抜き出し、ベージャーをたどる。
        """
        # ページから投稿のタイトルをすべて抜き出す。
        for title in response.css('h2.entry-title'):
            yield {'title': title.css('a ::text').extract_first()}

        # ページャーの次のページへのリンクを取得し、次のページがあればたどる。
        # 次のページもparse()メソッドで処理する。
        next_page = response.css('div.prev-post > a ::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)