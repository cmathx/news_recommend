# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

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


