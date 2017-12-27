import os
import config.config as conf
import json

import thulac
from gensim.models.keyedvectors import KeyedVectors


keynames = '文件名 题名 作者 第一责任人 单位 来源 关键词 摘要 出版日期'.split(' ')
fieldnames = 'id title_cn author_cn first_auth inst src keyw_cn abs_cn date'.split(' ')
multiValuedFields = 'author_cn inst keyw_cn'.split(' ')
analyzedFields = 'title_cn inst src keyw_cn abs_cn'.split(' ')
assert len(keynames) == len(fieldnames)
key2field = {}
for key, field in zip(keynames, fieldnames):
    key2field[key] = field


class BaseAnalyzer(object):
    '''
    A base analyzer to tokenize Chinese text
    '''
    def __init__(self):
        pass

    def analyze(self, text):
        raise NotImplementedError('Do not use base class!')


class ThulacAnalyzer(BaseAnalyzer):
    '''
    use thulac for tokenizing
    '''
    def __init__(self):
        super().__init__()
        self.analyzer = thulac.thulac(seg_only=True)

    def analyze(self, text):
        res = self.analyzer.cut(text)
        words = [x[0] for x in res]
        words = [x for x in words if x != '']
        return ' '.join(words)


class ThulacWord2vecAnalyzer(BaseAnalyzer):
    '''
    thulac + word2vec
    '''
    def __init__(self):
        super().__init__()
        self.analyzer = thulac.thulac(seg_only=True)
        self.wordvecs = KeyedVectors.load_word2vec_format(os.path.join(conf.DATADIR, 'pku_binary.emb'), binary=True)

    def analyze(self, text):
        res = self.analyzer.cut(text)
        words = [x[0] for x in res]
        words = [x for x in words if x != '']
        words_word2vec = []
        for word in words:
            try:
                top3sim = self.wordvecs.most_similar(word, topn=3)
                top3simwords = [x[0] for x in top3sim]
                for w in top3simwords:
                    words_word2vec.append(w)
            except KeyError:
                pass
        for w in words_word2vec:
            if w != '':
                words.append(w)
        return ' '.join(words)


def parse_data_to_json(datapath, outputpath, analyzer=None):
    with open(datapath, 'r', encoding='utf-8') as f:
        docs = []
        doc = {}
        while 1:
            line = f.readline()
            if line == '':
                docs.append(doc)
                break
            line = line.rstrip('\r\n')
            if line == '<REC>':
                if doc != {}:
                    docs.append(doc)
                doc = {}
                continue
            # print(line)
            splitline = line.split(sep='=', maxsplit=1)
            if len(splitline) < 2:
                continue
            key, value = splitline
            key = key[1:-1]
            if key in key2field.keys():
                fieldname = key2field[key]
                if fieldname in multiValuedFields:
                    value = [x for x in value.split(';') if x != '']
                elif fieldname == 'first_auth':
                    value = value.split(';')[0]
                if fieldname == 'date':
                    value += 'T12:00:00Z'
                if (analyzer is not None) and (fieldname in analyzedFields):
                    if isinstance(value, list):
                        value = [analyzer.analyze(x) for x in value]
                    else:
                        value = analyzer.analyze(value)
                doc[fieldname] = value
        with open(outputpath, 'w', encoding='utf-8') as outf:
            json.dump(docs, outf, ensure_ascii=False)
        return docs


def generate_json(methodname):
    if methodname == 'thulac':
        json_path = os.path.join(conf.DATADIR, 'thulac.json')
        parse_data_to_json(conf.DATAPATH, json_path, analyzer=ThulacAnalyzer())
    elif methodname == 'thulacword2vec':
        json_path = os.path.join(conf.DATADIR, 'thulacword2vec.json')
        parse_data_to_json(conf.DATAPATH, json_path, analyzer=ThulacWord2vecAnalyzer())
    elif methodname in ['hmm', 'bigram']:
        json_path = os.path.join(conf.DATADIR, 'not_analyzed.json')
        parse_data_to_json(conf.DATAPATH, json_path, analyzer=None)
    return json_path


if __name__ == '__main__':
    pass