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
import os
import json
from bs4 import BeautifulSoup
import numpy as np
from cfnlp.tools.logger import logger
from cfnlp.stable.punct import sentence_delimiters
import jieba

reload(sys)
sys.setdefaultencoding('utf-8')


class htmlTableAnalysis(object):

    def __init__(self, origin_html):
        """

        :param origin_html: 需要传入的html文件原文件内容
        :param saving_path: 输出的解析文件路径
        """
        self.html = origin_html
        self.soup = BeautifulSoup(self.html, 'html5lib')
        # self.saving_path = saving_path

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
                if seg in sentence_delimiters:
                    return True
            except:
                continue
        return False

    def _check_list_repeat(self, key_list):
        """
        判断列表中是否存在重复的子列表,如果有，提出子列表的index 和key
        :param key_list:
        :return:is_repeat bool
                repeat index list [[index1, index2, index3,...],...]
                new_key_list list
        """
        key_list = key_list.tolist()
        is_repeat = False
        key_set = set(key_list)
        key_list_length = len(key_list)
        if len(key_set) == len(key_list):
            return False, None, key_list
        new_key_list = key_list
        for seg in key_list:
            seg_index = [index for index, key in enumerate(key_list) if seg == key]
            if len(seg_index) > 1:
                cache_list = list()
                for index, _ in enumerate(seg_index[:-1]):
                    cache_list.append(seg_index[index + 1] - seg_index[index])
                cache_list.append(key_list_length - seg_index[-1])
                repeat_length = min(cache_list)
                if repeat_length < 2:
                    continue
                for shift in range(1, repeat_length):
                    cache_list = list()
                    for index in seg_index:
                        cache_list.append(key_list[index:index + shift + 1])
                    # set unhashable list
                    # if len(set(cache_list)) == 1:
                    #     continue
                    for index in range(0, len(cache_list) - 1):
                        if cache_list[index] == cache_list[index + 1]:
                            continue
                        else:
                            index -= 1
                            break
                    if index == len(cache_list) - 2:
                        if shift == repeat_length - 1:
                            is_repeat = True
                            shift_length = shift
                            continue
                        else:
                            continue
                    else:
                        if shift == 1:
                            break
                        else:
                            is_repeat = True
                            shift_length = shift - 1
                            break
                if is_repeat:
                    new_key_list = key_list[seg_index[0]:seg_index[0] + shift_length + 1]
                    cache_list = list()
                    for index in seg_index:
                        cache_list.append(range(index, index + shift_length + 1))
                    return is_repeat, cache_list, new_key_list
                else:
                    return False, None, new_key_list
            else:
                continue
        return False, None, new_key_list

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

    def generate_table_matrix(self, table_tag, table_col, table_row):
        """

        :param table_tag:
        :param table_col:
        :param table_row:
        :return:
        """
        try:
            str_matrix = [[None for _ in range(table_col)] for _ in range(table_row)]
            for row_index, tr in enumerate(table_tag.find_all('tr')):
                for col_index, td in enumerate(tr.find_all('td')):
                    wide = 0
                    height = 0
                    des = self._get_tag_string(td)
                    des = des.strip()
                    des = des.replace('\n', '')
                    des = des.replace(' ', '')
                    for i in range(0, table_col - col_index):
                        if str_matrix[row_index][col_index + i] == None:
                            str_matrix[row_index][col_index + i] = des
                            # 横向重定位
                            col_index = col_index + i
                            break
                        else:
                            continue
                    if td.attrs.get('rowspan'):
                        height = int(td.attrs.get('rowspan'))
                    if td.attrs.get('colspan'):
                        wide = int(td.attrs.get('colspan'))
                    if wide and height:
                        for i in range(0, height):
                            for j in range(0, wide):
                                str_matrix[row_index + i][col_index + j] = des
                        continue
                    elif wide or height:
                        if wide:
                            for i in range(1, wide):
                                str_matrix[row_index][col_index + i] = des
                        if height:
                            for i in range(1, height):
                                str_matrix[row_index + i][col_index] = des
                    else:
                        pass
            # self.matrix = str_matrix
            return str_matrix
        except Exception, e:
            logger.error('get table matrix failed')
            return None

    def generate_table_json(self, matrix, row_head, _col_head):
        """
        表格数据json化
        :param table_tag:
        :param matrix:
        :param row_head:
        :return:
        """
        try:
            table_info = []
            matrix = np.array(matrix)
            table_col = len(matrix[0, :])
            table_row = len(matrix[:, 0])
            # 在函数内部对_col_head进行了操作，需要用函数内的变量代替_col_head
            # global _col_head
            row_list = matrix[row_head:, _col_head - 1]
            col_list = matrix[row_head - 1, _col_head:]
            head_str = matrix[row_head - 1, _col_head - 1]
            year_head = 0
            num_head = 0
            year_head_row = 0
            num_head_row = 0
            for seg in col_list:
                if seg.endswith(u'年'):
                    year_head += 1
                try:
                    int(seg.strip())
                    num_head += 1
                except:
                    pass
            for seg in row_list:
                if seg.endswith(u'年'):
                    year_head_row += 1
                try:
                    float(seg.strip())
                    num_head_row += 1
                except:
                    pass
            # clean head_str
            head_str = head_str.strip().replace('\n', '').replace(' ', '')
            if head_str == u'序号':
                head_str_index = True
            else:
                head_str_index = False

            is_horizontal = True if float(year_head) / table_col > 0.6 or float(num_head) / table_col > 0.6 else False
            # 去除序号列
            is_row_num = True if float(year_head_row) / table_col < 0.4 or float(
                num_head_row) / table_col > 0.6 else False
            if head_str_index and is_row_num:
                _col_head += 1
                row_list = matrix[row_head:, _col_head - 1]
                col_list = matrix[row_head - 1, _col_head:]
            if is_horizontal:
                key_list = row_list
                inner_key_list = col_list
            else:
                key_list = col_list
                inner_key_list = row_list
            is_repeat, repeat_index, new_key_list = self._check_list_repeat(key_list)
            if not is_repeat:
                info_dic = dict()
                for i, key in enumerate(key_list):
                    key = key.strip().replace('\n', '').replace(' ', '')
                    if key not in info_dic.keys():
                        info_dic[key] = dict()
                    else:
                        continue
                    for j, inner_key in enumerate(inner_key_list):
                        inner_key = inner_key.strip().replace('\n', '').replace(' ', '')
                        if inner_key not in info_dic[key].keys():
                            if is_horizontal:
                                info_dic[key][inner_key] = matrix[i + row_head, j + _col_head]
                            else:
                                info_dic[key][inner_key] = matrix[j + row_head, i + _col_head]
                table_info.append(info_dic)
                # return table_json
            else:
                # 是否一开始就出现重复key
                # 如果重复key是以第一个key开始，则重新提取inner_key
                if repeat_index[0][0] != 0:
                    begin_repeat = False
                else:
                    begin_repeat = True
                for index_list in repeat_index:
                    if begin_repeat:
                        if is_horizontal:
                            inner_key_list = matrix[row_head + index_list[0] - 1, _col_head:]
                        else:
                            inner_key_list = matrix[row_head:, _col_head + index_list[0] - 1]
                    info_dic = dict()
                    for i, key in zip(index_list, new_key_list):
                        key = key.strip().replace('\n', '').replace(' ', '')
                        if key not in info_dic.keys():
                            info_dic[key] = dict()

                        for j, inner_key in enumerate(inner_key_list):
                            inner_key = inner_key.strip().replace('\n', '').replace(' ', '')
                            if inner_key not in info_dic[key].keys():
                                if is_horizontal:
                                    info_dic[key][inner_key] = matrix[i + row_head][j + _col_head]
                                else:
                                    info_dic[key][inner_key] = matrix[j + row_head][i + _col_head]
                    table_info.append(info_dic)
            return table_info
        except Exception, e:
            logger.error('get table info failed for %s' % str(e))
            return []

    def get_html_table_info(self):
        """
        html解析主函数
        输出table_info_dic

        [
            {
                'matrix': [[], []],
                'tableIndex': 1,
                'tableInfo':
            }
        ]
        :return:
        """
        try:
            self.table_info = list()
            for index, table in enumerate(self.soup.find_all('table')):
                info = dict()
                info['describe'] = self._search_table_describe(table)
                table_col, table_row, row_head, col_head, invaild = self._search_table_base_info(table)
                if invaild:
                    logger.info('find a invaild table tag, continue...')
                    continue
                else:
                    info['matrix'] = self.generate_table_matrix(table, table_col, table_row)
                    info['tableIndex'] = index
                    info['tableInfo'] = self.generate_table_json(info['matrix'], row_head, col_head)
                self.table_info.append(info)
            return self.table_info
        except Exception, e:
            logger.error('parser html failed for %s' % str(e))


if __name__ == '__main__':
    file_path = '/home/showlove/cc/gov/ppp/html'
    file_name = '高青县东部城区和南部新区集中供热工程项目财政承受能力论证报告（含附表）.htm'
    with open(os.path.join(file_path, file_name), 'rb') as f:
        content = f.read()
    html_parser = htmlTableAnalysis(content)
    table_info = html_parser.get_html_table_info()