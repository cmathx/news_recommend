# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-
import math
import re
import numpy as np
from utils import normalize

"""
Author:
Alex Kong (https://github.com/hitalex)

Reference:
http://blog.tomtung.com/2011/10/plsa
"""

np.set_printoptions(threshold='nan')


def split(paragraph):
    words = []
    # print paragraph
    count = 0
    paragraph = paragraph.split(' ')
    for w in paragraph:
        # print w
        word = w.split('/')
        if len(word) >= 2 and len(word[1]) > 0:# and len(word[0]) >= 4:  #only consider Noun and the length of this Noun must be greater than 1
            # if word[1][0] == 'n':
            words.append(word[0])
            count += 1
    if count == 0:
        print '没有关键词被提取出来！'
    return words

class Document(object):

    '''main element in Document
    #filepath, file, lines, words
    '''

    '''
    Splits a text file into an ordered list of words.
    '''

    # List of punctuation characters to scrub. Omits, the single apostrophe,
    # which is handled separately so as to retain contractions.
    # PUNCTUATION = ['(', ')', ':', ';', ',', '-', '!', '.', '?', '/', '"', '*']

    # Carriage return strings, on *nix and windows.
    # CARRIAGE_RETURNS = ['\n', '\r\n']

    # Final sanity-check regex to run on words before they get
    # pushed onto the core words list.
    # WORD_REGEX = "^[a-z']+$"

    def __init__(self, title, content):
        '''
        Set source file location, build contractions list, and initialize empty
        lists for lines and words.
        '''
        self.title = title
        self.content = content
        self.words = []#the clean words of this document


    def split(self):
        '''
        Split file into an ordered list of words. Scrub out punctuation;
        lowercase everything; preserve contractions; disallow strings that
        include non-letters.
        '''
        # self.title_words = split(self.title)
        self.content_words = split(self.content)

