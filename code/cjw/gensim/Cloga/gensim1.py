# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, models, similarities
print 'first method of applying gensim to analysis document'
documents = ["Human machine interface for lab abc computer applications",
              "A survey of user opinion of computer system response time",
              "The EPS user interface management system",
              "System and human system engineering testing of EPS",
              "Relation of user perceived response time to error measurement",
              "The generation of random binary unordered trees",
              "The intersection graph of paths in trees",
              "Graph minors IV Widths of trees and well quasi ordering",
              "Graph minors A survey"]
# remove common words and tokenize
stoplist = set('for a of the and to in'.split())
texts = [[word for word in document.lower().split() if word not in stoplist]
          for document in documents]
# remove words that appear only once
all_tokens = sum(texts, [])
tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
texts = [[word for word in text if word not in tokens_once]
          for text in texts]
print texts
print 'create dictionary'
dictionary = corpora.Dictionary(texts)
dictionary.save('/tmp/deerwester.dict') # store the dictionary, for future reference
print dictionary
print dictionary.token2id
print 'example:map input document with specific id'
new_doc = "Human computer interaction"
new_vec = dictionary.doc2bow(new_doc.lower().split())#函数doc2bow()只是计算每个唯一的词的出现频率
print new_vec # the word "interaction" does not appear in the dictionary and is ignored
print 'create corpus'
corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('/tmp/deerwester.mm', corpus) # store to disk, for later use
print corpus

print 'second method of applying gensim to analysis document'
# collect statistics about all tokens
dictionary = corpora.Dictionary(line.lower().split() for line in open('/tmp/mycorpus.txt'))
# remove stop words and words that appear only once
stop_ids = [dictionary.token2id[stopword] for stopword in stoplist
           if stopword in dictionary.token2id]
once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems()if docfreq == 1]
dictionary.filter_tokens(stop_ids + once_ids) # remove stop words and words that appear only once
dictionary.compactify() # remove gaps in id sequence after words that were removed
print dictionary
#define myCorpus
class MyCorpus(object):
     def __iter__(self):
         for line in open('/tmp/mycorpus.txt'):
             # assume there's one document per line, tokens separated by whitespace
             yield dictionary.doc2bow(line.lower().split())

corpus_memory_friendly = MyCorpus() # doesn't load the corpus into memory!
print corpus_memory_friendly
for vector in corpus_memory_friendly: # load one vector into memory at a time
    print vector
print 'serialize corpus'
corpora.MmCorpus.serialize('/tmp/corpus.mm', corpus_memory_friendly)
corpora.SvmLightCorpus.serialize('/tmp/corpus.svmlight', corpus_memory_friendly)
corpora.BleiCorpus.serialize('/tmp/corpus.lda-c', corpus_memory_friendly)
# corpora.LowCorpus.serialize('/tmp/corpus.low', corpus_memory_friendly)
print 'read corpus from disk'
corpus1 = corpora.MmCorpus('/tmp/corpus.mm')
print corpus1
