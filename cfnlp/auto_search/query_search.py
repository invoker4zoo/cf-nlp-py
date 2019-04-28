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


class searchModel(object):

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
        responce = list()
        dsl_query = {
            "query": {
                "match": {
                    filed: {
                        "query": query
                    }
                }
            }
        }
        result = self.es.search(self.index, self.type, body=dsl_query)
        for item in result.get('hits').get('hits'):
            responce.append(item)
        return responce


if __name__ == '__main__':
    model = searchModel(ES_URL, DOCS_INDEX, DOCS_TYPE)
    model.search_by_filed("农业转型")
