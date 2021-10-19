# -*- coding: utf-8 -*-
import scrapy
# 引入自定义的items
#from myTest.items import MytestItem
import re
import json
import time
import datetime
import configparser

class MytestItem(scrapy.Item):
    标题 = scrapy.Field()
    链接 = scrapy.Field()
    内容 = scrapy.Field()
    发帖时间 = scrapy.Field()


# 继承scrapy.Spider
class CookSpider(scrapy.Spider):
    # 爬虫名
    name = 'cook_spider'
    # 允许的域名
    allowed_domains = ['wangpai.2345.cn']
    # 入口url 扔到调度器里面去
    start_urls = ['http://wangpai.2345.cn/forumdisplay.php?fid=12&tid=0&act=middle_show&order_select=dateline&isPith=0']

    def parse(self, response):
        #提取页面关键字
        #keywords = ['QQ','蓝屏','崩溃','黑屏']
        #提取页面节点
        movieList = response.xpath('//tr[@class="list_tr"]/th/strong/a')
        for item in movieList:
            testItem = MytestItem()
            testItem["标题"] = item.xpath('text()').extract_first()
            testItem['链接'] = item.xpath('@href').extract_first()
            #for word in keywords:
                #if word in testItem["name"]:
            yield scrapy.Request(url=testItem['链接'],callback=self.parse_next,meta={"testItem":testItem})
            #print(movieList)
                    #break

#提取二级页面内容、标题、链接
    def parse_next(self, response):
        testItem=  response.meta["testItem"]
        data = response.xpath('//*[@id="top_lou"]/div[@class="article"]//div/text()').extract()
        #print(data)
        raw_data = "".join(data)
        #正则表达式
        dr = re.compile(r'<[^>]+>', re.S)
        dd = dr.sub('', raw_data)
        testItem['内容'] = dd.strip().replace('\xa0', '').replace('\u3000', '').replace('\r\n', '').replace('\t', '')

        #提取帖子时间(获取帖子时间)
        data_time=response.xpath('//*[@id="top_lou"]/div[@class="article"]//div[@class="floor"]/em/text()').extract()
        #print(data_time)
        raw_data_time="".join(data_time)
        ds = re.compile(r'<[^>]+>', re.S)
        dt = ds.sub('', raw_data_time)
        testItem['发帖时间'] = dt.strip().replace('\t', '').replace('\r\n', '')[0:10]
        #关键字
        cf = configparser.ConfigParser()
        cf.read("C:\python-scrapy-master\myTest\spiders\config.ini")  # 读取配置文件，如果写文件的绝对路径，就可以不用os模块
        secs = cf.sections()
        options = cf.get("Test","keywords_content")
        #keywords_content = ['黑屏','蓝屏','卡','崩溃','2345','消失']
        #print(options)
        for words_content in options:
            #获取当前系统时间
            now_time = datetime.datetime.now().strftime('%Y-%m-%d')
            #判断帖子时间是当前最新时间
            if words_content in testItem['内容'] and  now_time in testItem['发帖时间']:
                yield testItem
                #break
                #print (testItem)
                #yield testItem