class Corpus(object):

    #words in the corpus can be seen as features

    '''
    A collection of documents.
    '''

    def __init__(self):
        '''
        Initialize empty document list.
        '''
        self.documents = [] # documents


    def add_document(self, document):
        '''
        Add a document to the corpus.
        '''
        self.documents.append(document)

    #build corpus for all total documents
    def build_vocabulary(self):
        '''
        Construct a list of unique words in the corpus.
        '''
        # ** ADD ** #
        # exclude words that appear in 90%+ of the documents
        # exclude words that are too (in)frequent
        discrete_set = set()
        word_occurs = {}
        for document in self.documents:
            for word in document.content_words:
                word_occurs.setdefault(word, 0)
                word_occurs[word] += 1
            # for word in document.content_words:
            #     discrete_set.add(word)
        for word in word_occurs:
            if word_occurs[word] >= 200:
                discrete_set.add(word)
        self.main_vocabulary = list(discrete_set) #unique words in the corpus

    '''
    extract important words
    compute reverse_word_title and reverse_word_content
    (reverse_word_title: number of title which contains specific word
     reverse_word_content: number of content which contains specific word)
    '''
    def extract_main_vocabulary(self, number_of_main_words):
        main_discret_set = set()
        self.reverse_word_title = {}
        for t_doc in self.documents:
            t_set = set()
            for word in t_doc.title_words:
                self.reverse_word_title.setdefault(word, 0)
                if word not in t_set:
                    self.reverse_word_title[word] += 1
                    t_set.add(word)
        for w, num in sorted(self.reverse_word_title.items(), key=lambda d:d[1], reverse=True)[0:number_of_main_words]:
            main_discret_set.add(w)
        # self.reverse_word_content = {}
        # for t_doc in self.documents:
        #     t_set = set()
        #     for word in t_doc.content_words:
        #         self.reverse_word_content.setdefault(word, 0)
        #         if word not in t_set:
        #             self.reverse_word_content[word] += 1
        #             t_set.add(word)
        # for w, num in sorted(self.reverse_word_content.items(), key=lambda d:d[1], reverse=True)[0:number_of_main_words]:
        #     main_discret_set.add(w)
        self.main_vocabulary = list(main_discret_set)


    def plsa(self, number_of_topics, max_iter, number_of_main_words):

        '''
        Model topics.
        '''
        print "EM iteration begins..."
        # Get vocabulary and number of documents.
        # self.extract_main_vocabulary(number_of_main_words)
        number_of_documents = len(self.documents)
        vocabulary_size = len(self.main_vocabulary)

        # print "Main vocabulary size:" + str(vocabulary_size)

        #build IDF(Inverse Document Frequency) Matrix

        #TF(Term Frequence) Matrix
        # build term-doc matrix(numbers of specific word occurring in this document)
        # fp_term_doc = open('data//term_doc_matrix.csv', 'w')
        fp_main_vocabulary = open('data//main_vocabulary.csv', 'w')
        for v in self.main_vocabulary:
            fp_main_vocabulary.write('%s\n' %v)
        fp_main_vocabulary.close()
        # total_zero_count = 0
        import datetime
        starttime = datetime.datetime.now()
        print "build IF Matrix start"
        term_doc_matrix = np.zeros([number_of_documents, vocabulary_size], dtype = np.float)
        for d_index, doc in enumerate(self.documents):
            #compute tf-idf matrix only considering word in news content
            term_count = np.zeros(vocabulary_size, dtype = np.int)
            term_doc_tf_idf = np.zeros(vocabulary_size, dtype = np.float)
            for word in doc.content_words:
                if word in self.main_vocabulary:
                    w_index = self.main_vocabulary.index(word)
                    term_count[w_index] += 1
                    # term_doc_tf_idf[w_index] = 1.0 * term_count[w_index] / len(doc.content_words) * \
                    #                            math.log(1.0 * number_of_documents / (1.0 * (self.reverse_word_content[word] + self.reverse_word_title[word]) / 2 + 1))
            # for word in doc.content_words:
            #     if word in self.main_vocabulary:
            #         w_index = self.main_vocabulary.index(word)

            # term_doc_matrix[d_index] = term_doc_tf_idf
            term_doc_matrix[d_index] = term_count

            # max_doc_term = max(term_doc_matrix[d_index])
            # max_doc_tf_idf = max(term_doc_matrix[d_index])

            #amplify weight of title word(add the max tf-idf value in this document)
            # for word in doc.title_words:
            #     if word in self.main_vocabulary:
            #         w_index = self.main_vocabulary.index(word)
            #         term_doc_matrix[d_index][w_index] += max_doc_term
            # flag = True
            # for i in xrange(vocabulary_size):
            #     fp_term_doc.write('%d ' %term_doc_matrix[d_index][i])
            #     if term_doc_matrix[d_index][i] != 0:
            #         flag = False
            # if flag:
            #     total_zero_count += 1
            # fp_term_doc.write('\n')

        # fp_term_doc.close()
        # print '%d total zero bug!' %total_zero_count

        print "build IF Matrix end"
        endtime = datetime.datetime.now()
        minutes = (endtime - starttime).seconds / 60
        print "build TF Matrix costs %d minutes and %d seconds" %(minutes, (endtime - starttime).seconds - minutes * 60)

        # Create the counter arrays.
        starttime = datetime.datetime.now()
        self.document_topic_prob = np.zeros([number_of_documents, number_of_topics], dtype=np.float) # P(z | d)  z;topic d:document
        self.topic_word_prob = np.zeros([number_of_topics, len(self.main_vocabulary)], dtype=np.float) # P(w | z)  w:word z:topic
        self.topic_prob = np.zeros([number_of_documents, len(self.main_vocabulary), number_of_topics], dtype=np.float) # P(z | d, w)

        # Initialize
        print "Initializing..."
        # randomly assign values
        self.document_topic_prob = np.random.random(size = (number_of_documents, number_of_topics))
        for d_index in range(len(self.documents)):
            normalize(self.document_topic_prob[d_index]) # normalize for each document
        self.topic_word_prob = np.random.random(size = (number_of_topics, len(self.main_vocabulary)))
        for z in range(number_of_topics):
            normalize(self.topic_word_prob[z]) # normalize for each topic
        # Run the EM algorithm
        for iteration in range(max_iter):
            print "Iteration #" + str(iteration + 1) + "..."
            print "E step:"
            for d_index, document in enumerate(self.documents):
                for w_index in range(vocabulary_size):
                    prob = self.document_topic_prob[d_index, :] * self.topic_word_prob[:, w_index]
                    if sum(prob) == 0.0:
                        print "d_index = " + str(d_index) + ",  w_index = " + str(w_index)
                        print "self.document_topic_prob[d_index, :] = " + str(self.document_topic_prob[d_index, :])
                        print "self.topic_word_prob[:, w_index] = " + str(self.topic_word_prob[:, w_index])
                        print "topic_prob[d_index][w_index] = " + str(prob)
                        exit(0)
                    else:
                        normalize(prob)
                    self.topic_prob[d_index][w_index] = prob
            print "M step:"
            # update P(w | z)
            for z in range(number_of_topics):
                for w_index in range(vocabulary_size):
                    s = 0
                    for d_index in range(len(self.documents)):
                        count = term_doc_matrix[d_index][w_index]
                        s = s + count * self.topic_prob[d_index, w_index, z]
                    self.topic_word_prob[z][w_index] = s
                normalize(self.topic_word_prob[z])

            # update P(z | d)
            for d_index in range(len(self.documents)):
                for z in range(number_of_topics):
                    s = 0
                    for w_index in range(vocabulary_size):
                        count = term_doc_matrix[d_index][w_index]
                        s = s + count * self.topic_prob[d_index, w_index, z]
                    self.document_topic_prob[d_index][z] = s
                #                print self.document_topic_prob[d_index]
                #                assert(sum(self.document_topic_prob[d_index]) != 0)
                normalize(self.document_topic_prob[d_index])

        endtime = datetime.datetime.now()
        minutes = (endtime - starttime).seconds / 60
        print "Running EM Algorithm costs %d minutes and %d seconds" %(minutes, (endtime - starttime).seconds - minutes * 60)
