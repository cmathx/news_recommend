# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

import numpy as np
from numpy import *
from cjw.PLSA.plsaRecommend import *
import BaseLineSVD
import datetime

if __name__ == "__main__":
    print '建立doc映射表'
    doc_set_file = '../../data/document.csv'
    total_set_file = '../../data/total_set.txt'
    user_set, doc_set, user_map_r2v, user_map_v2r, doc_map_r2v, doc_map_v2r, doc_click_count, user_doc_click_count = \
    createDocMapAndClickInfo(total_set_file, doc_set_file)

    # load data
    train, test = BaseLineSVD.load_data()
    print 'load data success'
    user_news_arr = np.zeros([10000, 6183], dtype=np.float)
    for user, item_score in train.items():
        for item, score in item_score.items():
            user_news_arr[user_map_r2v[user], doc_map_r2v[item]] = float(score)
    print 'svd start'
    start = datetime.time()
    print type(user_news_arr[9999, 6182])
    user_arr, sigma, news_arr = linalg.svd(user_news_arr)
    end = datetime.time()
    # print 'it costs: ', end - start
    print sigma
    cnt = 0
    for feature_value in sigma:
        if feature_value >= 1e-2:
            cnt += 1
    print 'cnt = ', cnt
    sigma_arr = np.zeros([cnt, cnt], dtype=np.float)
    for i in xrange(cnt):
        sigma_arr[i, i] = sigma[i]
    predict_user_news_rate = np.dot(np.dot(user_arr[0:, 0:cnt], sigma_arr[0:cnt][0:cnt]), news_arr[0:cnt, 0:])
    print type(predict_user_news_rate), size(predict_user_news_rate)
    fp_svd_recommend = open('../../recommend/svd_recommend.csv', 'w')
    fp_svd_recommend.write('userid,newsid\n')
    error = 0
    for i in xrange(10000):
        max_index = -1
        max = -1
        for j in xrange(6183):
            if doc_map_v2r[j] not in train[user_map_v2r[i]]:
                if predict_user_news_rate[i, j] > max:
                    max = predict_user_news_rate[i, j]
                    max_index = j
            else:
                error += math.fabs(predict_user_news_rate[i][j] - train[user_map_v2r[i]][doc_map_v2r[j]])
        print max
        fp_svd_recommend.write('%s,%s\n' %(user_map_v2r[i], doc_map_v2r[max_index]))
    print error
    fp_svd_recommend.close()