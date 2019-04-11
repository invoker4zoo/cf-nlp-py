#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019/2/25 10:58
@Author  : Zhangyu
@Email   : zhangycqupt@163.com
@File    : jar_methods.py
@Software: PyCharm
@Github  : zhangyuo
"""
import os
import sys

import jpype
from jpype import *
from cfnlp.tools.logger import logger

reload(sys)
sys.setdefaultencoding('utf-8')


class NLPModel(object):
    def __init__(self, model_path, jar_path, **user_dic_path):
        """
        jar methods including: ansj, area extra
        :param model_path:
        :param jar_path: load multiple jar -> using ':' connection. such as name1.jar:name2.jar
        :param user_dic_path: format -> user_dic_name=user_dic_path
        :return:
        """
        # auto finding jvm path
        jvm_path = get_default_jvm_path()
        # jpype.startJVM(jvm_path, '-Djava.class.path=' + jar_path)
        # increase jvm heap memory
        jpype.startJVM(jvm_path, '-Djava.class.path=' + jar_path, '-Xms512M', '-Xmx2048m', '-XX:PermSize=64m',
                       '-XX:MaxPermSize=256m')
        # init ansj model
        self.ansj_api = JClass('com.zy.alg.JarExecution.AnsjSegPython')
        self.ansj_model = self.ansj_api.init()
        self.user_dic = dict()
        for k, v in user_dic_path.items():
            dic_path = v.repalce('..', '')
            dic_path = os.path.abspath(os.path.dirname(os.getcwd()) + os.path.sep + '.') + dic_path
            self.user_dic[k] = self.ansj_api.insertUserDic(dic_path)
        # init area model
        self.loc_api = JClass('com.zy.alg.JarExecution.LocationPython')
        self.area_model = self.loc_api.init(model_path)

    #############__ansj seg methods__start#################
    def text_tokenizer(self, text, type='1'):
        """
        ansj text tokenizer
        :param text: input text
        :param type: 1-ToAnalysis-distinct 2-ToAnalysis-not distinct 3-indexAnalysis 4-DicAnalysis
        :return:
        """
        try:
            result_list = list()
            result = [list(k) for k in list(self.ansj_api.textTokenizer(self.ansj_model, text, type))]
            for info in result:
                result_list.append(list(info))
            return result_list
        except Exception, e:
            logger.error('ansj seg failed for %s' % str(e))
            return None

    def text_tokenizer_stop(self, text, type='1'):
        """
        activate stop dictionary, ansj text tokenizer
        :param text: input text
        :param type: 1-ToAnalysis-distinct 2-ToAnalysis-not distinct 3-indexAnalysis 4-DicAnalysis
        :return:
        """
        try:
            result_list = list()
            result = [list(k) for k in list(self.ansj_api.textTokenizerStop(self.ansj_model, text, type))]
            for info in result:
                result_list.append(list(info))
            return result_list
        except Exception, e:
            logger.error('ansj seg failed for %s' % str(e))
            return None

    def text_tokenizer_user(self, text, type='1', **dict_key):
        """
        add uesr define dictionary, ansj text tokenizer. support adding two dictionary
        :param text: input text
        :param type: 1-ToAnalysis-distinct 2-ToAnalysis-not distinct 3-indexAnalysis 4-DicAnalysis
        :param dict_key: format -> define_parameter=user_dic_name
        :return:
        """
        try:
            result_list = list()
            if len(dict_key) == 1:
                result = [list(k) for k in list(self.ansj_api.textTokenizerUser(self.ansj_model, text, type,
                                                                                self.user_dic[dict_key.values()[0]]))]
                for info in result:
                    result_list.append(list(info))
            elif len(dict_key) == 2:
                result = [list(k) for k in list(self.ansj_api.textTokenizerUser(self.ansj_model, text, type,
                                                                                self.user_dic[dict_key.values()[0]],
                                                                                self.user_dic[dict_key.values()[1]]))]
                for info in result:
                    result_list.append(list(info))
            return result_list
        except Exception, e:
            logger.error('ansj seg failed for %s' % str(e))
            return None

    def text_tokenizer_user_stop(self, text, type='1', **dict_key):
        """
        add uesr define dictionary and activate stop dictionary, ansj text tokenizer. support adding two dictionary
        :param text: input text
        :param type: 1-ToAnalysis-distinct 2-ToAnalysis-not distinct 3-indexAnalysis 4-DicAnalysis
        :param dict_key: format -> define_parameter=user_dic_name
        :return:
        """
        try:
            result_list = list()
            if len(dict_key) == 1:
                result = [list(k) for k in list(self.ansj_api.textTokenizerUserStop(self.ansj_model, text, type,
                                                                                    self.user_dic[
                                                                                        dict_key.values()[0]]))]
                for info in result:

                    result_list.append(list(info))
            elif len(dict_key) == 2:
                result = [list(k) for k in list(self.ansj_api.textTokenizerUserStop(self.ansj_model, text, type,
                                                                                    self.user_dic[dict_key.values()[0]],
                                                                                    self.user_dic[
                                                                                        dict_key.values()[1]]))]
                for info in result:
                    result_list.append(list(info))
            return result_list
        except Exception, e:
            logger.error('ansj seg failed for %s' % str(e))
            return None

    #############__ansj seg methods__end###################

    #############__area_extra methods__start#################
    def get_format_area(self, text):
        """
        area extract
        :param text: input text
        :return: format -> province1&city1&area # province2&city2&area
        """
        try:
            area = self.loc_api.getFormatArea(self.area_model, text)
            return area
        except Exception, e:
            logger.error('area extractiopn failed for %s' % str(e))
            return None

    def area_extract(self, text):
        """
        area extract
        :param text: input text
        :return: json format
        """
        try:
            area = self.loc_api.areaExtract(self.area_model, text)
            if area == '':
                return None
            else:
                area_list = list()
                for k in area.split('#'):
                    _area = k.split('&')
                    province = None
                    abbr = None
                    city = None
                    dist = None
                    if len(_area) == 3:
                        province = _area[0].split('/')[0] + '/' + _area[0].split('/')[1]
                        abbr = _area[0].split('/')[2]
                        city = _area[1]
                        dist = _area[2]
                    elif len(_area) == 2:
                        province = _area[0].split('/')[0] + '/' + _area[0].split('/')[1]
                        abbr = _area[0].split('/')[2]
                        city = _area[1]
                    elif len(_area) == 1:
                        province = _area[0].split('/')[0] + '/' + _area[0].split('/')[1]
                        abbr = _area[0].split('/')[2]
                    area_list.append({"province": province,
                                      "city": city,
                                      "area": dist,
                                      "abbreviation": abbr})
                return area_list
        except Exception, e:
            logger.error('area extractiopn failed for %s' % str(e))
            return None
    #############__area_extra methods__end###################


if __name__ == '__main__':
    # area extract demo
    # model_path = os.path.abspath(os.path.dirname(os.getcwd()) + os.path.sep + '.') + '/stable/'
    # nlp_model = NLPModel(model_path, model_path + 'jar-jpype-connector-1.0.jar')
    # text = '重庆綦江是个好地方，渝中区，深圳是紧邻粤港澳大湾区'
    # # area = nlp_model.area_extract(text)
    # area = nlp_model.get_format_area(text)
    # print(area)

    # ansj
    model_path = os.path.abspath(os.path.dirname(os.getcwd()) + os.path.sep + '.') + '/stable/'
    nlp_model = NLPModel(model_path, model_path + 'jar-jpype-connector-1.0.jar')
    text = '红酒（Red wine）是葡萄酒的一种，并不一定特指红葡萄酒。红酒的成分相当简单，是经自然发酵酿造出来的果酒，' \
           '含有最多的是葡萄汁，葡萄酒有许多分类方式。还有2.7%和3.3亿元'
    terms = nlp_model.text_tokenizer(text)
    for term in terms:
        print('%s\t%s' % (term[0], term[1]))
