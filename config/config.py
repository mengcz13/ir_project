import os
import sys

# project common
ROOTDIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')

# indexing
DATADIR = os.path.join(ROOTDIR, 'data')
DATAPATH = os.path.join(DATADIR, 'CNKI_journal_v2.txt')

# solr
SOLRDIR = os.path.join(ROOTDIR, 'solr-7.2.0')
SOLRCMDPATH = os.path.join(SOLRDIR, 'bin', 'solr.cmd')
SOLRPOSTPATH = os.path.join(SOLRDIR, 'example', 'exampledocs', 'post.jar')
try:
    assert os.path.exists(SOLRDIR)
except AssertionError:
    print('Wrong path to solr! (%s)' % (SOLRDIR))
    exit(-1)
SOLRSCRIPT = os.path.join(SOLRDIR, 'bin', 'solr.cmd')
SOLRPORT = 8983
