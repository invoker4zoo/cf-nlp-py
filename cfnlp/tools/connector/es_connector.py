# coding=utf-8
"""
@ license: Apache Licence
@ github: invoker4zoo
@ author: invoker/cc
@ wechart: whatshowlove
@ software: PyCharm
@ file: es_connector.py
@ time: $19-2-21 上午9:29
"""
import sys
sys.path.append('..')
from elasticsearch import Elasticsearch
from logger import logger

reload(sys)
sys.setdefaultencoding('utf-8')


class esConnector(object):
    def __init__(self, url, index, doc_type):
        """
        暂时没有分布式， url为单个链接
        :param url:
        Elasticsearch fun
        es.index
        """
        self.es = Elasticsearch([url])
        self.index = index
        self.doc_type = doc_type
        self.re_connect = 3

    def search_all(self, size=1000):
        """
        可复写此方法
        查询示例
        :return:
        """
        try:
            dsl_query = {
                'query':{
                    'match_all':{}
                },
                'size':size
            }
            result = self.es.search(self.index, self.doc_type, body=dsl_query)
            return result
        except Exception, e:
            logger.error('search all doc failed for %s' % str(e))
            return None

    def search_doc_by_id(self, id):
        """
        可复写此方法
        查询示例
        search doc by id
        :param id:
        :return:
        """
        try:
            dsl_query = {
                'query': {
                    'match': {
                        '_id': id
                    }
                }
            }
            result = self.es.search(self.index, self.doc_type, body=dsl_query)
            if len(result.get('hits', {}).get('hits', [])):
                return result.get('hits', {}).get('hits', [])[0]
            else:
                return []
        except Exception, e:
            logger.error('search doc by id failed for %s' % str(e))
            return None

    def insert_single_info(self, info):
        """
        可复写此方法
        查询示例
        :param info:
        :return:
        """
        try:
            result = self.es.index(self.index, self.doc_type, body=info)
            return result
        except Exception, e:
            logger.error('insert single info failed for %s' % str(e))
            return None

    def check_info_exist(self, title):
        """
        可复写此方法
        查询示例
        由于为对插入操作指定id，需要使用title查询文件信息是否存在
        :param title:
        :return:
        """
        try:

            # elasticsearch中的字符串精确匹配
            # 参考 https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html
            dsl_query = {
                'query': {
                    'match_phrase': {
                        'title': title
                    }
                }
            }
            result = self.es.search(self.index, self.doc_type, body=dsl_query)

            if len(result.get('hits', {}).get('hits', [])):
                return True
            else:
                return False
        except Exception, e:
            logger.error('check info existed failed for %s' % str(e))
            return None



if __name__ == '__main__':
    es_db = esConnector(url='localhost:9200', index='test', doc_type='finace')
