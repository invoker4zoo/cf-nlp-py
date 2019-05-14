#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019-04-10 09:44
@Author  : zhangyu
@Contact : zhangycqupt@163.com
@File    : text_abstract.py
@Software: PyCharm
@Site    : https://github.com/zhangyuo
"""
import io
import subprocess
import os
from subprocess import STDOUT, PIPE


class summary(object):
    """
    文本摘要方法集合
    """

    def __init__(self, model_path, doc_path):
        """

        :param model_path: jar path
        """
        self.jar_path = model_path
        self.doc_path = doc_path

    def pkusumsum(self, input, output, T=1, L=1, n=500, m=2, stop='n'):
        """
        基于北大万小军老师团队的自动摘要方法汇总，支持单文档摘要、多文档摘要、topic-focused多文档摘要。
        :param input: 输入文件路径
        :param output: 输出文件路径
        :param T: 1-单文档摘要；2-多文档摘要；3-基于主题的多文档摘要
        :param L: 1-中文；2-英文；3-其他语言
        :param n: 返回摘要词长度
        :param m: T=1: 1 - Lead, 2 - Centroid, 3 - ILP, 4 - LexPageRank, 5 -TextRank, 6 - Submodular;
                  T=2: 0 - Coverage, 1 - Lead, 2 - Centroid, 3 - ILP, 4 - LexPageRank, 5 - TextRank, 6 - Submodular, 7 - ClusterCMRW;
                  T=3: 0 - Coverage, 1 - Lead, 2 - Centroid, 8 - ManifoldRank.
        :param stop: y-添加停用词表；n-不使用停用词表
        :return:
        """
        command = "java -jar %s -T %d -input %s -output %s -L %d -n %d -m %d -stop %s" % (
            self.jar_path, T, input, output, L, n, m, stop)
        p = subprocess.Popen(command, shell=True)
        p.wait()

    def single_text_abstract(self, instring, L=1, n=500, m=2, stop='n'):
        """
        单文本摘要
        :param instring: 输入文本
        :param L: 1-中文；2-英文；3-其他语言
        :param n: 返回摘要词长度
        :param m: 1 - Lead, 2 - Centroid, 3 - ILP, 4 - LexPageRank, 5 -TextRank, 6 - Submodular;
        :param stop: y-添加停用词表；n-不使用停用词表
        :return:
        """
        T = 1
        instring = instring.decode('utf-8')
        # generate doc
        file_path = self.doc_path + 'data.txt'
        output_path = self.doc_path + 'output.txt'
        with io.open(file_path, 'w', encoding='utf-8') as f:
            f.write(instring)
        self.pkusumsum(file_path, output_path, T, L, n, m, stop)
        result = ''
        with io.open(output_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                result += line
        return result


if __name__ == '__main__':
    model_path = '../stable/text-abstract.jar'
    doc_path = '../data/abstract/'
    model = summary(model_path, doc_path)
    # model.pkusumsum('/Users/zhangyu/Documents/data/data_test/abstract/test.txt',
    #                 '/Users/zhangyu/Documents/data/data_test/abstract/sample.txt', m=2)
    # 文本输入方式
    doc = """
    各省、自治区、直辖市、计划单列市财政厅（局）、住房城乡建设厅（局）：
按照《中央财政城镇保障性安居工程专项资金管理办法》（财综〔2017〕2号）等规定，现就分配下达2019年中央财政城镇保障性安居工程专项资金（以下称专项资金）预算的有关事宜通知如下：
一、根据财政部测算的均衡性转移支付财政困难程度系数，租赁补贴和棚户区改造2019年任务计划情况，以及国务院对2018年棚户区改造真抓实干成效明显地方（内蒙古自治区乌兰察布市、湖南省长沙市、江西省上饶市、新疆维吾尔自治区乌鲁木齐市、江苏省徐州市、山东省潍坊市、浙江省温州市、安徽省阜阳市、四川省南充市、河南省三门峡市、贵州省黔西南布依族苗族自治州、陕西省延安市）予以表扬激励的要求，现下达2019年中央财政城镇保障性安居工程专项资金（见附件2，项目代码Z135080000028，列《2019年政府收支分类科目》110类02款“一般性转移支付收入”58项“住房保障共同财政事权转移支付收入”科目。
我们将根据财政部驻当地财政监察专员办事处对租赁补贴、城市棚户区改造2018年完成情况，2018年城镇保障性安居工程财政资金绩效评价结果的审核认定数，适时对专项资金分配结果进行清算。
二、该专项资金用于向符合条件的在市场租赁住房的城镇住房保障家庭发放租赁补贴和支持城市棚户区改造项目，具体使用范围按照财综〔2017〕2号文件规定执行。
三、省级财政部门会同同级住房保障部门，应当结合本地实际情况，于接到专项资金后30日内，将专项资金一次性分配下达到县级以上各级财政部门。同时将下达专项资金文件抄送财政部驻当地财政监察专员办事处。
四、市、县财政部门收到专项资金后，应当实行专项管理、分账核算，按照规定统筹用于本市、县租赁补贴、城市棚户区改造，并按照工作（工程）进度及时拨付资金，确保资金专款专用，确保完成2019年城镇保障性安居工程任务。专项资金可统筹用于纳入国家计划的近3年城市棚户区改造项目。
五、市、县财政部门安排使用专项资金时，按用途分别填列《2019年政府收支分类科目》221类“住房保障支出”01款“保障性安居工程支出”03项“棚户区改造”和07项“保障性住房租金补贴”科目。
六、为贯彻落实党的十九大关于“全面实施绩效管理”的决策部署，切实提高资金使用效益，请在组织预算执行中对照你省（自治区、直辖市）绩效目标（附件4）做好绩效监控，确保绩效目标如期实现。同时请参照中央做法，将你省（自治区、直辖市）绩效目标及时对下分解，按要求做好省内预算绩效管理工作。
    """
    result = model.single_text_abstract(doc)
    print(result)
