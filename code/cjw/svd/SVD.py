# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

import numpy as np
from numpy import *
from cjw.PLSA.plsaRecommend import *
import BaseLineSVD


if __name__ == "__main__":
    print '建立doc映射表'
    doc_set_file = '../../data/document.csv'
    total_set_file = '../../data/total_set.txt'
    user_set, doc_set, doc_map1, doc_map2, doc_click_count, user_doc_click_count = \
    createDocMapAndClickInfo(total_set_file, doc_set_file)

    # load data
    train, test = BaseLineSVD.load_data()
    print 'load data success'
    user_news_arr = np.zeros([10000, 6183], dtype=np.float)
    for user, item_score in train.items():
        for item, score in item_score.items():
            user_news_arr[int(user), int(item)] = float(score)
    user_arr, sigma_arr, news_arr = linalg.svd(user_news_arr)
    print sigma_arr



