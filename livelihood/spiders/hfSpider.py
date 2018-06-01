# -*- coding: utf-8 -*-
import scrapy
import random
import logging
import urllib
from scrapy.spiders import Spider
from livelihood.items import Hf12345Item
from livelihood.constants import *

import re

class Hf12345Spider(Spider):
    name = 'hf12345'
    allowed_domains = ['hf12345.gov.cn']
    start_urls = ['http://www.hf12345.gov.cn/public/mhwz/xjxdList']
    detail_url = 'http://www.hf12345.gov.cn/public/mhwz/todetail'

    def parse(self, response):
        cards = response.xpath('//div[@id="new_html"]/table[@class="xjxd_tab"]/tr[@class="bgcol"]')
        pattern = re.compile(r"'(\w+)','(\w+)','(\w+)'")
        item = Hf12345Item()
        nexPage = 1
        if len(cards) > 1:
            for card in cards:
                detailIds = card.xpath('./td[1]/a/@onclick').extract()
                if (detailIds is None) or (len(detailIds) == 0):
                    logging.debug('ignore data:%s' % card)
                    continue
                results = pattern.search(detailIds[0])
                if (len(results.groups()) != 3):
                    logging.debug('ignore data:%s' % card)
                    continue
                item['cardId'] = results.group(1)
                item['isSearchPassWord'] = results.group(2)
                item['tag'] = results.group(3)
                item['title'] = card.xpath('./td[2]/a/text()').extract()[0]
                item['source'] = card.xpath('./td[3]/text()').extract()[0].strip()
                item['reply'] = card.xpath('./td[4]/text()').extract()[0]
                item['hotCount'] = card.xpath('./td[5]/text()').extract()[0]
                datas = card.xpath('./td[6]/text()').extract()
                if len(datas) > 0:
                    item['replyDate'] = datas[0]

                headers = dict({'Content-Type':'application/x-www-form-urlencoded'})
                body = {KEY_REQUEST_HF_ID:item['cardId'], KEY_REQUEST_HF_ISSEARCHPASSWORD:item['isSearchPassWord'],
                        KEY_REQUEST_HF_TAG:item['tag'], KEY_REQUEST_HF_SYS_RANDOM: random.random()}
                body = urllib.urlencode(body)
                yield scrapy.Request(self.detail_url, callback=self.parse_detail, method='POST', meta={'item':item},
                                     headers=headers, body=body)

            curPage = response.xpath('//form[@name="form1"]//span[@class="gotopage"]/input/@value').extract()[0].strip()
            nexPage = int(curPage) + 1
            headers = dict({'Content-Type': 'application/x-www-form-urlencoded'})
            body = {'curPage': str(nexPage)}
            body = urllib.urlencode(body)
            logging.debug('采集下一页数据，curPage:%s' % str(curPage))
            yield scrapy.Request(self.start_urls[0], method='POST', callback=self.parse ,headers=headers, body=body)
        else:
            logging.warn('采集结束！！totalPage:%s' % nexPage)

    def parse_detail(self, response):
        item = response.meta['item']
        nodes = response.xpath('//table[@class="xjxx_tab"]')
        item['type'] = nodes.xpath('.//tr[2]/td[1]/label/text()').extract()[0]
        item['createTime'] = nodes.xpath('./tr[2]/td[2]/label/text()').extract()[0]
        item['content'] = nodes.xpath('./tr[3]/td[1]/label/text()').extract()[0]
        item['replyContent'] = nodes.xpath('./tr[5]/td[1]/label/text()').extract()[0].strip()
        #print 'item:', item
        yield item