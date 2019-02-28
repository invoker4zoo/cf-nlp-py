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
        :param jar_path:
        :param user_dic_path: format -> user_dic_name=user_dic_path
        :return:
        """
        # auto finding jvm path
        jvm_path = get_default_jvm_path()
        # jpype.startJVM(jvm_path, '-Djava.class.path=' + jar_path)
        # increase jvm heap memory
        jpype.startJVM(jvm_path, '-Djava.class.path=' + jar_path, '-Xms512M', '-Xmx2048M', '-XX:PermSize=64m',
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
        self.loc_api = JClass('com.zy.alg.JarExecution.AnsjSegPython')
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
                info_dict = {
                    'name': list(info)[0],
                    'nature': list(info)[1]
                }
                result_list.append(info_dict)
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
                info_dict = {
                    'name': list(info)[0],
                    'nature': list(info)[1]
                }
                result_list.append(info_dict)
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
                    info_dict = {
                        'name': list(info)[0],
                        'nature': list(info)[1]
                    }
                    result_list.append(info_dict)
            elif len(dict_key) == 2:
                result = [list(k) for k in list(self.ansj_api.textTokenizerUser(self.ansj_model, text, type,
                                                                                self.user_dic[dict_key.values()[0]],
                                                                                self.user_dic[dict_key.values()[1]]))]
                for info in result:
                    info_dict = {
                        'name': list(info)[0],
                        'nature': list(info)[1]
                    }
                    result_list.append(info_dict)
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
                    info_dict = {
                        'name': list(info)[0],
                        'nature': list(info)[1]
                    }
                    result_list.append(info_dict)
            elif len(dict_key) == 2:
                result = [list(k) for k in list(self.ansj_api.textTokenizerUserStop(self.ansj_model, text, type,
                                                                                    self.user_dic[dict_key.values()[0]],
                                                                                    self.user_dic[
                                                                                        dict_key.values()[1]]))]
                for info in result:
                    info_dict = {
                        'name': list(info)[0],
                        'nature': list(info)[1]
                    }
                    result_list.append(info_dict)
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
            area = self.loc_api.getFormatArea(self.ansj_model, text)
            return area
        except Exception, e:
            logger.error('area extractiopn failed for %s' % str(e))
            return None
    #############__area_extra methods__end###################
