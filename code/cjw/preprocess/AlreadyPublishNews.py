# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

INTERVALS_LFT = -1
INTERVAL_RIGHT = 5

def getAlreadyPublishNews():
    user_fin_view_time = dict()
    fp_test_set = open('../../data/test_set.txt', 'r')
    for line in fp_test_set:
        words = line.split('\t')
        user_fin_view_time[words[0]] = words[2].split('-')[0]
    fp_test_set.close()

    news_publish_time = dict()
    fp_total_set = open('../../data/total_set.txt', 'r')
    for line in fp_total_set:
        words = line.split('\t')
        if news_publish_time.has_key(words[1]) == False:
            news_publish_time[words[1]] = words[3].split('-')[0]
    fp_total_set.close()

    user_may_read_news = dict()
    for user, fin_view_time in user_fin_view_time.items():
        fin_view_year = int(fin_view_time.split('/')[0])
        fin_view_month = int(fin_view_time.split('/')[1])
        fin_view_day = int(fin_view_time.split('/')[2])
        for news, publish_time in news_publish_time.items():
            publish_year = int(publish_time.split('/')[0])
            publish_month = int(publish_time.split('/')[1])
            publish_day = int(publish_time.split('/')[2])
            import datetime
            fin_view_date_time = datetime.datetime(fin_view_year, fin_view_month, fin_view_day)
            publish_date_time = datetime.datetime(publish_year, publish_month, publish_day)
            intervals = (publish_date_time - fin_view_date_time).days
            if intervals >= INTERVALS_LFT and intervals <= INTERVAL_RIGHT:
                user_may_read_news.setdefault(user, {})
                user_may_read_news[user].setdefault(news, 0)
    return user_may_read_news