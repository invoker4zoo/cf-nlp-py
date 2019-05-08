#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019-04-21 22:06
@Author  : zhangyu
@Contact : zhangycqupt@163.com
@File    : query_search.py
@Software: PyCharm
@Site    : https://github.com/zhangyuo
"""

from elasticsearch import Elasticsearch
from cfnlp.auto_search.config.config import *


class dslModel(object):

    def __init__(self, url, index, type):
        """
        暂时没有分布式，单个服务器
        :param url:
        :param index:
        :param type:
        """
        self.es = Elasticsearch([url])
        self.index = index
        self.type = type
        self.re_connect = 3

    def search_by_filed(self, query, filed='title'):
        """
        根据文档字段查询
        :param query:
        :param filed: 文档字段
        :return:
        """
        response = list()
        dsl_query = {
            'query': {
                'match': {
                    filed: query
                }
            }
        }
        result = self.es.search(self.index, body=dsl_query)
        for item in result.get('hits').get('hits'):
            response.append(item)
        return response


def print_doc(response):
    """
    打印响应结果
    :param response:
    :return:
    """
    for i, item in enumerate(response):
        info = item.get('_source', '')
        title = info.get('title', '')
        print ('%d#%s' % (i, title))


if __name__ == '__main__':
    model = dslModel(ES_URL, DOCS_INDEX, DOCS_TYPE)
    response = model.search_by_filed("农业")
    print_doc(response)
