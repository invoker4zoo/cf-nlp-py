#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019-04-15 15:49
@Author  : zhangyu
@Contact : zhangycqupt@163.com
@File    : data_process.py
@Software: PyCharm
@Site    : https://github.com/zhangyuo
"""

from cfnlp.auto_search.config.config import *
from cfnlp.tools.connector.mongo_connector import mongoConnector
from cfnlp.auto_search.build_es import create_index, delete_index, insert_data
from cfnlp.tools.logger import logger
from bs4 import BeautifulSoup
from cfnlp.tools.date_format import dateFormate


class docsTrans(object):
    """
    mongo数据库读取文件，并构建索引存入es
    """

    def __init__(self, index, type):
        self.index = index
        self.type = type
        self.db = mongoConnector(MONGODB_SERVER, MONGODB_PORT, MONGODB_DB, MONGODB_COLLECTION)
        delete_index(index)
        create_index(index)
        self.date_model = dateFormate('../stable/date_format.json')

    def load_docs(self):
        num = 0
        try:
            for i in self.db.collection.find():
                if i.get('_id', ''):
                    num += 1
                    id = i['_id']
                    json = {
                        "content_txt": i.get('content_txt', ''),
                        "createTime": str(i.get('createTime', '')),
                        "effect": i.get('effect', '').strip(),
                        "fileCategory0": i.get('fileCategory0', ''),
                        "fileCategory1": i.get('fileCategory1', ''),
                        "fileCategory2": i.get('fileCategory2', ''),
                        "fileCategory3": i.get('fileCategory3', ''),
                        "fileDepart": i.get('fileDepart', ''),
                        "fileLayer0": i.get('fileLayer0', ''),
                        "keyword": i.get('keyword', ''),
                        "pubTime": i.get('pubTime', ''),
                        "source_url": i.get('source_url', ''),
                        "title": i.get('title', ''),
                        "titleNum": i.get('titleNum', '')
                    }
                    insert_data(self.index, self.type, id, json)
                    logger.info('insert data: %d' % num)
            logger.info('insert data finished.')
        except Exception, e:
            logger.error('insert data failed in %d item for %s' % (num, str(e)))

    def _clean_content(self, content):
        """
        清洗content中的html标签
        :param content:
        :return:
        """
        try:
            trans_content = ''
            content_soup = BeautifulSoup(content, 'html5lib')
            for str in content_soup.strings:
                if len(str.strip()):
                    trans_content += str.strip() + '\n'
                else:
                    pass
            return trans_content
        except Exception, e:
            logger.error('clean content html tag failed for %s' % str(e))
            return ''


if __name__ == '__main__':
    process = docsTrans(DOCS_INDEX, DOCS_TYPE)
    process.load_docs()
