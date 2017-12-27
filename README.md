# 2017秋《信息检索》课程大作业

基于Lucene及其服务端扩展Solr搭建检索系统，支持以下功能：
- 输入query，输出检索结果
- 支持HMM和bigram两种分词方法
- 支持多域检索，布尔检索
- 检索时支持Word2Vec

## 目录结构

```
├─config # 全局参数，包括Solr安装路径和Solr占用端口号等
├─data # 存放CNKI数据集和word2vec embedding二进制结果
├─ir_frontend # 基于Flask框架的搜索网页和预处理程序
├─preprocessing # 生成用于索引的json文件
├─solr-7.2.0 # Solr安装目录
├─solr_conf # Solr配置文件
├─.gitignore
├─build.py # 启动Solr并完成索引
└─run.ps1 # 运行build.py并启动Flask服务
```

## 运行方法

1. 下载[Solr 7.2.0](http://archive.apache.org/dist/lucene/solr/7.2.0/solr-7.2.0.zip)并解压到工程根目录；
2. 将CNKI数据集`CNKI_journal_v2.txt`和Word2Vec向量**二进制**文件`pku_binary.emb`复制到`data`文件夹下；
3. 运行`run.ps1`；
4. 打开[检索页面](http://localhost:5000/static/index.html)。

## 功能演示

### Part 1

#### 基本检索功能

下图为在系统中检索“计算机”得到的结果。支持分页查询。

![](https://github.com/mengcz13/ir_project/raw/master/doc/basic_1.JPG)
![](https://github.com/mengcz13/ir_project/raw/master/doc/basic_2.JPG)

#### HMM和bigram分词

HMM分词模型是基于隐马尔科夫模型的统计模型，bigram分词方式则是将所有汉字分成单字后取所有的bi-gram作为分词结果。下2图分别为HMM分词和bigram分词下的检索结果，可见HMM模型将“计算机”识别为一个完整的词，而bigram分词则同时检索了“计算”和“算机”。

![](https://github.com/mengcz13/ir_project/raw/master/doc/analyzer_hmm.JPG)
![](https://github.com/mengcz13/ir_project/raw/master/doc/analyzer_bigram.JPG)

### Part 2

#### 多域检索

如下图，支持限定标题，摘要，作者，出版单位，出版年份。

![](https://github.com/mengcz13/ir_project/raw/master/doc/fields.JPG)

#### 布尔检索

如下图，支持对标题的布尔检索。

![](https://github.com/mengcz13/ir_project/raw/master/doc/boolean.JPG)

#### 与Word2Vec结合

实现时将待检索词及其TOP 3相似词输入检索系统，实现与Word2Vec的结合。如下图，未启用Word2Vec时，查询“电脑”仅得到“电脑”的结果；启用Word2Vec时，查询“电脑”可同时得到“电脑”与“计算机”的结果。

![](https://github.com/mengcz13/ir_project/raw/master/doc/word2vec_false.JPG)
![](https://github.com/mengcz13/ir_project/raw/master/doc/word2vec_true.JPG)

## 具体实现

### 整体架构

前端查询页面 -> Flask后端初步处理查询请求并结合Word2Vec -> Solr后端检索并返回结果

### 分词

直接使用Solr内置的分词类实现。

### Word2Vec

Word2Vec词向量由[wang2vec](https://github.com/wlin12/wang2vec)在人民日报语料库上通过如下参数训练得到。

```
./word2vec -train input_file -output embedding_file -type 0 -size 50 -window 5 -negative 10 -nce 0 -hs 0 -sample 1e-4 -threads 1 -binary 1 -iter 1000 -cap 0
```

对输入的检索词在Flask端进行处理后再转发给Solr查询系统。Flask端的分词采用[THULAC](https://github.com/thunlp/THULAC-Python)，查找TOP N邻近词采用[gensim](https://radimrehurek.com/gensim/models/word2vec.html).
