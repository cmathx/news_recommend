#__author__ = 'cjweffort'
# -*- coding: utf-8 -*-

def getUserFinalViewNews():
    #计算用户最后一条浏览的新闻
    user_final_view_news = dict()
    user_final_view_time = dict()
    fp_total_set = open('../../data/total_set.txt', 'r')
    for line in fp_total_set:
        tup = line.split('\t')
        user_final_view_news.setdefault(tup[0], tup[1])
        user_final_view_time.setdefault(tup[0], tup[2])
        if tup[2] > user_final_view_time[tup[0]]:
            user_final_view_news[tup[0]] = tup[1]
    fp_total_set.close()
    return user_final_view_news

def getUserFinalDayViewNews():
    #计算用户最后一天浏览的新闻列表
    user_final_view_news1 = dict()
    user_final_view_time1 = dict()
    fp_test_set = open('../../data/test_set.txt', 'r')
    for line in fp_test_set:
        tup = line.split('\t')
        user_final_view_time1.setdefault(tup[0], tup[2].split('-')[0])
    for user, final_view_time in user_final_view_time1.items():
        print user, final_view_time
    fp_total_set = open('../../data/total_set.txt', 'r')
    for line in fp_total_set:
        tup = line.split('\t')
        if tup[2].split('-')[0] == user_final_view_time1[tup[0]]:
            user_final_view_news1.setdefault(tup[0], {})
            user_final_view_news1[tup[0]].setdefault(tup[1], 0)
    fp_test_set.close()
    fp_total_set.close()
    return user_final_view_news1