# -*- coding:utf-8 -*-
# @Time     : 2019/2/28 16:25
# @Author   : Tanrui
# @Email    : cq_tanrui@163.com
# @File     : PDF_table_parser.py
# @Software : PyCharm
# @Desc     : 提取各省市2018预算执行和2019预算信息，
# 提取字段：财政事务--信息化建设；国有资产监管--行政运行

import numpy as np
import pdfplumber

class PdfTableExtract(object):

    def __init__(self, file_path):
        self.file_path = file_path
        self.info_constraction = [u'财政事务', u'信息化建设']
        self.assets_supervision = [u'国有资产监管', u'行政运行']

    def pdf_table_extrct(self):
        pdf = pdfplumber.open(self.file_path)
        flag_info = 0
        flag_asset = 0
        for page in pdf.pages:
            # 获取当前页面的全部文本信息，包括表格中的文字
            # print (page.extract_text())
            for table in page.extract_tables():
                # print(table)
                row_head = table[0]
                for row in table:
                    for r in row:
                        if self.info_constraction[0] == r:
                            flag_info = 1
                    if flag_info >= 1:
                        flag_info += 1
                    if self.info_constraction[1] in row and 9 >= flag_info >= 1:
                        for cell in row_head:
                            print cell.encode("utf-8")+"\t",
                        print
                        for cell in row:
                            print cell.encode("utf-8")+"\t",
                        print

                    if self.assets_supervision[0] in row:
                        flag_asset = 1
                    if flag_asset >= 1:
                        flag_asset += 1
                    if self.assets_supervision[1] in row and 4 >= flag_asset >= 1:
                        for cell in row_head:
                            print cell.encode("utf-8") + "\t",
                        print
                        for cell in row:
                            print cell.encode("utf-8") + "\t",
                        print


if __name__ == '__main__':
    file_path = u"C:/Users/tanru/Desktop/厦门市2019财政预算.pdf"  # type: str
    pdf_parser = PdfTableExtract(file_path)
    pdf_parser.pdf_table_extrct()
