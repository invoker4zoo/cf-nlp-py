# coding=utf-8
"""
@ license: Apache Licence
@ github: invoker4zoo
@ author: invoker/cc
@ wechart: whatshowlove
@ software: PyCharm
@ file: rule_lib.py
@ time: $19-6-27 下午2:28
"""
import re
doc = u'''一、中国制造业采购经理指数运行情况
（1） 测试1
1、 测试1.1
二、中国制造业采购经理指数运行情况-测试2
（2）测试2
1、测试2.1
2、测试2.2
'''
###############################
## re pattern lib
###############################
level_one_pattern = re.compile(u'[一|二|三|四|五]、')
level_two_pattern = re.compile(u'（\d+）')
level_three_pattern = re.compile(u'\d+、')
# start_tag = 0
# cache_list = []
# for m in re.finditer(level_one_pattern, doc):
#     if m.start()> start_tag:
#         cache_list.append(doc[start_tag:m.start()])
#         start_tag = m.start()
# if start_tag>0 and start_tag<len(doc):
#     cache_list.append(doc[start_tag:])


def parser_document(doc, rule_list, step=0):
    """

    :param doc: 需要解析的文本
    :param rule_list:解析文本层级的正则规则列表，正则规则按结构层级顺序排列
                    [level_one_pattern, level_two_pattern, level_three_pattern]
    :param step:
    :return:
    """
    if step >= len(rule_list):
        return [doc]
    start_tag = 0
    cache_list = []
    for m in re.finditer(rule_list[step], doc):
        if m.start() > start_tag:
            cache_doc = doc[start_tag:m.start()]
            cache_list += parser_document(cache_doc, rule_list, step=step + 1)
            start_tag = m.start()
    if start_tag == 0:
        return [doc]
    if start_tag > 0 and start_tag < len(doc):
        cache_doc = doc[start_tag:]
        cache_list += parser_document(cache_doc, rule_list, step=step + 1)
    return cache_list

result = parser_document(doc, [level_one_pattern, level_two_pattern, level_three_pattern], 0)


class RULELIB(object):
    def __init__(self):
        pass

    def pattern_lib(self):
        """
        常用正则 pattern 库
        :return:
        """
        CHINESE = re.compile(u'[一、|二、|三、|四、|五、]')