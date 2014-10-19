# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

import numpy as np
import time


def getUserItemRate():
    user_item_rate = dict()
    fp_total_set = open('../../../data/total_set.txt', 'r')
    for line in fp_total_set:
        words = line.split('\t')
        user_item_rate.setdefault(words[0], {})
        user_item_rate[words[0]].setdefault(words[1], 0)
        user_item_rate[words[0]][words[1]] += 1
    fp_rate_set = open('../../../data/user_item_rate.csv', 'w')
    for user, item_score in user_item_rate.items():
        for item in item_score.keys():
            fp_rate_set.write('%s\t%s\t%s\n' % (user, item, item_score[item]))
    fp_rate_set.close()
    fp_total_set.close()


def getTermDocMat(number_of_documents, vocabulary_size):
    print '计算初始评分矩阵'
    getUserItemRate()

    user_news_ratings = dict()  #用户-物品的评分表
    user_dict_r2v = dict()
    item_dict_r2v = dict()
    user_dict_v2r = dict()
    item_dict_v2r = dict()
    user_cnt = 0
    item_cnt = 0
    for line in open('../../../data/user_item_rate.csv'):
        user, item, score = line.strip().split("\t")
        if user_dict_r2v.has_key(user) == False:
            user_dict_r2v[user] = user_cnt
            user_dict_v2r[user_cnt] = user
            user_cnt += 1
        if item_dict_r2v.has_key(item) == False:
            item_dict_r2v[item] = item_cnt
            item_dict_v2r[item_cnt] = item
            item_cnt += 1
        user_news_ratings.setdefault(user, {})
        user_news_ratings[user][item] = float(score)

    print 'compute term_doc_matrix'
    term_doc_matrix = np.zeros([number_of_documents, vocabulary_size], dtype=np.int)
    for user, item_score in user_news_ratings.items():
        for item, score in item_score.items():
            term_doc_matrix[user_dict_r2v[user]][item_dict_r2v[item]] = score
    return term_doc_matrix, user_dict_v2r, item_dict_v2r


def documentWordProb(number_of_documents, vocabulary_size, number_of_topics, document_topic_prob, topic_word_prob):
    # number_of_documents = 10000
    # vocabulary_size = 6183
    # number_of_topics = NUMBERS_OF_TOPIC
    document_word_prob = np.zeros([number_of_documents, vocabulary_size], dtype=np.float)  # P(w | d)
    for d_index in xrange(number_of_documents):
        for v_index in xrange(vocabulary_size):
            for t_index in xrange(number_of_topics):
                document_word_prob[d_index][v_index] += document_topic_prob[d_index][t_index] * \
                                                        topic_word_prob[t_index][v_index]
    return document_word_prob


def plsaRecommend(document_word_prob, user_dict_v2r, item_dict_v2r, N):
    numbers_of_users = 10000
    numbers_of_items = 6183
    fp_plsa_recommend = open('../../../recommend/plsaRecommend.csv', 'w')
    fp_plsa_recommend.write('userid,newsid\n')
    for u_index in xrange(numbers_of_users):
        user_id = user_dict_v2r[u_index]
        item_score_dict = dict()
        for i_index in xrange(numbers_of_items):
            item_score_dict[item_dict_v2r[i_index]] = document_word_prob[u_index][i_index]
        item_rec_list = sorted(item_score_dict.items(), key=lambda d: d[1], reverse=True)[0:N]
        for i in xrange(N):
            fp_plsa_recommend.write('%s,%s\n' % (user_id, item_rec_list[i][0]))


