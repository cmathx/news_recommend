# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-
import logging

from gensim import corpora, models, similarities

from cjw.CF.Rate import getUserItemRate
from cjw.CF.ItemCF import *
from cjw.PLSA.plsaRecommend import createDocMapAndClickInfo
import plsaForNewsCluster


print '准备工作'
logging.basicConfig(format=' %(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

print '建立doc映射表'
doc_set_file = '../PLSA/data/document.csv'
total_set_file = '../../data/total_set.txt'
user_set, doc_set, doc_map_r2v, doc_map_v2r, doc_click_count, user_doc_click_count = \
    createDocMapAndClickInfo(total_set_file, doc_set_file)

#############################################################################################
print '计算文档相似度开始！'
fp_doc_set = open(doc_set_file, 'r')

print '中文分词提取开始！'

print '中文分词'
corpus = plsaForNewsCluster.Corpus()
original_texts = []
title_no_key_word = 0
content_no_key_word = 0
for line in fp_doc_set:
    ele = line.split('\t')
    document = plsaForNewsCluster.Document(ele[1], ele[2])  #prepare words which has been segmented
    title_tag, content_tag = document.split()
    if title_tag == False:
        title_no_key_word += 1
    if content_no_key_word == False:
        content_no_key_word += 1
    corpus.add_document(document)
    original_texts.append(document.title_words)
print '标题没有提取出关键字有%d个' %title_no_key_word
print '正文没有提取出关键字有%d个' %content_no_key_word

print 'write news title and content start'
fp_title_set = open('/tmp/title.csv', 'w')
fp_content_set = open('/tmp/content.csv', 'w')
for doc in corpus.documents:
    tag = True
    for word in doc.getTitleKeyWords():
        if tag == True:
            tag = False
        else:
            fp_title_set.write('\t')
        fp_title_set.write('%s' %word)
    fp_title_set.write('\n')
    # fp_title_set.write(str(unicode(doc.getTitleKeyWords(), 'gbk')) + '\n')
for doc in corpus.documents:
    tag = True
    for word in doc.getContentKeyWords():
        if tag == True:
            tag = False
        else:
            fp_content_set.write('\t')
        fp_content_set.write('%s' %word)
    fp_content_set.write('\n')
    # fp_title_set.write(str(unicode(doc.getContentKeyWords(), 'gbk')) + '\n')
fp_title_set.close()
fp_content_set.close()
print 'write news title and content end'

'''
LOW_FREQUENCE = 50
print '去掉在预料库中出现次数小于等于LOW_FREQUENCE的低频词'
word_occur = {}
for text in original_texts:
    for word in text:
        word_occur.setdefault(word, 0)
        word_occur[word] += 1
stems_low_occur = set()
for word in word_occur:
    if word_occur[word] < LOW_FREQUENCE:
        stems_low_occur.add(word)
# all_stems = sum(original_texts, [])
# stems_low_occur = set(stem for stem in set(all_stems) if all_stems.count(stem) < LOW_FREQUENCE)
texts = [[stem for stem in text if stem not in stems_low_occur] for text in original_texts]
'''
print '中文分词提取结束'

texts = original_texts
print '建立TF-IDF模型'
print '建立词袋（bag of words）'
dictionary = corpora.Dictionary(texts)
print dictionary
dictionary.save('data/news.dict') # store the dictionary, for future reference
print '将文档的token映射为id'
print dictionary.token2id
print '用符串表示的文档转换用id表示的文档向量'
corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('data/news.mm', corpus) # store to disk, for later use
for doc in corpus:
    print doc
fp_word_news_rate = open('../../data/word_news_rate.csv', 'w')
cnt = 0
for doc in corpus:
    news_id = doc_map_v2r[cnt]
    cnt += 1
    for tup in doc:
        fp_word_news_rate.write('%s\t%s\t%s\n' %(tup[0], news_id, tup[1]))
fp_word_news_rate.close()
print cnt

icfRecommend(user_set)
# print '基于训练文档计算一个TF-IDF模型'
# tfidf = models.TfidfModel(corpus)
# print '基于TF-IDF模型计算出TF-IDF矩阵'
# corpus_tfidf = tfidf[corpus]
# for doc in corpus_tfidf:
#     print doc
# print tfidf.dfs
# print tfidf.idfs

'''
print '训练LSI模型'
topic_num = 5
print 'topic数量:%d' %topic_num
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=topic_num)
lsi.print_topics(topic_num)
print '基于LSI模型计算文档和主题的相关性'
corpus_lsi = lsi[corpus_tfidf]
# for doc in corpus_lsi:
#     print doc

print '建立索引'
index = similarities.MatrixSimilarity(lsi[corpus])
'''

'''
print '训练LDA模型'
topic_num = 6
print 'topic数量:%d' %topic_num
lda = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=topic_num)
lda.print_topics(topic_num)
print '基于LDA模型计算文档和主题的相关性'
corpus_lda = lda[corpus_tfidf]
'''

# fp_lda_doc_pro = open('data/lda_doc_probability.csv', 'w')
# cnt = 0
# for doc in corpus_lda:
#     doc.sort(key=lambda d: d[1], reverse=True)
#     # print type(doc)
#     # print type(doc[1])
#     fp_lda_doc_pro.write('%s\n' %doc)
#     # print len(doc), len(doc[0])
#     if len(doc) == 10 and doc[0][1] + doc[1][1] >= 0.8:
#         cnt += 1
# fp_lda_doc_pro.close()
# print 'cnt = ', cnt

'''
print '建立索引'
index = similarities.MatrixSimilarity(lda[corpus_tfidf])


length = len(texts)
sims_arr = []
for i in xrange(length):
    text_bow = dictionary.doc2bow(texts[i])
    text_lsi = lda[text_bow]
    sims = index[text_lsi]
    sims_arr.append(sims)
print '计算文档相似度结束！'
#############################################################################################

print '基于item based的协同过滤'
# getUserItemRate()
print '读入用户和news的交互行为记录'
itemBasedCF = ItemBasedCF('../../data/user_item_rate.csv', '')
print '求解news的相似度'
itemBasedCF.ItemSimilarity()
itemBasedCF.ItemSimilarityByTopicModel(sims_arr, doc_map2)
# itemBasedCF.FinalItemSimilarity(doc_map2)
print '基于item based进行推荐'
K = 10000 #最近邻的文档数量
N = 1 #推荐数量
fp_recommend_set = open('../../recommend/itemBasedRecomemndWithTopicModel.csv', 'w')
# fp_recommend_set = open('/home/cmathx/Desktop/itemBasedRecomemndCombineLDA.csv', 'w')
fp_recommend_set.write('userid,newsid\n')
for user_id in user_set:
    recommend_news = itemBasedCF.Recommend(user_id, K, N)
    for recommend_news_id in recommend_news:
        fp_recommend_set.write('%s,%s\n' %(user_id, recommend_news_id))

# print '查询文档向量化'
# query = 'gold silver truck'
# query_bow = dictionary.doc2bow(query.lower().split())
# print query_bow
# print '用之前训练好的LSI模型将其映射到二维的topic空间'
# query_lsi = lsi[query_bow]
# print query_lsi
# print '计算其和index中doc的余弦相似度'
# sims = index[query_lsi]
# print list(enumerate(sims))
# print '按照相似度进行排序'
# sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
# print sort_sims
'''
