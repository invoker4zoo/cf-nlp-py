# coding=utf-8
"""
@ license: Apache Licence
@ github: invoker4zoo
@ author: invoker/cc
@ wechart: whatshowlove
@ software: PyCharm
@ file: document_analysis.py
@ time: $19-3-4 下午5:05
"""
import json
import sys
from cfnlp.tools.logger import logger
reload(sys)
sys.setdefaultencoding('utf-8')


class BaseDocumentAnalysis(object):

    def __init__(self, config_path):
        """
        初始化类， 读入配置文件
        :param config_path:
        """
        try:
            with open(config_path, 'rb') as f:
                self.config = json.loads(f.read())
        except Exception, e:
            logger.error('loading config file failed for %s' % str(e))
            sys.exit(1)

    def _config_router(self):
        """
        解析配置文件，  使用配置文件进行读入、筛选、解析等
        :return:
        """
        try:
            # initial result
            self.result = dict()

            # loading info part
            # loading analysis file
            self.loading_info = self.config['loadingInfo']
            for key in self.loading_info.keys():
                pass
            # get loading format
            self.loading_format = self.loading_info['loadingFormat']
            # get loading type document/library
            self.loading_type = self.loading_info['type']
            # get loading document format
            self.loading_document_format = self.loading_info['documentFormat']
            # loading function
            self.loading_function = self.loading_info['function']
            # get loading result
            self.loading = eval(self.loading_function)({

            })

            # basic info part
            self.basic_info = self.config['basicInfo']
            # process name
            self.process_name = self.basic_info['processName']

            # method routing
            # route keys beyond loadingInfo and basicInfo
            for key in self.config.keys():
                if key not in ['basicInfo', 'loadingInfo']:
                    pass
                else:
                    pass

        except Exception, e:
            logger.error('analysis config file failed for %s' % str(e))

    def _check_config_valid(self):
        """
        判断config文件的有效性
        :return:
        """
        try:
            # 1.检查字段完整性（basicInfo, loadingInfo）
            if 'basicInfo' in self.config.keys() and 'loadingInfo' in self.config.keys():
                pass
            else:
                return False
            # 2. 检查字段中配置完整性, [function]
            for key in self.config.keys():
                if key not in ['basicInfo', 'loadingInfo']:
                    if self.config[key].get('function'):
                        pass
                    else:
                        return False
                else:
                    if self.config[key].get('function'):
                        pass
                    else:
                        return False
                    if self.config[key].get('type'):
                        pass
                    else:
                        return False
                    if self.config[key].get('documentFormat'):
                        pass
                    else:
                        return False
            return True
        except Exception, e:
            logger.error('check config file valid failed for %s' % str(e))
            return False