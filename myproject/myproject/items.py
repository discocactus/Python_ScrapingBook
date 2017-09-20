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