# -*- coding:utf-8 -*-
# @Time     : 2019/2/25 10:16
# @Author   : Tanrui
# @Email    : cq_tanrui@163.com
# @File     : word_2_vector.py
# @Software : PyCharm
# @Desc     : 该模块包括训练文本预处理和词向量训练方法，
#             输入训练语料所在文件夹路径，输出词向量模型。

import os
import numpy
import jieba
from gensim.models import word2vec
from cfnlp.stable.punct import *
from cfnlp.tools.jar_methods import NLPModel

SEG_FILTER_FILEPATH = '../word_seg_filter_file.txt'

class word2vector(object):

    def __init__(self, train_file_dir, vm_model_path):
        self.train_file_dir = train_file_dir
        self.vec_model_path = vm_model_path

    def file_pretreatment(self):
        # seg_model_path = u"../cfnlp/stable/"
        # seg_jar_path = u"../cfnlp/stable/"
        # nlp_model = NLPModel(seg_model_path, seg_jar_path)
        file_list = os.listdir(self.train_file_dir)
        with open(SEG_FILTER_FILEPATH, 'w') as f:
            for i in range(0,len(file_list)):
                file_path = os.path.join(self.train_file_dir,file_list[i])
                if os.path.isfile(file_path):
                    file = open(file_path, 'r+')
                    for line in file:
                        # TODO 分词部分，以空格分隔存入文件
                        # seg_result = nlp_model.text_tokenizer(line, type='1')
                        seg_result = jieba.cut(line, cut_all=False)
                        print(seg_result)
                        line = punct(line)


    def train(self):
        str = word2vec.LineSentence(SEG_FILTER_FILEPATH)
        model = word2vec.Word2Vec(str, size=300)
        model.save(self.vm_model_path)

    def word2vec_test(self, word):
        wv_model = word2vec.Word2Vec.load(self.vec_model_path)
        word_vec = wv_model.wv
        if word in word_vec:
            print('word in corpus!')
            vector = word_vec[word]
            sim = word_vec.most_similar(word, topn=10)
            for item in sim:
                print(item[0] + '\t' + str(item[1]))
        else:
            print('word not in corpus!')

if __name__ == '__main__':
    train_file_dir = u'E:/tanrui/'
    vm_model_path = u'E:/tanrui/w2v.model'
    w2v = word2vector(train_file_dir,vm_model_path)
    w2v.file_pretreatment()
    w2v.train()
    w2v.word2vec_test('目录')