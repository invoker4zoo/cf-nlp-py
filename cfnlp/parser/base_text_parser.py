# coding=utf-8
"""
@ license: Apache Licence
@ github: invoker4zoo
@ author: invoker/cc
@ wechart: whatshowlove
@ software: PyCharm
@ file: base_text_parser.py
@ time: $19-3-8 下午5:19
"""
from nlp.punct import punct
import jieba
import thulac
import sys
from gensim import corpora, models
from gensim.models import Word2Vec
import multiprocessing
from gensim.models.word2vec import LineSentence
import os
import time
reload(sys)
sys.setdefaultencoding('utf-8')


class BaseTextParser(object):

    def __init__(self, file_path, seg_model='jieba', model_path=None):
        """

        :param file_path:
        :param seg_model: 使用的分词模型type ['jieba', 'thunlp']
        :param model_path:
        """
        self.file_path = file_path
        self.seg_model_type = seg_model
        if seg_model == 'jieba':
            self.seg_model = jieba
        elif seg_model == 'thunlp' and model_path != None:
            self.seg_model = thulac.thulac(seg_only=True, model_path=model_path)

    def load_file(self):
        """
        可针对不同的文本存储方式复写此方法
        :return:
        """
        if len(os.listdir(self.file_path)):
            # for file in os.listdir(self.file_path):
            # limit file num for testing
            for index, file in enumerate(os.listdir(self.file_path)):
                if index > 300:
                    break
                file_path = os.path.join(self.file_path, file)
                if os.path.isfile(file_path):
                    with open(file_path, 'rb') as f:
                        content = f.read().decode('utf-8')
                    tag = file.split('_')[0]
                    doc_str_list = self.cut_clearn_doc(content)
                    yield doc_str_list
        else:
            yield None

    def _iter_load_file(self):
        """

        :return:
        """
        return [x for x in self.load_file()]

    def cut_clearn_doc(self, doc):
        """

        :param doc: 传入的单篇文档文本
        :return:
        """
        # 分词
        if self.seg_model_type == 'jieba':
            doc_str_list = list(self.seg_model.cut(doc))
            # doc_str_list = list(doc_str_list)
        elif self.seg_model_type == 'thunlp':
            doc_str_list = self._get_thunlp_cut_list(self.seg_model.cut(doc))
        # 除去停用词
        stop_word_file = STOP_WORD_DIC_PATH
        with open(stop_word_file, 'rb') as f:
            stop_word_list = f.read().split('\n')
        doc_str_list = self._rm_stop_word(doc_str_list, stop_word_list)
        # 除去标点和特殊字符
        doc_str_list = self._rm_punct(doc_str_list, punct)
        return doc_str_list

    def _rm_stop_word(self, doc_str_list, stop_word_list):
        """
        移除停用词
        :param doc_str_list: 分词后的文档列表
        :return:
        """
        # with open(stop_word_file, 'rb') as f:
        #     stop_word_list = f.read().split('\n')
        # for n, item in enumerate(doc_str_list):
        #     if item in stop_word_list or item == u'':
        #         doc_str_list.pop(n)
        return [seg for seg in doc_str_list if seg not in stop_word_list and seg != u'']

    def _rm_punct(self, doc_str_list, punct_list):
        """
        移除标点符号
        :param doc_str_list:分词后的文档列表
        :return:
        """
        for n, item in enumerate(doc_str_list):
            if item in punct_list or item == '\u300':
                doc_str_list.pop(n)
        return doc_str_list

    def _get_thunlp_cut_list(self, thunlp_cut):
        """
        将thunlp分词结果提取为字符列表
        :param thunlp_cut:
        :return:
        """
        result_list = list()
        for item in thunlp_cut:
            result_list.append(item[0])
        return result_list

    def generate_docs_dictionary(self, dictionary_path):
        """
        生成文本库的字典文件
        :param dictionary_path:生成的dictionary文件的存储地址
        :return:
        """
        self.dictionary = corpora.Dictionary()
        for index, doc_str_list in enumerate(self.load_file()):
            # doc_str_list = self.cut_clearn_doc(content)
            self.dictionary.add_documents(doc_str_list)
            if index % 100 == 0:
                print '[%s] %d file has been loaded' % \
                      (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), index)
        # 寻找在文档中出现频率过低的词的id
        low_freq_ids = [tokenid for tokenid, freq in self.dictionary.dfs.items() if freq < 3]
        # filter_tokens 从词典中移除bad_id
        self.dictionary.filter_tokens(low_freq_ids)
        # 重新分配字典id号
        self.dictionary.compactify()
        # 保存字典文件
        self.dictionary.save(dictionary_path)

    def generate_docs_tfidf(self, dictionary_model_path, tfidf_model_path):
        """
        生成文本库tfidf计算文件
        :param dictionary_model_path: 生成的字典文件存储地址
        :param tfidf_model_path: 生成的tfidf模型存储地址
        :return:
        """
        dictionary = corpora.Dictionary.load(dictionary_model_path)
        self.tfidf_model = models.TfidfModel(dictionary=dictionary)
        docs_tfidf_list = list()
        for index, doc_str_list in enumerate(self.load_file()):
            # doc_str_list = self.cut_clearn_doc(content)
            doc_bow = self.dictionary.doc2bow(doc_str_list)
            # 生成单个文档tfidf向量
            doc_tfidf = self.tfidf_model[doc_bow]
            docs_tfidf_list.append(doc_tfidf)
        # 生成整个文档库的tfidf模型文件
        corpora.MmCorpus.serialize(tfidf_model_path, docs_tfidf_list, id2word=self.dictionary)

    def generate_library_word2vector(self, word2vector_file_path, vector_size=300, window=5, min_count=5):
        """
        生成文档库的word2vector模型文件
        :param word2vector_file_path:
        :return:
        """
        begin_time = time.time()
        # initial vector model
        model = Word2Vec(self._iter_load_file(), size=vector_size, window=window, min_count=min_count,
                         workers=multiprocessing.cpu_count())
        end_time = time.time()
        process_time = end_time - begin_time
        print 'generate document library word2vector model success, using %f seconds'%process_time
        # save vector file
        model.wv.save_word2vec_format(word2vector_file_path, binary=False)

    # def _initial_calculation_model(self):
    #     pass
    def cal_document_tfidf(self, document, dictionary_model_path):
        """
        计算一篇文档所有seg的tfidf值集合
        :param document:
        :param dictionary_model_path:
        :param tfidf_model_path:
        :return:
        """
        dictionary = corpora.Dictionary.load(dictionary_model_path)
        tfidf_model = models.TfidfModel(dictionary=dictionary)
        doc_str_list = self.cut_clearn_doc(document)
        doc_bow = dictionary.doc2bow(doc_str_list)
        return tfidf_model[doc_bow]

    def cal_document_bow(self, document, dictionary_model_path):
        """
        计算一篇文档的词袋统计
        :param document:
        :param dictionary_model_path:
        :return:
        """
        dictionary = corpora.Dictionary.load(dictionary_model_path)
        tfidf_model = models.TfidfModel(dictionary=dictionary)
        doc_str_list = self.cut_clearn_doc(document)
        return dictionary.doc2bow(doc_str_list)