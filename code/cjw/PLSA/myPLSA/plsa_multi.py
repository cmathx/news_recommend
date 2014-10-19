import re
from utils import normalize
import numpy as np
import time
import random
from multiprocessing import Pool, freeze_support
import itertools
import functools

# def getTermDocMatrix():
#     return term_doc_matrix
#
# def getNumberOfDocuments():
#     return number_of_documents
#
# def getVocabularySize():
#     return vocabulary_size
#
# def getNumberOfTopics():
#     return number_of_topics
#
# def getMaxIter():
#     return max_iter
#
# def getDocumentTopicProb():
#     return document_topic_prob
#
# def getTopicWordProb():
#     return topic_word_prob
#
# def getTopicProb():
#     return topic_prob

global ed, md, mt

# These get passed out to workers.
def do_estep(d, vocabulary_size, number_of_topics, document_topic_prob, topic_word_prob):
    # vocabulary_size = getVocabularySize()
    # number_of_topics = getNumberOfTopics()
    # document_topic_prob = getDocumentTopicProb()
    # topic_word_prob = getTopicWordProb()
    # print 'e_step:', vocabulary_size, number_of_topics
    # print document_topic_prob
    # print topic_word_prob
    print 'document %d' %d
    result = np.zeros([vocabulary_size, number_of_topics])

    for w in range(vocabulary_size):
        prob = document_topic_prob[d, :] * topic_word_prob[:, w]
        if sum(prob) == 0.0:
            print 'exit'
        else:
            normalize(prob)
        result[w] = prob
    return result


def do_mstep_a(t, vocabulary_size, number_of_documents, term_doc_matrix, topic_prob):
    # vocabulary_size = getVocabularySize()
    # number_of_documents = getNumberOfDocuments()
    # term_doc_matrix = getTermDocMatrix()
    # topic_prob = getTopicProb()
    print 'topic %d' %t
    result = np.zeros([vocabulary_size])

    for w_index in range(vocabulary_size):
        s = 0
        for d_index in range(number_of_documents):
            count = term_doc_matrix[d_index][w_index]
            s = s + count * topic_prob[d_index, w_index, t]
        result[w_index] = s
    normalize(result)
    return result


def do_mstep_b(d, vocabulary_size, number_of_topics, term_doc_matrix, topic_prob):
    # number_of_topics = getNumberOfTopics()
    # vocabulary_size = getVocabularySize()
    # term_doc_matrix = getTermDocMatrix()
    # topic_word_prob = getTopicWordProb()
    print 'document %d' %d
    result = np.zeros([number_of_topics])
    for z in range(number_of_topics):
        s = 0
        for w_index in range(vocabulary_size):
            count = term_doc_matrix[d][w_index]
            s = s + count * topic_prob[d, w_index, z]
        result[z] = s
    normalize(result)
    return result


