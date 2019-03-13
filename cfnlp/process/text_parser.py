# coding=utf-8
"""
@ license: Apache Licence
@ github: invoker4zoo
@ author: invoker/cc
@ wechart: whatshowlove
@ software: PyCharm
@ file: text_parser.py
@ time: $19-3-8 下午5:28
"""
from cfnlp.parser.base_text_parser import BaseTextParser
from cfnlp.tools.connector.mongo_connector import mongoConnector
from cfnlp.tools.logger import logger

STOP_WORD_DIC_PATH = "/home/showlove/PycharmProjects/data_test/nlp/stop_word_dic.txt"
THUNLP_MODEL_PATH = "/home/showlove/cc/code/THULAC-Python/models"
TEXT_SAMPLE_DIR = "/home/showlove/PycharmProjects/data_test/nlp/doc/corpus_6_4000"
DICTIONARY_PATH = "/home/showlove/PycharmProjects/data_test/tmp/sample.dict"
TFIDF_PATH = "/home/showlove/PycharmProjects/data_test/tmp/tfidf_corpus/tfidf.mm"
Word2Vec_PATH = "/home/showlove/PycharmProjects/data_test/tmp/word2vector/news.vector"

class GovDocAnalysis(BaseTextParser):
    """
    继承BaseTextParser，做出财政政策库的文本属性
    """
    def load_file(self, mongo_config):
        """
        重载文档库载入函数
        :param mongo_config: MONGODB_SERVER,MONGODB_PORT,MONGODB_DB,MONGODB_COLLECTION
        :return:
        """
        try:
            mongo_connector = mongoConnector(mongo_config['MONGODB_SERVER'], mongo_config['MONGODB_PORT'],\
                                             mongo_config['gov_finace'], mongo_config['country'])
            for item in mongo_connector.collection.aggregate([{'pubTime': {'$gt': '2008-01-01'}},\
                                                              {'sort': {'pubTime': 1}}]).batch_size(1):
                content = item.get('content_text', '')
                yield content
        except Exception, e:
            logger.error('load gov document library failed for %s' % str(e))

if __name__ == '__main__':
    text_model = BaseTextParser(seg_model='jieba', config={'file_path': TEXT_SAMPLE_DIR, 'stop_word_dic_path': STOP_WORD_DIC_PATH})
    # document = """网易体育2月11日讯：2007/2008赛季CBA联赛总决赛首回合比赛将于北京时间2月13日晚7点半正式打响，首场较量华南虎广东宏远将坐镇主场迎接东北虎辽宁盼盼的挑战，比赛打到这个份上，总冠军奖杯近在咫尺，谁都不想遗憾地错过，本轮比赛，两只老虎势必会有一场殊死之战。"""
    # doc_tfidf = text_model.cal_document_tfidf(document, DICTIONARY_PATH)
    # 生成文档库的字典文件
    # text_model.generate_docs_dictionary(DICTIONARY_PATH)
    # 生成文档库的tfidf文件，需要首先生成dictionary文件
    # text_model.generate_docs_tfidf(DICTIONARY_PATH, TFIDF_PATH)
    text_model.generate_docs_dictionary(DICTIONARY_PATH)

