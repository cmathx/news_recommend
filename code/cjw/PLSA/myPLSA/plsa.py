import re
import time
import numpy as np
from utils import normalize

"""
Author: 
Alex Kong (https://github.com/hitalex)

Reference:
http://blog.tomtung.com/2011/10/plsa
"""


def plsa(term_doc_matrix, number_of_documents, vocabulary_size, number_of_topics, max_iter):
    '''
    Model topics.
    '''
    print "EM iteration begins..."

    # print term_doc_matrix
    # Create the counter arrays.
    document_topic_prob = np.zeros([number_of_documents, number_of_topics], dtype=np.float)  # P(z | d)
    topic_word_prob = np.zeros([number_of_topics, vocabulary_size], dtype=np.float)  # P(w | z)
    topic_prob = np.zeros([number_of_documents, vocabulary_size, number_of_topics],
                          dtype=np.float)  # P(z | d, w)

    # Initialize
    print "Initializing..."
    # randomly assign values
    document_topic_prob = np.random.random(size=(number_of_documents, number_of_topics))
    for d_index in range(number_of_documents):
        normalize(document_topic_prob[d_index])  # normalize for each document
    topic_word_prob = np.random.random(size=(number_of_topics, vocabulary_size))
    for z in range(number_of_topics):
        normalize(topic_word_prob[z])  # normalize for each topic
    #
    # print document_topic_prob
    # print topic_word_prob
    # for i in xrange(number_of_documents):
    #     t_sum = 0
    #     for j in xrange(vocabulary_size):
    #         t_sum += term_doc_matrix[i][j]
    #     if t_sum == 0.0:
    #         print i

    # Run the EM algorithm
    for iteration in range(max_iter):
        print "Iteration #" + str(iteration + 1) + "..."
        print "E step:"
        start = time.time()
        for d_index in xrange(number_of_documents):
            print 'E_Step:document ', d_index
            for w_index in range(vocabulary_size):
                prob = document_topic_prob[d_index, :] * topic_word_prob[:, w_index]
                t_sum = sum(prob)
                if t_sum == 0.0:
                    print "d_index = " + str(d_index) + ",  w_index = " + str(w_index)
                    print "self.document_topic_prob[d_index, :] = " + str(document_topic_prob[d_index, :])
                    print "self.topic_word_prob[:, w_index] = " + str(topic_word_prob[:, w_index])
                    print "topic_prob[d_index][w_index] = " + str(prob)
                    exit(0)
                else:
                    normalize(prob)
                topic_prob[d_index][w_index] = prob
        print 'E_Step costs:', time.time() - start

        print "M step:"
        start = time.time()
        # update P(w | z)
        for z in range(number_of_topics):
            print 'M_Step:topic ', z
            for w_index in range(vocabulary_size):
                s = 0
                for d_index in range(number_of_documents):
                    count = term_doc_matrix[d_index][w_index]
                    s = s + count * topic_prob[d_index, w_index, z]
                topic_word_prob[z][w_index] = s
            normalize(topic_word_prob[z])
        print 'M_Step_A costs:', time.time() - start

        # update P(z | d)
        start = time.time()
        for d_index in range(number_of_documents):
            print 'M_Step:document ', d_index
            for z in range(number_of_topics):
                s = 0
                for w_index in range(vocabulary_size):
                    count = term_doc_matrix[d_index][w_index]
                    s = s + count * topic_prob[d_index, w_index, z]
                document_topic_prob[d_index][z] = s
            normalize(document_topic_prob[d_index])
        print 'M_Step_B costs:', time.time() - start

        print "iteration " + str(iteration) + " completed in " + str(time.time() - start) + " seconds."

    return document_topic_prob, topic_word_prob
