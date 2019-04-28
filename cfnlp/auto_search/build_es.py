#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019-04-15 15:56
@Author  : zhangyu
@Contact : zhangycqupt@163.com
@File    : build_es.py
@Software: PyCharm
@Site    : https://github.com/zhangyuo
"""

from cfnlp.auto_search.config.config import *
import subprocess
from cfnlp.tools.logger import logger
import requests


def create_index(index):
    """
    构建es索引
    :return:
    """
    index = DOCS_INDEX
    command = "curl -XPUT %s/%s " % (ES_URL, index)
    p = subprocess.Popen(command, shell=True)
    p.wait()
    logger.info("build es index success.")


def delete_index(index):
    """
    删除es索引
    :param index:
    :return:
    """
    command = "curl -XDELETE %s/%s " % (ES_URL, index)
    p = subprocess.Popen(command, shell=True)
    p.wait()
    logger.info("delete es index success.")


def insert_data(index, type, id, json):
    """
    插入数据-post方式(实质修改数据)
    :param index: es索引
    :param type: es索引的type
    :param id: es类型的id
    :param json: json数据
    :return:
    """
    # 法一：
    url = 'http://%s/%s/%s/%s' % (ES_URL, index, type, id)
    responce = requests.post(url, json=json)
    # 法二：
    # str_json = '{\n'
    # for k, v in json.items():
    #     str_json += '\"%s\":\"%s\",' % (k, v)
    # str_json = str_json[0:-1] + '\n}'
    # command = u"curl -H 'Content-Type: application/json' -X POST %s/%s/%s/%s -d @- <<CURL_DATA\n%s\nCURL_DATA" \
    #           % (ES_URL, index, type, id, str_json)
    # p = subprocess.Popen(command, shell=True)
    # p.wait()
    logger.info("insert data ok")


def set_mappings(index, rep_num):
    """
    已存在索引时，只能修改副本数量
    :param index: es索引
    :param rep_num: 副本数量
    :return:
    """
    url = 'http://%s/%s/_settings' % (ES_URL, index)
    responce = requests.put(url, 2)


def set_settings():
    pass


if __name__ == '__main__':
    # delete_index(DOCS_INDEX)
    # create_index(DOCS_INDEX)
    json = {"name": "zhangyuo"}
    insert_data(DOCS_INDEX, DOCS_TYPE, '1', json)
