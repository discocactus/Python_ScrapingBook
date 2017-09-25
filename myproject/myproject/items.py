# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyprojectItem(scrapy.Item):
    # このクラスは削除しても構わない
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Headline(scrapy.Item):
    """
    ニュースのヘッドラインを表すItem
    """

    title = scrapy.Field()
    body = scrapy.Field()


class Restaurant(scrapy.Item):
    """
    食べログのレストラン情報
    """

    name = scrapy.Field()
    address = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    station = scrapy.Field()
    score = scrapy.Field()


class Page(scrapy.Item):
    """
    Webページ
    """

    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

    def __repl__(self):
        """
        ログへの出力時に長くなり過ぎないよう、contentを省略する
        """

        p = Page(self) # このPageを複製したPageを得る
        if len(p['content']) > 100:
            p['content'] = p['content'][:100] + '...' # 100文字より長い場合は省略する

        return super(Page, p).__repl__() # 複製したPageのもj列表現を返す
