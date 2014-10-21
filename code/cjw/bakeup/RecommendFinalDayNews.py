# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

def countEveryDayPublishNews(total_set_file):
    publish_news_every_day = {}
    fp_total_set = open(total_set_file, 'r')
    for line in fp_total_set:
        tup = line.split('\t')
        news_id = tup[1]
        publish_time = tup[3].split('-')[0]
        publish_news_every_day.setdefault(publish_time,[])
        publish_news_every_day[publish_time].append(news_id)
    return publish_news_every_day

def recommendFinalDayNews(test_set_file, publush_news_every_day):
    fp_test_set = open(test_set_file, 'r')
    fp_recommend_final_day_news = open('../../recommend/final_day_news.csv', 'w')
    fp_recommend_final_day_news.write('userid,newsid\n')
    for line in fp_test_set:
        tup = line.split('\t')
        user_id = tup[0]
        view_time = tup[2].split('-')[0]
        for item in publush_news_every_day[view_time]:
            fp_recommend_final_day_news.write('%s,%s\n' %(user_id, item))

if __name__ == '__main__':
    test_set_file = '../../data/test_set.txt'
    total_set_file = '../../data/total_set.txt'
    publush_news_every_day = countEveryDayPublishNews(total_set_file)
    recommendFinalDayNews(test_set_file, publush_news_every_day)