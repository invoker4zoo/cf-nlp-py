# coding=utf-8
"""
@ license: Apache Licence
@ github: invoker4zoo
@ author: invoker/cc
@ wechart: whatshowlove
@ software: PyCharm
@ file: mysql_connector.py
@ time: $19-2-21 上午10:12
"""

import pymysql.cursors
import sys
from cfnlp.tools.logger import logger

class mysqlConnector(object):

    def __init__(self, host, user, password, db, table):
        self.connector = pymysql.connect(host=host,
                                         user=user,
                                         password=password,
                                         db=db,
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor
                                         )
        self.db = db
        self.table = table

    def select_one_info(self, sql, sql_params):
        """
        可复写方法，查询一条数据
        :param sql: example:"select * from `table_name` limit %d"
        :param sql_params: (1000,)
        :return:
        """
        try:
            with self.connector.cursor() as cursor:
                cursor.execute(sql, sql_params)
                result = cursor.fetchone()
                return result
        except Exception, e:
            logger.error('select one info failed for %s' % str(e))
            return None

if __name__ == '__main__':
    mysql_db = mysqlConnector(host='127.0.0.1', user='root', password='123456', db='db_name', table='table_name')