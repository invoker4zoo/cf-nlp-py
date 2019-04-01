#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019-03-27 11:25
@Author  : zhangyu
@Contact : zhangycqupt@163.com
@File    : data_index_format.py
@Software: PyCharm
@Site    : https://github.com/zhangyuo
"""

from cfnlp.tools.logger import logger
import jieba.posseg
import thulac
from cfnlp.tools.jar_methods import NLPModel
import os
import re


class dataIndexFormate(object):

    def __init__(self, seg_model='ansj', model_path=None, unit=['元', '%']):
        """

        :param seg_model: 分词模型：jieba/thunlp/ansj
        :param model_path: 分词模型
        :param unit: 单位匹配字符 ['元', '%']
        """
        self.pattern = unit
        ####################
        self.seg_type = seg_model
        if seg_model == 'jieba':
            # self.seg_model = jieba
            self.seg_model = jieba.posseg
        elif seg_model == 'thunlp' and model_path != None:
            self.seg_model = thulac.thulac(seg_only=True, model_path=model_path)
        elif seg_model == 'ansj':
            # 由于ansj模型采用Jar包加载，由jar_methods统一初始化
            self.seg_model = model_path

    def extract_data(self, text):
        """
        提取文本中的数据指标。注意使用标点符号分割的句子作为输入文本。
        :param text:
        :return:
        """
        try:
            self.text = self._strQ2B(text)
            if self.seg_type == 'jieba':
                seg = self.seg_model.cut(text)
                # for term in seg:
                #     term = term
            elif self.seg_type == 'thunlp':
                seg = self.seg_model.cut(text)
            elif self.seg_type == 'ansj':
                seg = self.seg_model.text_tokenizer(text)

            return self._get_data(seg)
        except Exception, e:
            logger.error('extract data from text failed for %s' % str(e))
            return None

    ##################private_func#########################
    def _strQ2B(self, text):
        """
        全角转半角
        :param text:
        :return:
        """
        try:
            text = text.decode('utf-8')
            rstring = ''
            for char in text:
                inside_code = ord(char)
                if inside_code == 12288:
                    inside_code = 32
                elif inside_code >= 65281 and inside_code <= 65374:
                    inside_code -= 65248
                rstring += unichr(inside_code)
            return rstring
        except Exception, e:
            logger.error('text transaction failed for %s' % str(e))

    def _strB2Q(self, text):
        """
        半角转全角
        :param text:
        :return:
        """
        try:
            rstring = ''
            for char in text:
                inside_code = ord(char)
                if inside_code == 32:
                    inside_code = 12288
                elif inside_code >= 32 and inside_code <= 126:
                    inside_code += 65248
                rstring += unichr(inside_code)
            return rstring
        except Exception, e:
            logger.error('text transaction failed for %s' % str(e))

    def _get_data(self, seg):
        """
        提取具体类型数据
        :param seg:
        :return:
        """
        try:
            data_list = list()
            _begin = 0
            last_term = ''
            for _seg in seg:
                name = _seg[0]
                nature = _seg[1]
                index = text.index(name, _begin)
                des = self.text[0:index] + name
                des = des.split(';')[-1]
                _begin = index
                if True in [True if _ in name else False for _ in self.pattern]:
                    result = re.findall(ur'[\u4e00-\u9fa5]', name)
                    # 非中文字符判断
                    if len(result) == 0:
                        result = self.pattern
                    value = name
                    for char in result:
                        value = value.replace(char, '')
                    unit = name.replace(value, '')
                    # value/unit 是否分割判断
                    if value == '':
                        if last_term[1] == 'm' or last_term[1] == 'mq':
                            value = last_term[0]
                            unit = name
                    value = float(value)
                    if '下降' in des or '降低' in des:
                        value = - float(value)
                    data_body = {
                        'index': index,
                        'value': value,
                        'unit': unit,
                        'des': des
                    }
                    data_list.append(data_body)
                last_term = _seg

            return data_list
        except Exception, e:
            logger.error('get data failed for %s' % str(e))
            return None


if __name__ == '__main__':
    text = '2月份，全市完成一般公共预算收入208.3亿元，下降2.7%；完成一般公共预算支出195.8亿元，提高20.2%'

    model_path = os.path.abspath(os.path.dirname(os.getcwd()) + os.path.sep + '.') + '/stable/'
    nlp_model = NLPModel(model_path, model_path + 'jar-jpype-connector-1.0.jar')
    data_model = dataIndexFormate(seg_model='ansj', model_path=nlp_model, unit=['元', '%'])
    result_list = data_model.extract_data(text)

    # data_model = dataIndexFormate(seg_model='jieba')
    # result_list = data_model.extract_data(text)

    # model_path = '/User/zhangyu/model/'
    # data_model = dataIndexFormate(seg_model='thunlp', model_path=model_path)

    for result in result_list:
        print('index:%s\tvalue:%.2f\tunit:%s\tdes:%s'
              % (result['index'], result['value'], result['unit'], result['des']))
