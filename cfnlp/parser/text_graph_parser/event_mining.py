# -*- coding:utf-8 -*-
# @Time     : 2019/2/21 15:08
# @Author   : Tanrui
# @Email    : cq_tanrui@163.com
# @File     : event_mining.py
# @Software : PyCharm
# @Desc     :

import re
from cfnlp.parser.text_graph_parser.ltp_parser import *
from collections import Counter
from cfnlp.parser.text_graph_parser.graph_show import *
from cfnlp.parser.text_graph_parser.graph_textrank import *

'''事件挖掘'''
class EventMining:
    def __init__(self,ltp_model_dir):
        self.textranker = TextRank()
        self.parser = LtpParser(ltp_model_dir)
        self.ners = ['nh', 'ni', 'ns', 'nt']
        self.ner_dict = {
        'nh':'人物',
        'ni':'机构',
        'ns':'地名',
        'nt':'时间'
        }
        self.graph_shower = GraphShow()

    '''移除括号内的信息，去除噪声'''
    def remove_noisy(self, content):
        p1 = re.compile(r'（[^）]*）')
        p2 = re.compile(r'\([^\)]*\)')
        return p2.sub('', p1.sub('', content))

    '''收集命名实体'''
    def collect_ners(self, words, postags):
        ners = []
        for index, pos in enumerate(postags):
            if pos in self.ners:
                ners.append(words[index] + '/' + pos)
        return ners

    '''对文章进行分句处理'''
    def seg_content(self, content):
        return [sentence for sentence in re.split(r'[？?！!。；;：:\n\r]', content) if sentence]

    '''对句子进行分词，词性标注处理'''
    def process_sent(self, sent):
        words, postags = self.parser.basic_process(sent)
        return words, postags

    '''构建实体之间的共现关系'''
    def collect_coexist(self, ner_sents, ners):
        co_list = []
        for sent in ner_sents:
            words = [i[0] + '/' + i[1] for i in zip(sent[0], sent[1])]
            co_ners = set(ners).intersection(set(words))
            co_info = self.combination(list(co_ners))
            co_list += co_info
        if not co_list:
            return []
        return {i[0]:i[1] for i in Counter(co_list).most_common()}

    '''列表全排列'''
    def combination(self, a):
        combines = []
        if len(a) == 0:
            return []
        for i in a:
            for j in a:
                if i == j:
                    continue
                combines.append('@'.join([i, j]))
        return combines

    '''抽取出事件三元组'''
    def extract_triples(self, words, postags):
        svo = []
        tuples, child_dict_list = self.parser.parser_main(words, postags)
        for tuple in tuples:
            rel = tuple[-1]
            if rel in ['SBV']:
                sub_wd = tuple[1]
                verb_wd = tuple[3]
                obj = self.complete_VOB(verb_wd, child_dict_list)
                subj = sub_wd
                verb = verb_wd
                if not obj:
                    svo.append([subj, verb])
                else:
                    svo.append([subj, verb+obj])
        return svo

    '''过滤出与命名实体相关的事件三元组'''
    def filter_triples(self, triples, ners):
        ner_triples = []
        for ner in ners:
            for triple in triples:
                if ner in triple:
                    ner_triples.append(triple)
        return ner_triples

    '''根据SBV找VOB'''
    def complete_VOB(self, verb, child_dict_list):
        for child in child_dict_list:
            wd = child[0]
            attr = child[3]
            if wd == verb:
                if 'VOB' not in attr:
                    continue
                vob = attr['VOB'][0]
                obj = vob[1]
                return obj
        return ''

    '''对文章进行关键词挖掘'''
    def extract_keywords(self, words_list):
        return self.textranker.extract_keywords(words_list, 10)

    '''基于文章关键词，建立起实体与关键词之间的关系'''
    def rel_entity_keyword(self, ners, keyword, subsent):
        events = []
        rels = []
        sents = []
        ners = [i.split('/')[0] for i in set(ners)]
        keyword = [i[0] for i in keyword]
        for sent in subsent:
            tmp = []
            for wd in sent:
                if wd in ners + keyword:
                    tmp.append(wd)
            if len(tmp) > 1:
                sents.append(tmp)
        for ner in ners:
            for sent in sents:
                if ner in sent:
                    tmp = ['->'.join([ner, wd]) for wd in sent if wd in keyword and wd != ner and len(wd) > 1]
                    if tmp:
                        rels += tmp
        for e in set(rels):
            events.append([e.split('->')[0], e.split('->')[1]])
        return events


    '''利用标点符号，将文章进行短句切分处理'''
    def seg_short_content(self, content):
        return [sentence for sentence in re.split(r'[，,？?！!。；;：:\n\r\t ]', content) if sentence]

    '''挖掘主控函数'''
    def main(self, content):
        if not content:
            return []
        # 对文章进行去噪处理
        content = self.remove_noisy(content)
        # 对文章进行长句切分处理
        sents = self.seg_content(content)
        # 对文章进行短句切分处理
        subsents = self.seg_short_content(content)
        subsents_seg = []
        # words_list存储整篇文章的词频信息
        words_list = []
        # ner_sents保存具有命名实体的句子
        ner_sents = []
        # ners保存命名实体
        ners = []
        # triples保存主谓宾短语
        triples = []
        # 存储文章事件
        events = []
        for sent in subsents:
            words, postags = self.process_sent(sent)
            words_list += [[i[0], i[1]] for i in zip(words, postags)]
            subsents_seg.append([i[0] for i in zip(words, postags)])
            ner = self.collect_ners(words, postags)
            if ner:
                triple = self.extract_triples(words, postags)
                if not triple:
                    continue
                triples += triple
                ners += ner
                ner_sents.append([words, postags])

        # 获取文章关键词, 并图谱组织, 这个可以做
        keywords = [i[0] for i in self.extract_keywords(words_list)]
        for keyword in keywords:
            name = keyword
            cate = '关键词'
            events.append([name, cate])
        # 对三元组进行event构建，这个可以做
        for t in triples:
            if (t[0] in keywords or t[1] in keywords) and len(t[0]) > 1 and len(t[1]) > 1:
                events.append([t[0], t[1]])

        # 获取文章词频信息话，并图谱组织，这个可以做
        word_dict = [i for i in Counter([i[0] for i in words_list if i[1][0] in ['n', 'v'] and len(i[0]) > 1]).most_common()][:10]
        for wd in word_dict:
            name = wd[0]
            cate = '高频词'
            events.append([name, cate])

        #　获取全文命名实体，这个可以做
        ner_dict = {i[0]:i[1] for i in Counter(ners).most_common()}
        for ner in ner_dict:
            name = ner.split('/')[0]
            cate = self.ner_dict[ner.split('/')[1]]
            events.append([name, cate])

        # 获取全文命名实体共现信息,构建事件共现网络
        co_dict = self.collect_coexist(ner_sents, list(ner_dict.keys()))
        co_events = [[i.split('@')[0].split('/')[0], i.split('@')[1].split('/')[0]] for i in co_dict]
        events += co_events
        #将关键词与实体进行关系抽取
        events_entity_keyword = self.rel_entity_keyword(ners, keywords, subsents_seg)
        events += events_entity_keyword
        #对事件网络进行图谱化展示
        self.graph_shower.create_page(events)