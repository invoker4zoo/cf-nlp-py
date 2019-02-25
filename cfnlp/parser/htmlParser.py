# coding=utf-8
"""
@ license: Apache Licence
@ github: invoker4zoo
@ author: invoker/cc
@ wechart: whatshowlove
@ software: PyCharm
@ file: htmlParser.py
@ time: $19-2-21 下午3:28
"""
import sys
sys.path.append('..')
import json
from bs4 import BeautifulSoup
from tools.logger import logger
from stable.punct import sentence_delimiters
import jieba

class htmlTableAnalysis(object):

    def __init__(self, origin_html, saving_path):
        """

        :param origin_html: 需要传入的html文件原文件
        :param saving_path: 输出的解析文件路径
        """
        self.html = origin_html
        self.saving_path = saving_path

    def _get_tag_string(self, tag):
        """
        读取一个tag中的所有字符串
        :param tag:
        :return:
        """
        des = ''
        if tag.string:
            return tag.string
        else:
            for str in tag.strings:
                des += str
        return des

    def _check_sentence(self, str):
        """
        判断是否为完整句子
        :param str:
        :return:
        """
        for seg in str[::-1]:
            try:
                if seg.encode('utf-8') in sentence_delimiters:
                    return True
            except:
                continue
        return False

    def _search_table_describe(self, table_tag):
        """
        搜索表格标签的描述；
        搜索策略: 搜索text_align属性，有text_align属性搜索到非text_align为止；
                如果为段落，进行分句，取最后一个句子;需要判断tag是否有效
        :param: table_tag:bs 中的table tag
        :return: des表格描述字符串
        """
        try:
            des = ''
            for element in table_tag.previous_siblings:
                is_center = False
                if element.name:
                    # element.name
                    if element.name == 'table':
                        des = u'连续表'
                        break
                    if element.get('align', '') == 'center':
                        is_center = True
                        try:
                            int(self._get_tag_string(element).strip())
                            is_center = False
                            continue
                        except:
                            # if is_center:
                            #     continue
                            # else:
                            #     break
                            des = self._get_tag_string(element) + des
                            continue
                    else:
                        if is_center:
                            break

                    des = self._get_tag_string(element) + des
                    if self._check_sentence(des):
                        break
                else:
                    continue
            if self._check_sentence(des):
                if des[-1].encode('utf-8') in sentence_delimiters:
                    des = des[:-1]
                for index, seg in enumerate(des[::-1]):
                    if seg.encode('utf-8') in sentence_delimiters:
                        return des.split(seg)[-1]
                return des
            else:
                return des
        except Exception as e:
            logger.error('search table describe failed for %s' % str(e))

    def _search_table_base_info(self, table_tag):
        """
        计算表格基础信息
        :param table_tag:
        :return:
        """
        table_col = 0
        table_row = len(table_tag.find_all('tr'))
        tr_head = table_tag.find('tr')
        num_head = 0
        year_head = 0
        row_head = 1
        empty_head = 0
        type_list = list()
        for td in tr_head.find_all('td'):
            td_str = self._get_tag_string(td)
            td_str.strip()
            td_str.replace(',', '')
            try:
                float(str)
                num_head += 1
            except:
                try:
                    float(str[:-1])
                    num_head += 1
                except:
                    pass
            if td_str == '':
                empty_head += 1
            if td_str.endswith(u'年'):
                year_head += 1
            if td.attrs.get('rowspan'):
                row_head = max(row_head, int(td.attrs.get('rowspan')))
            if td.attrs.get('colspan'):
                table_col += int(td.attrs.get('colspan'))
            else:
                table_col += 1
            #
            if td.attrs.get('rowspan'):
                type_list.append(1)
            elif td.attrs.get('colspan'):
                type_list.append(2)
            else:
                type_list.append(0)
        # 计算左上表头大小，同一类型才能被默认为一个表头
        if type_list[0] == 0:
            col_head = 1
        else:
            for index in range(1, len(type_list)):
                if len(set(type_list[0:index + 1])) == 1:
                    continue
                else:
                    col_head = index
                    break
        # 判断横向表和竖向表
        # is_horizontal = True if float(year_head)/table_col > 0.6 or float(year_head)/table_col > 0.6 else False
        # 有效性检查
        invaild = True if float(empty_head) / table_col > 0.8 or table_col < 1 or table_row < 2 else False
        return table_col, table_row, row_head, col_head, invaild