# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from cgi import log

from dingtalkchatbot.chatbot import DingtalkChatbot
import datetime
import pymysql
from scrapy.exceptions import DropItem

def dbHandle(self):
    self.conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        passwd='123456',
        charset='utf8',
        use_unicode=False
    )
    self.cursor = self.connect.cursor();


class MytestPipeline(object):
    #建立数据库
    def __init__(self):
        # 建立连接
        self.conn = pymysql.connect('127.0.0.1', 'root', '123456', 'joke')  # 有中文要存入数据库的话要加charset='utf8'
        self.cursor = self.conn.cursor()
        self.testItem=set()


    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=7604b5f3729b17430beaba515f404d1a906d92202c4ee476b11a9575690f9635'

    def send_dingtalk_text(self, webhook, msg, is_at_all=False):
        dingtalk = DingtalkChatbot(webhook)
        dingtalk.send_text(msg, is_at_all=is_at_all)


    def process_item(self, Item, spider):
        #数据去重
        title = Item['链接']
        if title in self.testItem:
            raise DropItem('{}已存在'.format(title))
        self.testItem.add(title)
        now_time = datetime.datetime.now().strftime('%Y-%m-%d')+ "\n"
        content = json.dumps(dict(Item), indent=1,ensure_ascii=False) + "\n"
        self.file.write(content.encode("utf-8"))
        self.send_dingtalk_text(self.webhook, '2345技术员论坛：'+'\n'+'当前时间： '+ now_time+ content, True)
    #数据插入到数据库
        insert_sql = """
                insert into t_baike(标题,链接,内容,发帖时间) value(%s,%s,%s,%s)
                """
        # 执行插入数据到数据库操作
        self.cursor.execute(insert_sql, (Item['标题'], Item['链接'], Item['内容'], Item['发帖时间']))
        self.conn.commit()
    #写入数据
    def open_spider(self,spider):
        self.file=open("a.txt","wb")

    def close_spider(self,close_spider):
        self.file.close()