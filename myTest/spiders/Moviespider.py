# -*- coding: utf-8 -*-
import scrapy
from myTest.items import MovieItem

class MoviespiderSpider(scrapy.Spider):
    name = 'moviespider'
    allowed_domains = ['dytt8.net']
    start_urls = ['http://www.dytt8.net/html/gndy/dyzz/']

    def parse(self, response):
        # print(response.text)
        movie_list = response.xpath("//div[@class='co_content8']//table")
        for movie in movie_list:
            item = MovieItem()
            item["name"] = movie.xpath(".//a[@class='ulink']/text()").extract_first()
            item["date"] = movie.xpath(".//font[@color='#8F8C89']/text()").extract_first().split("\r")[0]

            # 获取二级页面的url
            next_url = "http://www.dytt8.net" + movie.xpath(".//a[@class='ulink']/@href").extract_first()

            yield scrapy.Request(url=next_url,callback=self.parse_next,meta={"item":item})
            # meta是response的一个成员变量，加入meta以后可以通过meta把额外一些内容添加到response中

    # 定义一个函数用于解析二级页面
    def parse_next(self,response):
        item = response.meta["item"]
        # print(item)
        item["haibao"] = response.xpath("//div[@id='Zoom']//img[1]/@src").extract_first()
        item["info"] = r"\n".join(response.xpath("//div[@id='Zoom']//p[1]/text()").extract())
        item["zhongzi"] = response.xpath("//div[@id='Zoom']//td[@bgcolor='#fdfddf']//a/@href").extract_first()
        yield item