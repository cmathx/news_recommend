# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

import os
import numpy as np
import RecommendToolkit
import plsa_multi
import plsa

NUMBER_OF_DOCUMENTS = 10000  #len(self.documents)
VOCABULARY_SIZE = 6183  #len(self.vocabulary)
NUMBERS_OF_TOPICS = 8
MAX_ITERS = 10

def writePLSAResult(document_topic_prob, topic_word_prob):
    fp_document_topic_prob = open('document_topic_prob.csv', 'w')
    for i in xrange(NUMBER_OF_DOCUMENTS):
        tag = True
        for j in xrange(NUMBERS_OF_TOPICS):
            if tag == True:
                tag = False
            else:
                fp_document_topic_prob.write('\t')
            fp_document_topic_prob.write('%s' %document_topic_prob[i][j])
        fp_document_topic_prob.write('\n')
    fp_document_topic_prob.close()
    fp_topic_word_prob = open('topic_word_prob.csv', 'w')
    for i in xrange(NUMBERS_OF_TOPICS):
        tag = True
        for j in xrange(VOCABULARY_SIZE):
            if tag == True:
                tag = False
            else:
                fp_topic_word_prob.write('\t')
            fp_topic_word_prob.write('%s' %topic_word_prob[i][j])
        fp_topic_word_prob.write('\n')
    fp_topic_word_prob.close()

def readPLSAResult():
    document_topic_prob = np.zeros([number_of_documents, number_of_topics], dtype=np.float)  # P(z | d)
    topic_word_prob = np.zeros([number_of_topics, vocabulary_size], dtype=np.float)  # P(w | z)
    fp_document_topic_prob = open('document_topic_prob.csv', 'r')
    ii = 0
    for line in fp_document_topic_prob:
        words = line.split('\t')
        jj = 0
        for item in words:
            document_topic_prob[ii][jj] = (float)(item)
            jj += 1
        ii += 1
    ii = 0
    fp_topic_word_prob = open('topic_word_prob.csv', 'r')
    for line in fp_topic_word_prob:
        words = line.split('\t')
        jj = 0
        for item in words:
            topic_word_prob[ii][jj] = (float)(item)
            jj += 1
        ii += 1
    print document_topic_prob
    print topic_word_prob
    return document_topic_prob, topic_word_prob

def getError(document_topic_prob, topic_word_prob, document_topic_prob1, topic_word_prob1):
    error1 = 0
    error2 = 0
    for i in xrange(NUMBER_OF_DOCUMENTS):
        for j in xrange(NUMBERS_OF_TOPICS):
            error1 += document_topic_prob[i][j] - document_topic_prob1[i][j]
    for i in xrange(NUMBERS_OF_TOPICS):
        for j in xrange(VOCABULARY_SIZE):
            error2 += topic_word_prob[i][j] - topic_word_prob1[i][j]
    print error1, error2

if __name__ == '__main__':
    number_of_documents = NUMBER_OF_DOCUMENTS
    vocabulary_size = VOCABULARY_SIZE
    number_of_topics = NUMBERS_OF_TOPICS
    max_iter = MAX_ITERS
    plsa_success = False
    if os.path.isfile('document_topic_prob.csv'):
        plsa_success = True
    term_doc_matrix, user_dict_v2r, item_dict_v2r = RecommendToolkit.getTermDocMat(number_of_documents, vocabulary_size)
    if plsa_success == False:
        print number_of_documents, vocabulary_size
    # print type(term_doc_matrix)
        document_topic_prob, topic_word_prob = plsa\
            .plsa(term_doc_matrix, number_of_documents, vocabulary_size, number_of_topics, max_iter)
        writePLSAResult(document_topic_prob, topic_word_prob)
    else:
        document_topic_prob, topic_word_prob = readPLSAResult()
        # getError(document_topic_prob, topic_word_prob, document_topic_prob1, topic_word_prob1)
    print 'compute document_word_prob'
    document_word_prob = RecommendToolkit.documentWordProb(number_of_documents, vocabulary_size, number_of_topics, document_topic_prob, topic_word_prob)
    print 'plsa recommend'
    RecommendToolkit.plsaRecommend(document_word_prob, user_dict_v2r, item_dict_v2r, 1)