import os
import subprocess
import config.config as conf
from preprocessing.preprocessing import generate_json


def preproc_and_create_solr_core(methodname):
    try:
        assert methodname in ['thulac', 'hmm', 'bigram', 'thulacword2vec']
    except AssertionError:
        print('Analyzing method %s not supported!' % (methodname))
        exit(-1)

    '''
    Preprocessing input file.
    
    For thulac, we use analyzer in preprocessing, which will insert spaces between analyzed words, and use space analyzer in solr.
    For hmm and bigram, we directly use built-in analyzers in solr and do not analyze here.
    '''
    json_path = generate_json(methodname)

    '''
    start solr and create the core
    '''
    core_name = 'core_' + methodname
    core_config_dir = os.path.join(conf.ROOTDIR, 'solr_conf', core_name)
    subprocess.call('%s stop -p %d' % (conf.SOLRCMDPATH, conf.SOLRPORT))  # stop solr server
    subprocess.call('%s start -p %d' % (conf.SOLRCMDPATH, conf.SOLRPORT)) # start solr server
    print('started solr at port %d' % (conf.SOLRPORT))
    subprocess.call('%s delete -c %s' % (conf.SOLRCMDPATH, core_name)) # delete core if exists
    subprocess.call('%s create_core -c %s -d %s' % (conf.SOLRCMDPATH, core_name, core_config_dir)) # create core according pre-set config files
    print('successfully created core %s!' % (core_name))

    '''
    indexing
    '''
    subprocess.call('java -Dtype=application/json -Dc=%s -Dport=%d -jar %s %s' % (core_name, conf.SOLRPORT, conf.SOLRPOSTPATH, json_path))
    print('successfully indexed core %s with data %s!' % (core_name, json_path))

    '''
    show link
    '''


if __name__ == '__main__':
    for methodname in ['hmm', 'bigram']:
        preproc_and_create_solr_core(methodname)
    # start Flask server