def plsa(t_d_m, n_o_d, v_s, n_o_t, m_i, processes=4):
    '''
    Model topics using multiprocessing.

    Args
        nt (int): number of topic
        max_iter (int): maximum number of iterations
        processes (int): maximum number of parallel processes (default=4)

    '''
    global term_doc_matrix, number_of_documents, vocabulary_size, number_of_topics, max_iter, document_topic_prob, topic_word_prob, topic_prob
    term_doc_matrix = t_d_m
    number_of_documents = n_o_d
    vocabulary_size = v_s
    number_of_topics = n_o_t
    max_iter = m_i

    print "number of documents:", str(number_of_documents) + "  vocabulary size:", str(vocabulary_size)
    print "EM iteration begins. Num topics: " + str(number_of_topics) + "; Iterations: " + str(max_iter) + "; Processes: " + str(
        processes)

    # Create the counter arrays.
    document_topic_prob = np.zeros([number_of_documents, number_of_topics], dtype=np.float)  # P(z | d)
    topic_word_prob = np.zeros([number_of_topics, vocabulary_size], dtype=np.float)  # P(w | z)
    topic_prob = np.zeros([number_of_documents, vocabulary_size, number_of_topics], dtype=np.float)  # P(z | d, w)


    # Initialize
    print "Initializing..."

    # randomly assign values
    document_topic_prob = np.random.random(size=(number_of_documents, number_of_topics))
    for d_index in range(number_of_documents):
        normalize(document_topic_prob[d_index])  # normalize for each document
    topic_word_prob = np.random.random(size=(number_of_topics, vocabulary_size))
    for z in range(number_of_topics):
        normalize(topic_word_prob[z])  # normalize for each topic

    # print document_topic_prob
    # print topic_word_prob
    # print topic_prob

    # Run the EM algorithm using multiprocessing
    for iteration in range(max_iter):

        start1 = time.time()
        print 'E_Step'
        start = time.time()
        freeze_support()
        # e step
        customized_do_estep = functools.partial(do_estep, vocabulary_size=vocabulary_size, number_of_topics=number_of_topics,\
                                        document_topic_prob=document_topic_prob, topic_word_prob=topic_word_prob)
        topic_prob = []
        pool = Pool(processes)
        TASKS = []
        for d_index in range(number_of_documents):
            TASKS.append(d_index)
        topic_prob = pool.map(customized_do_estep, TASKS)
        pool.close()
        pool.join()

        # print 'e_step result:'
        # print topic_prob
        # print jobs
        # finished = False
        # while not finished:
        #     # try:
        #     topic_prob.rint append(jobs.next())
        #     # except Exception as e:
        #     #     finished = True
        # topic_prob = np.asarray(topic_prob)
        # # print 'jobs = ', jobs

        # print "iteration " + str(iteration) + '  topic_prob = ', topic_prob
        print 'it costs: ', time.time() - start

        print 'M_Step_A'
        start = time.time()
        # m step - first part
        customized_do_mstep_a = functools.partial(do_mstep_a, vocabulary_size=vocabulary_size, number_of_documents=number_of_documents,\
                                        term_doc_matrix=term_doc_matrix, topic_prob=topic_prob)
        pool = Pool(processes / 2)
        topic_word_prob = []
        TASKS = []
        for z_index in range(number_of_topics):
            TASKS.append(z_index)
        topic_word_prob = pool.imap(customized_do_mstep_a, TASKS)

        pool.close()
        pool.join()
        # print 'm_step_a result:'
        # print topic_word_prob

        # finished = False
        # while not finished:
        #     try:
        #         topic_word_prob.append(jobs.next())
        #     except:
        #         finished = True
        topic_word_prob = np.asarray(topic_word_prob)

        # print "iteration " + str(iteration) + '  topic word prob = ', topic_word_prob
        print 'it costs: ', time.time() - start

        print 'M_Step_B'
        start = time.time()
        # m step - second part
        customized_do_mstep_b = functools.partial(do_mstep_b, vocabulary_size=vocabulary_size, number_of_topics=number_of_topics,\
                                        term_doc_matrix=term_doc_matrix, topic_prob=topic_prob)
        pool = Pool(processes / 2)
        document_topic_prob = []
        TASKS = []
        for d_index in range(number_of_documents):
            TASKS.append(d_index)
        document_topic_prob = pool.imap(customized_do_mstep_b, TASKS)
        pool.close()
        pool.join()

        # print 'm_step_b result:'
        # print document_topic_prob

        # finished = False
        # while not finished:
        #     try:
        #         document_topic_prob.append(jobs.next())
        #     except:
        #         finished = True

        document_topic_prob = np.asarray(document_topic_prob)

        # print "iteration " + str(iteration) + '  document topic prob = ' + document_topic_prob
        print 'it costs: ', time.time() - start

        print "iteration " + str(iteration) + " completed in " + str(time.time() - start1) + " seconds."
        print "document probability variance: " + str(np.var(document_topic_prob))

    return document_topic_prob, topic_word_prob

