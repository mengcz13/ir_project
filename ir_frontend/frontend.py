from flask import Flask
from flask import abort, redirect, url_for, request, Response
import requests
import os
import thulac
from gensim.models.keyedvectors import KeyedVectors
app = Flask(__name__)


SOLRPORT = 8983
ROOTDIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
DATADIR = os.path.join(ROOTDIR, 'data')
thu1 = thulac.thulac(seg_only=True)
wordvecs = KeyedVectors.load_word2vec_format(os.path.join(DATADIR, 'pku_binary.emb'), binary=True)


@app.route('/')
def index():
    return redirect(url_for('static', filename='index.html'))

@app.route('/static/select/', methods=['GET'])
def search():
    payload = request.args
    analyzer = payload['analyzer']
    word2vecflag = (payload['word2vecflag'] == 'true')
    qtext = payload['q']
    payloadnew = {}
    for k, v in payload.items():
        if k not in ['analyzer', 'true']:
            payloadnew[k] = v

    # only turn word2vec on for default field
    if word2vecflag is True and qtext != '':
        qtextsplit = [x[0] for x in thu1.cut(qtext) if x[0] != '']
        qtextnew = []
        for word in qtextsplit:
            try:
                top3sim = wordvecs.most_similar(word, topn=3)
                top3simwords = [x[0] for x in top3sim]
                for w in top3simwords:
                    qtextnew.append(w)
            except KeyError:
                pass
        for word in qtextsplit:
            qtextnew.append(word)
        payloadnew['q'] = ' '.join(qtextnew)

    r = requests.get('http://localhost:%d/solr/%s/select' % (SOLRPORT, 'core_' + analyzer), params=payloadnew)
    return r.text