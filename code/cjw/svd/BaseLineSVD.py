# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

'''''
Created on Dec 13, 2012

@Author: Dennis Wu
@E-mail: hansel.zh@gmail.com
@Homepage: http://blog.csdn.net/wuzh670

Data set download from : http://www.grouplens.org/system/files/ml-100k.zip
'''

from math import sqrt, fabs
import random
from cjw.PLSA.plsaRecommend import *

def load_data():
    train = {}
    test = {}
    filename_train = '../../data/user_item_rate.csv'
    # filename_test = 'data/ua.test'

    for line in open(filename_train):
        (userId, itemId, rating) = line.strip().split('\t')
        train.setdefault(userId, {})
        train[userId][itemId] = float(rating)

    '''
    for line in open(filename_test):
        (userId, itemId, rating, timestamp) = line.strip().split('\t')
        test.setdefault(userId,{})
        test[userId][itemId] = float(rating)
    '''

    return train, test


def calMean(train):
    stat = 0
    num = 0
    for u in train.keys():
        for i in train[u].keys():
            stat += train[u][i]
            num += 1
    mean = stat * 1.0 / num
    return mean


def initialBias(train, user_set, movie_set, mean):
    bu = {}
    bi = {}
    biNum = {}
    buNum = {}

    for su in user_set:
        for i in train[su].keys():
            bi.setdefault(i, 0)
            biNum.setdefault(i, 0)
            bi[i] += (train[su][i] - mean)
            biNum[i] += 1

    for si in movie_set:
        biNum.setdefault(si, 0)
        if biNum[si] >= 1:
            bi[si] = bi[si] * 1.0 / (biNum[si] + 25)
        else:
            bi[si] = 0.0

    for su in user_set:
        for i in train[su].keys():
            bu.setdefault(su, 0)
            buNum.setdefault(su, 0)
            bu[su] += (train[su][i] - mean - bi[i])
            buNum[su] += 1

    for su in user_set:
        buNum.setdefault(su, 0)
        if buNum[su] >= 1:
            bu[su] = bu[su] * 1.0 / (buNum[su] + 10)
        else:
            bu[su] = 0.0

    return bu, bi


def initialFeature(feature, user_set, movie_set):
    random.seed(0)
    user_feature = {}
    item_feature = {}
    for si in user_set:
        user_feature.setdefault(si, {})
        j = 1
        while j < (feature + 1):
            sj = str(j)
            user_feature[si].setdefault(sj, random.uniform(0, 1))
            j += 1

    for si in movie_set:
        item_feature.setdefault(si, {})
        j = 1
        while j < (feature + 1):
            sj = str(j)
            item_feature[si].setdefault(sj, random.uniform(0, 1))
            j += 1
    return user_feature, item_feature


def svd(train, mean, feature, user_feature, item_feature, bu, bi):
    gama = 0.02
    lamda = 0.3
    slowRate = 0.99
    step = 0
    preRmse = 1000000000.0
    nowRmse = 0.0

    while step < 100:
        rmse = 0.0
        n = 0
        for u in train.keys():
            for i in train[u].keys():
                pui = 1.0 * (mean + bu[u] + bi[i])
                k = 1
                while k < (feature + 1):
                    sk = str(k)
                    pui += user_feature[u][sk] * item_feature[i][sk]
                    k += 1
                eui = train[u][i] - pui
                # print train[u][i], pui, eui
                rmse += pow(eui, 2)

                n += 1
                bu[u] += gama * (eui - lamda * bu[u])
                bi[i] += gama * (eui - lamda * bi[i])
                k = 1
                while k < (feature + 1):
                    sk = str(k)
                    user_feature[u][sk] += gama * (eui * item_feature[i][sk] - lamda * user_feature[u][sk])
                    item_feature[i][sk] += gama * (eui * user_feature[u][sk] - lamda * item_feature[i][sk])
                    k += 1

        nowRmse = sqrt(rmse * 1.0 / n)
        print 'step: %d      Rmse: %s' % ((step + 1), nowRmse)

        if (nowRmse < preRmse):
            preRmse = nowRmse

        gama *= slowRate
        step += 1
    return user_feature, item_feature, bu, bi

def recommend(train, bu, bi, user_feature, item_feature, mean, feature, RECOMMEND_NUM, user_set, doc_set):
    fp_recommend = open('../../recommend/svd_sgd_recommend.csv', 'w')
    fp_recommend.write('userid,newsid\n')
    for su in user_set:
        item_score = dict()
        for si in doc_set:
            pui = 1.0 * (mean + bu[su] + bi[si])
            k = 1
            while k < (feature + 1):
                sk = str(k)
                pui += user_feature[su][sk] * item_feature[si][sk]
                k += 1
            item_score.setdefault(si, pui)
        sorted_item_score = sorted(item_score.items(), key = lambda d: d[1], reverse = True)
        cnt = 0
        for tup in sorted_item_score:
            item = tup[0]
            if cnt == RECOMMEND_NUM:
                break
            if item not in train[su]:
                fp_recommend.write('%s,%s\n' %(su, item))
                cnt += 1


def calRmse(test, bu, bi, user_feature, item_feature, mean, feature):
    rmse = 0.0
    n = 0
    for u in test.keys():
        for i in test[u].keys():
            pui = 1.0 * (mean + bu[u] + bi[i])
            k = 1
            while k < (feature + 1):
                sk = str(k)
                pui += user_feature[u][sk] * item_feature[i][sk]
                k += 1
            eui = pui - test[u][i]
            rmse += pow(eui, 2)
            n += 1
    rmse = sqrt(rmse * 1.0 / n)
    return rmse;


if __name__ == "__main__":
    print '建立doc映射表'
    doc_set_file = '../../data/document.csv'
    total_set_file = '../../data/total_set.txt'
    user_set, doc_set, doc_map1, doc_map2, doc_click_count, user_doc_click_count = \
    createDocMapAndClickInfo(total_set_file, doc_set_file)

    # load data
    train, test = load_data()
    print 'load data success'

    # Calculate overall mean rating
    mean = calMean(train)
    print 'mean = ', mean
    print 'Calculate overall mean rating success'

    # USER_NUM = 943
    # MOVIE_NUM = 1682
    FEATURE_NUM = 100   #svd特征值个数
    # initial user and item Bias, respectly
    bu, bi = initialBias(train, user_set, doc_set, mean)
    print 'initial user and item Bias, respectly success'

    # initial user and item feature, respectly
    user_feature, item_feature = initialFeature(FEATURE_NUM, user_set, doc_set)
    print 'initial user and item feature, respectly success'

    # baseline + svd + stochastic gradient descent
    user_feature, item_feature, bu, bi = svd(train, mean, FEATURE_NUM, user_feature, item_feature, bu, bi)
    print 'baseline + svd + stochastic gradient descent success'

    #svd(stochastic gradient descent) based recommend
    RECOMMEND_NUM = 2
    recommend(train, bu, bi, user_feature, item_feature, mean, FEATURE_NUM, RECOMMEND_NUM, user_set, doc_set)

    # compute the rmse of test set
    # print 'the Rmse of test test is: %s' % calRmse(test, bu, bi, user_feature, item_feature, mean, 100)