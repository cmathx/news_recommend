# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

from gensim import corpora, models, similarities
import logging

print '准备工作'
logging.basicConfig(format=' %(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

print '文档输入'
documents = ["Shipment of gold damaged in a fire",\
             "Delivery of silver arrived in a silver truck",\
             "Shipment of gold arrived in a truck"]
print '文档单词分割'
texts = [[word for word in document.lower().split()] for document in documents]
print texts
print '建立词袋（bag of words）'
dictionary = corpora.Dictionary(texts)
print dictionary
print '将文档的token映射为id'
print dictionary.token2id
print '用符串表示的文档转换用id表示的文档向量'
corpus = [dictionary.doc2bow(text) for text in texts]
print corpus
print '基于训练文档计算一个TF-IDF模型'
tfidf = models.TfidfModel(corpus)
print '基于TF-IDF模型计算出TF-IDF矩阵'
corpus_tfidf = tfidf[corpus]
for doc in corpus_tfidf:
    print doc
print tfidf.dfs
print tfidf.idfs

print '训练LSI模型'
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)
lsi.print_topics(2)
print '基于LSI模型计算文档和主题的相关性'
corpus_lsi = lsi[corpus_tfidf]
for doc in corpus_lsi:
    print doc

print '训练LDA模型'
lda = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=2)
lda.print_topics(2)
print '基于LDA模型计算文档和主题的相关性'
corpus_lda = lda[corpus_tfidf]
for doc in corpus_lda:
    print doc

print '建立索引'
index = similarities.MatrixSimilarity(lsi[corpus])
print '查询文档向量化'
query = 'gold silver truck'
query_bow = dictionary.doc2bow(query.lower().split())
print query_bow
print '用之前训练好的LSI模型将其映射到二维的topic空间'
query_lsi = lsi[query_bow]
print query_lsi
print '计算其和index中doc的余弦相似度'
sims = index[query_lsi]
print list(enumerate(sims))
print '按照相似度进行排序'
sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
print sort_sims