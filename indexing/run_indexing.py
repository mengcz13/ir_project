import os
import config.config as conf
import json


keynames = '文件名 题名 英文篇名 作者 英文作者 第一责任人 单位 来源 关键词 英文关键词 摘要 英文摘要 年 期 英文刊名'.split(' ')
fieldnames = 'id title_cn title_en author_cn author_en first_auth inst src keyw_cn keyw_en abs_cn abs_en year volumn src_en'.split(' ')
multiValuedFields = 'author_cn author_en first_auth inst keyw_cn keyw_en'.split(' ')
intFields = 'year'.split(' ')
assert len(keynames) == len(fieldnames)
key2field = {}
for key, field in zip(keynames, fieldnames):
    key2field[key] = field


def parse_data_to_json(datapath, analyzer=None):
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
                    if fieldname == 'author_en':
                        value = [x for x in value.split(',') if x != '']
                    else:
                        value = [x for x in value.split(';') if x != '']
                elif fieldname in intFields:
                    value = int(value)
                doc[fieldname] = value
        return docs


if __name__ == '__main__':
    docs = parse_data_to_json(conf.DATAPATH)
    with open(os.path.join('data', 'commit.json'), 'w', encoding='utf-8') as f:
        json.dump(docs, f, ensure_ascii=False)