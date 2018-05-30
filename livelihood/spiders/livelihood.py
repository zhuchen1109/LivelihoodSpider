# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider

import re

class Hf12345Spider(Spider):
    name = 'hf12345'
    allowed_domains = ['hf12345.gov.cn']
    start_urls = ['http://www.hf12345.gov.cn/public/mhwz/xjxdList']

    def parse(self, response):
        cards = response.xpath('//div[@id="new_html"]/table[@class="xjxd_tab"]/tr[@class="bgcol"]')
        #print 'cards', cards
        for card in cards:
            print type(card)
            print card
            ids = card.xpath('./td[1]/a/@onclick').extract()
            # # 信件编号
            # cardId = models.CharField(primary_key=True, max_length=30)
            # # 信件标题
            # title = models.CharField(default='', max_length=100)
            # # 信件类型
            # type = models.SmallIntegerField(default=0)
            # # 信件来源
            # source = models.CharField(default='', max_length=30)
            # # 答复单位
            # reply = models.CharField(default='', max_length=30)
            # # 人气
            # hotCount = models.IntegerField(default=0)
            # # 回复时间
            # replyDate = models.DateTimeField()
            # # 请求参数
            # isSearchPassWord = models.CharField(default='', max_length=40)
            # # 请求参数
            # tag = models.CharField(default='', max_length=40)
            # # 来信时间
            # createTime = models.DateTimeField()
            # # 信件内容
            # content = models.TextField(default='')
            # # 回复内容
            # replyContent = models.TextField(default='')
            print 'id:', id