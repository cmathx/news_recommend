# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

from cjw.PLSA.plsaRecommend import *

def getDocumentWeight(user_doc_click_count):
    user_news_weight = dict()
    for user, news_click in user_doc_click_count.items():
        user_news_weight.setdefault(user, {})
        t_sum = sum(user_doc_click_count[user])
        for news, click in news_click.items():
            user_news_weight[user].setdefault(news, 1.0 * click / t_sum)
    return user_news_weight

def userFeature(user_news_weight, corpus_feature, doc_map_r2v):
    user_feature = dict()
    for user, news_weight in user_news_weight.items():
        user_feature.setdefault(user, {})
        for news, weight in user_news_weight[user].items():
            v_news = doc_map_r2v[news]
            for tup in corpus_feature[v_news]:
                user_feature[user].setdefault(tup[0], 0)
                user_feature[user][tup[0]] += weight * tup[1]
    user_feature_lst = dict()
    for user, feature in user_feature.items():
        user_feature[user] = sorted(user_feature[user].items(), key=lambda d:d[0], reverse=False)
        ll = []
        for index, f_val in user_feature[user].items():
            ll.append((index, f_val))
        user_feature_lst[user] = ll
    return user_feature_lst

