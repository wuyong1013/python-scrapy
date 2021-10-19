# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MytestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #movieName = scrapy.Field()
    #movieRate = scrapy.Field()
    name = scrapy.Field()
    Url = scrapy.Field()
    content = scrapy.Field()
    title = scrapy.Field()

class NovelItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

class MovieItem(scrapy.Item):
    name = scrapy.Field()
    date = scrapy.Field()
    haibao = scrapy.Field()
    info = scrapy.Field()
    zhongzi = scrapy.Field()