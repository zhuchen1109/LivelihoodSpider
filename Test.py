#coding=utf-8

import json
import logging
import MySQLdb
from livelihood.settings import MYSQL

def main():
    str = '{"replyContent": "经高新区回复，计划2019年秋季（9月）开学，学区暂未划分。", "title": "合肥高新区彩虹中学学区", "content": "彩虹中学什么时间招生？哪些小区会是其学区的？", "source": "门户网站", "replyDate": "2018-05-31", "tag": "c1f14d0251425c", "cardId": "18052888080007", "isSearchPassWord": "b6925d002642480001", "reply": "高新技术产业开发区", "type": "咨询", "createTime": "2018-05-27 20:34:12", "hotCount": "31"}'
    item = json.loads(str, encoding='utf-8')
    host = MYSQL.get('HOST')
    port = MYSQL.get('PORT')
    user = MYSQL.get('USER')
    psw = MYSQL.get('PASSWORD')
    name = MYSQL.get('DB')
    sqlTable = MYSQL.get('TABLE')
    mysqlConn = MySQLdb.connect(host=host, port=port, user=user, passwd=psw, db=name, charset='utf8')
    try:
        cursor = mysqlConn.cursor()
        sql = 'insert into '+sqlTable+' (cardId, title, type, source, reply, hotCount, replyDate, isSearchPassWord, ' \
              'tag, createTime, content, replyContent) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(sql, [item['cardId'], item['title'], 1, item['source'],
                             item['reply'], 11, item['replyDate'], item['isSearchPassWord'], item['tag'],
                             item['createTime'], item['content'], item['replyContent']])
        mysqlConn.commit()
        cursor.close()
    except Exception as e:
        logging.error('保存数据库出错:%s,item:%s' % (e, item))

if __name__ == '__main__':
    main()