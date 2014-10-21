# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora, models, similarities
dictionary = corpora.Dictionary.load('/tmp/deerwester.dict')
corpus = corpora.MmCorpus('/tmp/deerwester.mm')
print 'corpus'
for doc in corpus:
    print doc

tfidf = models.TfidfModel(corpus) # 第一步--初始化一个模型
print tfidf
corpus_tfidf = tfidf[corpus]
for doc in corpus_tfidf:
    print doc