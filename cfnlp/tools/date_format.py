#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2018/9/5 9:20
@Author  : Zhangyu
@Email   : zhangycqupt@163.com
@File    : date_format.py
@Software: PyCharm
@Github  : zhangyuo
"""

import re
import json
from cfnlp.tools.logger import logger


class dateFormate(object):
    def __init__(self, date_path):
        """
        日期提取初始化
        :param date_path: 日期模型路径
        """
        self.nlp_date_madel = load_date_model(date_path)
        # 年、月、日
        # 2016/12/12 or 2016-12-12 or 2018 12 12 or 2011.11.5
        self.pattern_ymr1 = re.compile(u'(\d{2,4}[- /.]\d{1,2}[- /.]\d{1,2})')
        # self.pattern_ymr1 = re.compile(u'(\d不要)')
        # 2016年12月12日
        self.pattern_ymr2 = re.compile(u'(\d{2,4}年\d{1,2}月\d{1,2}日)')
        # self.pattern_ymr2 = re.compile(u'(\d不要)')
        # 2016——12——12
        self.pattern_ymr3 = re.compile(u'(\d{2,4}[—]+\d{1,2}[—]+\d{1,2})')
        # self.pattern_ymr3 = re.compile(u'(\d不要)')

        # 年、月
        # 2016/12 or 2016-12
        self.pattern_ym1 = re.compile(u'(\d{2,4}[/-]\d{1,2})')
        # self.pattern_ym1 = re.compile(u'(\d不要)')
        # 2016年12月
        self.pattern_ym2 = re.compile(u'(\d{2,4}年\d{1,2}月)')
        # self.pattern_ym2 = re.compile(u'(\d不要)')
        # 2016——12
        self.pattern_ym3 = re.compile(u'(\d{2,4}[—]+\d{1,2})')
        # self.pattern_ym3 = re.compile(u'(\d不要)')

        # 2012年1——6月
        self.pattern_ym4 = re.compile(u'(\d{2,4}年\d{1,2}[—]+\d{1,2}月)')
        # self.pattern_ym4 = re.compile(u'(\d不要)')
        # 2012年1-6月 or 2012年1至6月 or 2012年1到6月
        self.pattern_ym5 = re.compile(u'(\d{2,4}年\d{1,2}[-至到]\d{1,2}月)')
        # self.pattern_ym5 = re.compile(u'(\d不要)')

        # 月、日
        # 12月12日
        self.pattern_mr = re.compile(u'(\d{1,2}月\d{1,2}日)')
        # self.pattern_mr = re.compile(u'(\d不要)')

        # 年
        # 2012年 or 12年
        self.pattern_y = re.compile(u'(\d{2,4}年)')
        # self.pattern_y = re.compile(u'(\d不要)')

        # 月
        # 1-6月 or 1至6月 or 1到6月
        self.pattern_m1 = re.compile(u'(\d{1,2}[-至到]\d{1,2}月)')
        # self.pattern_m1 = re.compile(u'(\d不要)')
        # 1——6月
        self.pattern_m2 = re.compile(u'(\d{1,2}[—]+\d{1,2}月)')
        # self.pattern_m2 = re.compile(u'(\d不要)')
        # 9月
        self.pattern_m3 = re.compile(u'(\d{1,2}月)')
        # self.pattern_m3 = re.compile(u'(\d不要)')

    def extract_date(self, text):
        """
        提取日期描述
        :param text: 输入文本
        :return:
        """
        try:
            self.result_list = list()
            # 日期描述在字串中的位置
            self.index_list = list()
            # 2016/12/12 or 2016 12 12 or 2016—12—12
            self._extract_ymr1(text)
            # 2016年12月12日
            self._extract_ymr2(text)
            # 2016——12——12
            self._extract_ymr3(text)
            # 2016/12 or 2016—12
            self._extract_ym1(text)
            # 2016年12月
            self._extract_ym2(text)
            # 2016——12
            self._extract_ym3(text)
            # 2012年1——6月
            self._extract_ym4(text)
            # 2012年1-6月 or 2012年1至6月 or 2012年1到6月
            self._extract_ym5(text)
            # 12月12日
            self._extract_mr(text)
            # 2012年 or 12年
            self._extract_y(text)
            # 1-6月 or 1至6月 or 1到6月
            self._extract_m1(text)
            # 1——6月
            self._extract_m2(text)
            # 9月
            self._extract_m3(text)

            # nlp映射方式
            self._extract_nlp(text)
            # sort
            sort_list = sorted(self.result_list, key=lambda x: x['index'], reverse=False)
            # 格式化
            final_list = list()
            for info in sort_list:
                # 连接字符格式化
                if u'—' in info['month'] or u'至' in info['month'] or u'到' in info['month']:
                    info['month'] = info['month'].replace(u'—', '-').replace(u'至', '-').replace(u'到', '-')
                    _seg = info['month'].split('-')
                    if len(_seg) > 2:
                        info['month'] = _seg[0] + '-' + _seg[len(_seg) - 1]
                # month 格式化
                if info['month']:
                    date_dict = re.search(r'(?P<start>\d{1,2})(-{0,1})(?P<end>\d{0,2})', info['month']).groupdict()
                    _start = int(date_dict['start'])
                    if _start < 10:
                        _start = '0' + str(_start)
                    else:
                        _start = str(_start)
                    if date_dict['end']:
                        _end = int(date_dict['end'])
                        if _end < 10:
                            _end = '0' + str(_end)
                        else:
                            _end = str(_end)
                        info['month'] = _start + '-' + _end
                    else:
                        info['month'] = _start
                # day 格式化
                if info['day']:
                    _day = int(info['day'])
                    if _day < 10:
                        info['day'] = '0' + str(_day)
                final_list.append(info)
            return final_list
        except Exception, e:
            logger.error('extract date failed for %s' % str(e))
            return []

    def update_date_describe(self, result, pattern, length, index):
        """
        更新日期描述，对已有日期判断并更新
        :param result: 输入日期描述
        :param pattern: 分割模式
        :param length: 分割长度
        :param index: 位置
        :return:
        """
        try:
            seg = re.split(pattern, result)
            if len(seg) == length:
                year = ''
                month = ''
                day = ''
                if length >= 3:
                    year = seg[0]
                    if len(year) == 2:
                        year = '20' + year
                    month = seg[1]
                    if u'-' in month or u'—' in month or u'至' in month or u'到' in month:
                        pass
                    else:
                        if month:
                            if int(month) > 12:
                                return None
                    day = seg[2]
                    if day:
                        if int(day) > 31:
                            return None
                elif length == 2:
                    year = seg[0]
                    if len(year) == 2:
                        year = '20' + year
                    month = seg[1]
                    if int(month) > 12:
                        return None
                    day = ''
                elif length == 1:
                    year = seg[0]
                    if len(year) == 2:
                        year = '20' + year
                    result += u'年'
                if not year:
                    return None
                date_dict = {
                    'index': index,
                    'year': year,
                    'month': month,
                    'day': day,
                    'date_des': result
                }
                add_flag = True
                rv_falg = False
                rv_info = None
                if index in self.index_list:
                    for info in self.result_list:
                        if info['index'] == index:
                            add_flag = False
                            if len(result) > len(info['date_des']):
                                rv_falg = True
                                rv_info = info
                            break
                if rv_falg:
                    self.result_list.remove(rv_info)
                    self.result_list.append(date_dict)
                elif add_flag and date_dict not in self.result_list:
                    self.result_list.append(date_dict)
                    self.index_list.append(index)
                return self.result_list, self.index_list
        except Exception, e:
            logger.error('update date describe failed for %s' % str(e))
            return self.result_list, self.index_list

    ##########################private_func##########################
    def _check_grammar(self, seg):
        """
        格式、语法校对
        :param seg:
        :return:
        """
        year = None
        month = None
        day = None
        if len(seg) == 3:
            year = seg[0]
            if len(year) == 2:
                year = '20' + year
            month = seg[1]
            if int(month) > 12:
                return False, None
            day = seg[2]
            if int(day) > 31:
                return False, None
        return True, {"year": year,
                      "month": month,
                      "day": day}

    def _extract_ymr1(self, text):
        """
        2016/12/12 or 2016 12 12 or 2016—12—12
        :param text:
        :return:
        """
        result1 = self.pattern_ymr1.findall(text)
        symbol = re.split(ur"[}\\]", self.pattern_ymr1.pattern)
        _len = 0
        for result in result1:
            index = text.index(result, _len)
            _len = index + len(result)
            if self._check_tail(text, result, index):
                continue
            seg = re.split(symbol[2], result)
            flag, _date = self._check_grammar(seg)
            if flag:
                date_dict = {
                    'index': index,
                    'year': _date['year'],
                    'month': _date['month'],
                    'day': _date['day'],
                    'date_des': result
                }
                if date_dict not in self.result_list:
                    self.result_list.append(date_dict)
                if index not in self.index_list:
                    self.index_list.append(index)

    def _extract_ymr2(self, text):
        """
        # 2016年12月12日
        :param text:
        :return:
        """
        result2 = self.pattern_ymr2.findall(text)
        pattern = ur'[年月日]'
        length = 4
        _len = 0
        for result in result2:
            index = text.index(result, _len)
            _len = index + len(result)
            self.update_date_describe(result, pattern, length, index)

    def _extract_ymr3(self, text):
        """
        2016——12——12
        :param text:
        :return:
        """
        result3 = self.pattern_ymr3.findall(text)
        symbol = re.split(ur"[}\\]", self.pattern_ymr3.pattern)
        length = 3
        _len = 0
        for result in result3:
            index = text.index(result, _len)
            _len = index + len(result)
            if self._check_tail(text, result, index):
                continue
            self.update_date_describe(result, symbol[2], length, index)

    def _extract_ym1(self, text):
        """
        2016/12 or 2016—12
        :param text:
        :return:
        """
        result4 = self.pattern_ym1.findall(text)
        symbol = re.split(ur"[}\\]", self.pattern_ym1.pattern)
        length = 2
        _len = 0
        for result in result4:
            index = text.index(result, _len)
            _len = index + len(result)
            if self._check_tail(text, result, index):
                continue
            self.update_date_describe(result, symbol[2], length, index)

    def _extract_ym2(self, text):
        """
        2016年12月
        :param text:
        :return:
        """
        result5 = self.pattern_ym2.findall(text)
        pattern = ur'[年月]'
        length = 3
        _len = 0
        for result in result5:
            index = text.index(result, _len)
            _len = index + len(result)
            self.update_date_describe(result, pattern, length, index)

    def _extract_ym3(self, text):
        """
        2016——12
        :param text:
        :return:
        """
        result6 = self.pattern_ym3.findall(text)
        symbol = re.split(ur"[}\\]", self.pattern_ym3.pattern)
        length = 2
        _len = 0
        for result in result6:
            index = text.index(result, _len)
            _len = index + len(result)
            if self._check_tail(text, result, index):
                continue
            self.update_date_describe(result, symbol[2], length, index)

    def _extract_ym4(self, text):
        """
        2012年1——6月
        :param text:
        :return:
        """
        result7 = self.pattern_ym4.findall(text)
        pattern = ur'[年月]'
        length = 3
        _len = 0
        for result in result7:
            index = text.index(result, _len)
            _len = index + len(result)
            self.update_date_describe(result, pattern, length, index)

    def _extract_ym5(self, text):
        """
        2012年1-6月 or 2012年1至6月 or 2012年1到6月
        :param text:
        :return:
        """
        result8 = self.pattern_ym5.findall(text)
        pattern = ur'[年月]'
        length = 3
        _len = 0
        for result in result8:
            index = text.index(result, _len)
            _len = index + len(result)
            self.update_date_describe(result, pattern, length, index)

    def _extract_mr(self, text):
        """
        12月12日
        :param text:
        :return:
        """
        result13 = self.pattern_mr.findall(text)
        _len = 0
        for result in result13:
            index = text.index(result, _len)
            _len = index + len(result)
            seg = re.split(ur'[月日]', result)
            if len(seg) == 3:
                year = ''
                month = seg[0]
                if month:
                    if int(month) > 12:
                        continue
                day = seg[1]
                date_dict = {
                    'index': index,
                    'year': year,
                    'month': month,
                    'day': day,
                    'date_des': result
                }
                lf_flag = True
                for i in self.index_list:
                    if abs(i - index) <= 5:
                        for r in self.result_list:
                            if i == r['index'] and result in r['date_des']:
                                lf_flag = False
                                break
                if lf_flag:
                    self.result_list.append(date_dict)
                    self.index_list.append(index)

    def _extract_y(self, text):
        """
        2012年 or 12年
        :param text:
        :return:
        """
        result9 = self.pattern_y.findall(text)
        pattern = ur'[年]'
        length = 1
        _len = 0
        for result in result9:
            index = text.index(result, _len)
            _len = index + len(result)
            result = result.replace(u'年', '')
            self.update_date_describe(result, pattern, length, index)

    def _extract_m1(self, text):
        """
        1-6月 or 1至6月 or 1到6月
        :param text:
        :return:
        """
        result10 = self.pattern_m1.findall(text)
        symbol = re.split(ur"[}\\]", self.pattern_m1.pattern)
        _len = 0
        for result in result10:
            index = text.index(result, _len)
            _len = index + len(result)
            year = ''
            month = result.replace(u'月', '')
            _seg = re.split(symbol[2], month)
            if int(_seg[0]) > 12 or int(_seg[1]) > 12:
                continue
            day = ''
            date_dict = {
                'index': index,
                'year': year,
                'month': month,
                'day': day,
                'date_des': result
            }
            lf_flag = True
            for i in self.index_list:
                if abs(i - index) <= 5:
                    for r in self.result_list:
                        if i == r['index'] and result in r['date_des']:
                            lf_flag = False
                            break
            if lf_flag:
                self.result_list.append(date_dict)
                self.index_list.append(index)

    def _extract_m2(self, text):
        """
        1——6月
        :param text:
        :return:
        """
        result11 = self.pattern_m2.findall(text)
        symbol = re.split(ur"[}\\]", self.pattern_m2.pattern)
        _len = 0
        for result in result11:
            index = text.index(result, _len)
            _len = index + len(result)
            year = ''
            month = result.replace(u'月', '')
            _seg = re.split(symbol[2], month)
            if int(_seg[0]) > 12 or int(_seg[1]) > 12:
                continue
            day = ''
            date_dict = {
                'index': index,
                'year': year,
                'month': month,
                'day': day,
                'date_des': result
            }
            lf_flag = True
            for i in self.index_list:
                if abs(i - index) <= 5:
                    for r in self.result_list:
                        if i == r['index'] and result in r['date_des']:
                            lf_flag = False
                            break
            if lf_flag:
                self.result_list.append(date_dict)
                self.index_list.append(index)

    def _extract_m3(self, text):
        """
        9月
        :param text:
        :return:
        """
        result12 = self.pattern_m3.findall(text)
        _len = 0
        for result in result12:
            index = text.index(result, _len)
            _len = index + len(result)
            year = ''
            month = result.replace(u'月', '')
            if int(month) > 12:
                continue
            day = ''
            date_dict = {
                'index': index,
                'year': year,
                'month': month,
                'day': day,
                'date_des': result
            }
            lf_flag = True
            for i in self.index_list:
                if abs(i - index) <= 9:
                    for r in self.result_list:
                        if i == r['index'] and result in r['date_des']:
                            lf_flag = False
                            break
            if lf_flag:
                self.result_list.append(date_dict)
                self.index_list.append(index)

    def _check_tail(self, text, result, index):
        """
        检查匹配字串下一个字符是否为数字
        :param text:
        :param result:
        :param index:
        :return:
        """
        _len = len(result) + index
        temp_str = text[_len:_len + 1]
        if temp_str.isdigit():
            return True
        return False

    def _extract_nlp(self, text):
        """
        nlp映射方式
        :param text:
        :return:
        """
        nlp_list = list()
        for date in self.nlp_date_madel:
            date_des = date['rawDes']
            _seg = re.split(u'[,，。.？?！!;；]', text)
            _len = 0
            for _text in _seg:
                if date_des in _text:
                    index = text.index(date_des, _len)
                    _len = index + len(_text) + 1
                    date_dict = {
                        'index': index,
                        'year': date['year'],
                        'month': date['month'],
                        'day': date['day'],
                        'date_des': date_des
                    }
                    add_flag = True
                    rv_flag = False
                    for result in nlp_list:
                        if abs(index - result['index']) <= 3:
                            add_flag = False
                            if len(result['date_des']) < len(date_des):
                                rv_flag = True
                                rv_info = result
                                add_flag = True
                    if rv_flag:
                        nlp_list.remove(rv_info)
                    if add_flag:
                        nlp_list.append(date_dict)
        for result in nlp_list:
            self.result_list.append(result)


##########################external_func########################
def load_date_model(path):
    """
    加载时间格式化模型
    :param path:
    :return:
    """
    try:
        path = unicode(path, 'utf-8')
        result_list = json.load(open(path, 'rb'))
        return result_list
    except Exception, e:
        logger.error('load date model failed for %s' % str(e))
        return []


if __name__ == '__main__':
    date_path = '../stable/date_format.json'
    date_model = dateFormate(date_path)
    # test
    text = u'2011 12 12，2011/12/22，2011-1-12,如这样的日期2011.5.8，不正确日期2011-19-5，2011 6 1234，' \
           u'2012年2月18日，' \
           u'2013———12———2, 2013——12——3，2013—12—25,' \
           u'2014-11, 2014/12，' \
           u'2015年3月，' \
           u'2016——1，2016———2，2016—3，' \
           u'2017年1———6月, 也可以匹配到2017年1—3月，' \
           u'2018年1到6月,2018年1-7月，2018年3到9月。' \
           u'9月9日，' \
           u'2020年, 20年，' \
           u'3-6月，1至5月，1到3月，' \
           u'4—7月，2———6月，2——4月，' \
           u'11月, 25月，' \
           u'一二季度，一至三季度,我的三季度，' \
           u'其他干扰测试：2018年多岁的5月21日。'
    result_list = date_model.extract_date(text)
    for result in result_list:
        print('index:%s\tyear:%s\tmonth:%s\tday:%s\tdate_des:%s'
              % (result['index'], result['year'], result['month'], result['day'], result['date_des']))
