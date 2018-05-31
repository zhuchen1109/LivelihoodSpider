# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item

class Hf12345Item(Item):

    # 信件编号
    cardId = Field()
    # 信件标题
    title = Field()
    # 信件类型 咨询：1 建议：2
    type = Field()
    # 信件来源
    source = Field()
    # 答复单位
    reply = Field()
    # 人气
    hotCount = Field()
    # 回复时间
    replyDate = Field()
    # 请求参数
    isSearchPassWord = Field()
    # 请求参数
    tag = Field()
    # 来信时间
    createTime = Field()
    # 信件内容
    content = Field()
    # 回复内容
    replyContent = Field()

    def getType(self):
        type = 0
        if self['type'] == '咨询':
            type = 1
        elif self['type'] == '建议':
            type = 2
        return type

    def getHotCount(self):
        hot = -1;
        try:
            hot = int(self['hotCount'])
        except:
            pass
        return hot

    def __str__(self):
        return 'id:%s,title:%s' % (self['cardId'], self['title'])