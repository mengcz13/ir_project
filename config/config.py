import os
import sys

# project common
ROOTDIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')

# indexing
DATAPATH = os.path.join(ROOTDIR, 'data', 'CNKI_journal_v2.txt')

# solr
SOLRDIR = r'C:\Users\Mengcz\AppData\Local\solr-7.2.0'
try:
    assert os.path.exists(SOLRDIR)
except AssertionError:
    print('Wrong path to solr! (%s)' % (SOLRDIR))
    exit(-1)
SOLRSCRIPT = os.path.join(SOLRDIR, 'bin', 'solr.cmd')
PORT = 8983
UPDATE_ENDPOINT = 'http://%s:%d/solr/%s/update' # %(hostname, port, core_name)

