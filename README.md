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
>-[X] 常用工具集合
>- [ ] 文本解析方案（包括单文本的html文件和纯文本解析）
>- [ ] nlp模型工具集合
>- [X] 数据库链接方法集合

## 安装/卸载/上载方法


## 功能模块详细说明

#### [stable](cfnlp/stable): 静态文件说明
* AreaTagLibrary: 国内地点识别文件， 在jar_method中载入使用
* AbbreviationWord: 国内地名缩写词识别文件，在jar_method中载入使用
* java-knowledge-extraction-sdk-1.0.jar: 集成java方法中使用的jar包

#### [parser](cfnlp/parse): 文本解析方法

* htmlParser:html类文档的解析方法

- 对html中的表格进行数据提取的方法
```

```
- 对html中的目录和主要内容进行提取的方法
```

```

* documentParse: 文本类文档的解析方法

#### [tools](cfnlp/tools): 常用工具说明

* [jar_method.py](cfnlp/tools/jar_method.py):在python中集成java的部分功能函数。

- 初始化java方法类
```

```

- 地域识别方法
```

```

- ansj分词方法
```

```

#### [connector](cfnlp/tools/connector): 数据库连接方法集合

- [es_connector.py](cfnlp/tools/connector/es_connector.py)elasticsearch搜索引擎连接方法
```

```

- [mysql_connector.py](cfnlp/tools/connector/mysql_connector.py)mysql数据库连接方法
```

```

- [mongo_connector.py](cfnlp/tools/connector/mongo_connector.py)mongo数据库连接方法
```

```

- [neo_connector.py](cfnlp/tools/connector/neo_connector.py)neo4j图数据库连接方法
