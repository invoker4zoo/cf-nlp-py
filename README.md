# 自然语言处理python工具库

normal nlp python lib


-----

## 项目结构

* [stable](cfnlp/stable): 工具库中需要的模型静态文件存储地址
* [parser](cfnlp/parser): 文本解析方法集合
* [tools](cfnlp/tools): python常用工具方法集合
* [connector](cfnlp/tools/connector): 数据库连接方法
* [model](cfnlp/model): 自然语言处理相关模型算法

## 版本更新日志

> 版本0.1（更新时间2019-02-20）

> #### 待实现功能
>- [X] 常用工具集合
>- [ ] 文本解析方案（包括单文本的html文件和纯文本解析）
>- [ ] nlp模型工具集合
>- [X] 数据库链接方法集合

## 安装/卸载/上载方法


## 功能模块详细说明

#### [stable](cfnlp/stable): 静态文件说明
* AreaTagLibrary: 国内地点识别文件， 在jar_method中载入使用
* AbbreviationWord.txt: 国内地名缩写词识别文件，在jar_method中载入使用
* jar-jpype-connector-1.0.jar: 集成java方法中使用的jar包
* punct.py: punct(字符串), sentence_delimiters(句子分割符)

#### [parser](cfnlp/parse): 文本解析方法

* htmlParser:html类文档的解析方法

- 对html中的表格进行数据提取的方法
```

```
- 对html中的目录和主要内容进行提取的方法
```

```
* textEventGraphParser: 文档抽取关键信息并图谱化展示
```
    使用说明：
    from cfnlp.parser.text_graph_parser.event_mining import EventMining
    content = '你要分析的文本'
    handler = CrimeMining()
    handler.main(content)
    输出：项目路径下graph_show.html
```
* documentParse: 文本类文档的解析方法

#### [tools](cfnlp/tools): 常用工具说明

###### [jar_method.py](cfnlp/tools/jar_method.py):在python中集成java的部分功能函数。

- 初始化java方法类
```
    1.jvm路径加载;2.启动jvm;3.初始化方法模型
```

- 地域识别方法
```
    [get_format_area]:输入自然语言文本，识别地域并补全区域位置(省/市/区)
```

- ansj分词方法
```
    目前集成4类分词方法：1.精确分词-不去重;2.精确分词-去重;3.索引分词;4.Dic分词
    >- [text_tokenizer]: 含4类分词方法
    >- [text_tokenizer_stop]: 含4类分词方法，并激活停用词典。注：目前停用词典使用jar包内部管理，暂不支持外部加载。
    >- [text_tokenizer_user]: 含4类分词方法，支持最多2个自定义词典加载。
    >- [text_tokenizer_user_stop]: 含4类分词方法，支持最多2个自定义词典加载，并激活停用词典。注：目前停用词典使用jar包内部管理，暂不支持外部加载。
```

###### [logger.py](cfnlp/tools/logger.py): python日志工具

- 日志存储会在当前启动脚本路径下建立./log 文件夹，并以时间作为分割

```
    from cfnlp.tools.logger import logger
    logger.info('test text')
```


#### [connector](cfnlp/tools/connector): 数据库连接方法集合

- [es_connector.py](cfnlp/tools/connector/es_connector.py)elasticsearch搜索引擎连接方法
```
    # 初始化es连接
    # 需要ip, 端口, 索引名称， doc_type名称
    es_db = esConnector(url='localhost:9200', index='test', doc_type='finace')
    # 可复写es查询方法
```

- [mysql_connector.py](cfnlp/tools/connector/mysql_connector.py)mysql数据库连接方法

```
    # 初始化mysql 连接
    # 需要hostip, 用户名， 用户密码， db名， table名
    mysql_db = mysqlConnector(host='127.0.0.1', user='root', password='123456', db='db_name', table='table_name')
    # 可复写mysqlConnector类的查询方法，示例
    # def select_one_info(self, sql, sql_params):
    #     """
    #     可复写方法，查询一条数据
    #     :param sql: example:"select * from `table_name` limit %d"
    #     :param sql_params: (1000,)
    #     :return:
    #     """
    #     try:
    #         with self.connector.cursor() as cursor:
    #             cursor.execute(sql, sql_params)
    #             result = cursor.fetchone()
    #             return result
    #     except Exception, e:
    #         logger.error('select one info failed for %s' % str(e))
    #         return None
```

- [mongo_connector.py](cfnlp/tools/connector/mongo_connector.py)mongo数据库连接方法
```
    # 初始化mongo连接，需要ip地址，端口，db名，collection名
    MONGODB_SERVER = "127.0.0.1"
    MONGODB_PORT = 27017
    MONGODB_DB = "gov_finace"
    MONGODB_COLLECTION = "center"
    db = mongoConnector(MONGODB_SERVER,MONGODB_PORT,MONGODB_DB,MONGODB_COLLECTION)
```

- [neo_connector.py](cfnlp/tools/connector/neo_connector.py)neo4j图数据库连接方法
```
    # 初始化neo4j连接，需要ip地址，端口，用户名，用户密码
    neo4j_db = Neo4jConnector("bolt://localhost:7687", "neo4j", "passw0rd")
```
