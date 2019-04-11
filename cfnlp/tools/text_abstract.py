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

import subprocess
import os
from subprocess import STDOUT, PIPE


class summary(object):
    """
    文本摘要方法集合
    """

    def __init__(self, model_path):
        """

        :param model_path: jar path
        """
        self.jar_path = model_path

    def pkusumsum(self, input, output, T=1, L=1, n=100, m=2, stop='n'):
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
        command = "java -jar %s -T %d -input %s -output %s -L %d -n %d -m %d -stop %s" % (self.jar_path, T, input, output, L, n, m, stop)
        p = subprocess.Popen(command, shell=True)
        p.wait()


if __name__ == '__main__':
    model_path = '../stable/PKUSUMSUM.jar'
    model = summary(model_path)
    model.pkusumsum('/Users/zhangyu/Documents/data/corpus_6_4000/Auto_0.txt',
                    '/Users/zhangyu/Documents/data/data_test/abstract/sample.txt', )
    doc = """
    大C4毕加索首现优惠 现车降5000元现货供应
网上车市1月4日报道 
是以进口方式引进的一款集合了多项科技的MPV轿车。它搭载了雪铁龙最新的技术，将中央集控式方向盘、全新CVVT可变气门发动机引入其中，根据网上车市价格监测系统显示，目前大C4毕加索最高可优惠现金5000元。
据4S店销售人员介绍，目前C4大毕加索现车可优惠现金5000元，全系车型有舒适版和豪华版两款车型，售价分别为27.68万和30.68万。目前现车供货比较充足，现车颜色也比较齐全。消费者可在元旦期间到店看车选购。
 
大C4毕加索给人的第一感觉就是“大”：车长4.59米、轴距超过了2.7米，车顶高1.68米；超大的前挡风玻璃几乎延伸到了前排乘客的头顶，可视角度达到了惊人的70度，为驾驶者提供了一个非常出色的视野。复合式设计的超大头灯摄人心魂；前散热格栅上宽大的镀铬双人字齿轮标一直延伸到两个前车灯内侧，为大C4毕加索更添了一分干练和强悍；采用的柱式LED组合的大面积直立式尾灯十分醒目，同时也提高了夜间行车的辨识性。
 
大C4-毕加索的内部整理箱可谓是一应俱全，除了常规的手套箱之外，正、副驾驶前面的中控台上各有一个开启式的储物盒。另外大C4毕加索放弃了传统的换档操控位置，将四档自动电子变速箱的换档杆和换档拨片都集中到方向盘上，从而使前排中部的车内空间更宽裕，驾驶操作也更便捷，而且还得到了一个额外的空间奖励：一个位于中控台下方的5.4升大容积冷藏箱。
"""
    print('ok')
