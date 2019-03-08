# coding=utf-8
"""
@ license: Apache Licence
@ github: invoker4zoo
@ author: invoker/cc
@ wechart: whatshowlove
@ software: PyCharm
@ file: func_timer.py
@ time: $19-3-8 下午5:48
"""
import datetime
from cfnlp.tools.logger import logger


def func_timer(func):
    def int_time(*args, **kwargs):
        # 程序开始时间
        start_time = datetime.datetime.now()
        # func process
        func(*args, **kwargs)
        # 程序结束时间
        end_time = datetime.datetime.now()
        total_time = (end_time - start_time).total_seconds()
        logger.info('程序运行时间总计%s秒' % total_time)
    return int_time