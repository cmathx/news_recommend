# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

print '打开coursera课程训练数据'
courses = [line.strip() for line in file('coursera_corpus')]
courses_name = [course.split('\t')[0] for course in courses]
print courses_name[0:10]

print '引入NLTK'
import nltk
# nltk.download()

print '测试brown语料库'
from nltk.corpus import brown
print brown.readme()
print brown.words()[0:10]
print brown.tagged_words()[0:10]
print len(brown.words())

print '单词最小化'
texts_lower = [[word for word in document.lower().split()] for document in courses]
print texts_lower[0]
print '对课程的英文数据进行 tokenize'
from nltk.tokenize import word_tokenize
texts_tokenized = [[word.lower() for word in word_tokenize(document)] for document in courses]
print texts_tokenized[0]
print '过滤课程语料中的停用词'
from nltk.corpus import stopwords
english_stopwords = stopwords.words('english')
print english_stopwords
texts_filtered_stopwords = [[word for word in document if not word in english_stopwords] for document in texts_tokenized]
print texts_filtered_stopwords[0]
print '去除标点符号'
english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']
texts_filtered = [[word for word in document if not word in english_punctuations] for document in texts_filtered_stopwords]
print texts_filtered[0]
print '英文单词词干化（Stemming)'
from nltk.stem.lancaster import LancasterStemmer
print 'stemming 测试'
st = LancasterStemmer()
print st.stem('stemmed')
print st.stem('stemming')
print st.stem('stemmer')
print st.stem('running')
print st.stem('maximum')
print st.stem('presumably')

texts_stemmed = [[st.stem(word) for word in docment] for docment in texts_filtered]
print texts_stemmed[0]

print '去掉在预料库中出现次数为1的低频词'
all_stems = sum(texts_stemmed, [])
stems_once = set(stem for stem in set(all_stems) if all_stems.count(stem) == 1)
texts = [[stem for stem in text if stem not in stems_once] for text in texts_stemmed]

print '引入gensim进行计算'
from gensim import corpora, models, similarities
import logging
logging.basicConfig(format=' %(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
print '训练topic数量为10的LSI 模型'
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=10)

print '建立基于LSI模型的课程索引,并以Andrew Ng的机器学习公开课为例，通过lsi模型将这门课程映射到10个topic主题模型空间上,然后计算和其他课程计算相似度'
index = similarities.MatrixSimilarity(lsi[corpus])
print courses_name[210] # Machine Learning
ml_course = texts[210]
ml_bow = dictionary.doc2bow(ml_course)
ml_lsi = lsi[ml_bow]
print ml_lsi
sims = index[ml_lsi]
sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
print sort_sims[0:10]