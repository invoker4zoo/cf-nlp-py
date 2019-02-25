# -*- coding:utf-8 -*-
# @Time     : 2019/2/25 10:16
# @Author   : Tanrui
# @Email    : cq_tanrui@163.com
# @File     : word2vector_parser.py
# @Software : PyCharm
# @Desc     :

import numpy
from gensim.models import word2vec

class word2vector(object):

    def __init__(self, train_file_path, vm_model_path):
        self.train_file_path = train_file_path
        self.vec_model_path = vm_model_path

    def train(self):
        str = word2vec.LineSentence(self.train_file_path)
        model = word2vec.Word2Vec(str, size=300)
        model.save(self.vm_model_path)

    def
