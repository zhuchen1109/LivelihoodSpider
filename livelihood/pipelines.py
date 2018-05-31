# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import MySQLdb
from settings import MYSQL

class HfPipeline(object):
    def __init__(self):
        host = MYSQL.get('HOST')
        port = MYSQL.get('PORT')
        user = MYSQL.get('USER')
        psw = MYSQL.get('PASSWORD')
        name = MYSQL.get('DB')
        self.sqlTable = MYSQL.get('TABLE')
        self.mysqlConn = MySQLdb.connect(host=host, port=port, user=user, passwd=psw, db=name, charset='utf8')


    def process_item(self, item, spider):
        try:
            cursor = self.mysqlConn.cursor()
            sql = 'insert into '+self.sqlTable+' (cardId, title, type, source, reply, hotCount, replyDate, ' \
                    'isSearchPassWord, tag, createTime, content, replyContent) values ' \
                    '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(sql, [item['cardId'], item['title'], item.getType(), item['source'],
                           item['reply'], item.getHotCount(), item['replyDate'], item['isSearchPassWord'], item['tag'],
                           item['createTime'], item['content'], item['replyContent']])
            self.mysqlConn.commit()
            cursor.close()
        except Exception as e:
            logging.error('保存数据库出错:%s,item:%s' % (e, item))
        return item

    def close_spider(self, spider):
        self.mysqlConn.close()
