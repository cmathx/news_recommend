# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

import re
import ConfigParser

def sortByTime(train_set):
    fp_data = open('data/train_data.map.txt', 'r')
    data_list = []
    for line in fp_data:
        element = line.split('\t')
        user_id = int(element[0])
        news_id = int(element[1])
        time = int(element[2])
        title = element[3]
        content = element[4]
        publish_time = element[5]
        t_list = (user_id, news_id, time, title, content, publish_time)
        data_list.append(t_list)
    data_list.sort(key = lambda d: (d[0], d[2]), reverse = True)
    fp_total_set = open('data/train_data.sort.txt', 'w')
    for item in data_list:
        fp_total_set.write('%d\t%d\t%d\t%s\t%s\t%s' %(int(item[0]), int(item[1]), int(item[2]), \
                                                     item[3], item[4], item[5]))

def dataPreprocess(train_set):
    user_id_map = {}
    user_read_count_map = {}
    user_count = 0
    news_id_map = {}
    news_count = 0
    news_been_read_count_map = {}
    train_data = open(train_set, 'r')
    train_data_after_map = open('result/train_data.map.txt', 'w')
    for line in train_data:
        line = line.rstrip('\t')
        if line == '':
            continue
        word = line.split('\t')
        user_id = int(word[0])
        news_id = int(word[1])
        read_time = int(word[2])
        title = word[3]
        content = word[4]
        publish_time = word[5]
        if user_id_map.has_key(user_id) == False:
            user_id_map[user_id] = user_count
            user_count += 1
            user_read_count_map[user_id_map[user_id]] = 1
        else:
            user_read_count_map[user_id_map[user_id]] += 1
        if news_id_map.has_key(news_id) == False:
            news_id_map[news_id] = news_count
            news_count += 1
            news_been_read_count_map[news_id_map[news_id]] = 1
        else:
            news_been_read_count_map[news_id_map[news_id]] += 1
        train_data_after_map.write('%d\t%d\t%d\t%s\t%s\t%s' \
                                   %(user_id_map[user_id], news_id_map[news_id], read_time, \
                                     title, content, publish_time))
    return user_id_map, user_count, news_id_map, news_count, user_read_count_map, news_been_read_count_map

def getReverseIdMap(user_id_map, news_id_map):
    fp_user_id_map = open('result/user_id_map.txt', 'w')
    fp_reverse_user_id_map = open('result/reverse_user_id_map.txt', 'w')
    reverse_user_id_map = {}
    for user_id in user_id_map:
        reverse_user_id_map[user_id_map[user_id]] = user_id
        fp_user_id_map.write('%d\t%d\n' %(user_id, user_id_map[user_id]))
        fp_reverse_user_id_map.write('%d\t%d\n' %(user_id_map[user_id], user_id))
    fp_news_id_map = open('result/news_id_map.txt', 'w')
    fp_reverse_news_id_map = open('result/reverse_news_id_map.txt', 'w')
    reverse_news_id_map = {}
    for news_id in news_id_map:
        reverse_news_id_map[news_id_map[news_id]] = news_id
        fp_news_id_map.write('%d\t%d\n' %(news_id, news_id_map[news_id]))
        fp_reverse_news_id_map.write('%d\t%d\n' %(news_id_map[news_id], news_id))
    return reverse_user_id_map, reverse_news_id_map

def printNewsReadCountInfo(user_read_count_map, news_been_read_count_map):
    sort_user_read_count_map= sorted(user_read_count_map.iteritems(), key=lambda d:d[1], reverse = True)
    sort_news_been_read_count_map = sorted(news_been_read_count_map.iteritems(), key=lambda d:d[1], reverse = True)
    userReadNewsCountInfo = open('result/userReadNewsCountInfo.txt', 'w')
    formatter = "%r\t%r\n"
    for user_read_info in sort_user_read_count_map:
        userReadNewsCountInfo.write(formatter %(user_read_info[0], user_read_info[1]))
    cnt = 0
    fp_hot_news = open('result/hotNews.txt', 'w')
    newsBeenReadCountInfo = open('result/newsBeenReadCountInfo.txt', 'w')
    for news_been_read_info in sort_news_been_read_count_map:
        if cnt < 10:
            fp_hot_news.write('%d\n' %(news_been_read_info[0]))
        cnt += 1
        newsBeenReadCountInfo.write(formatter %(news_been_read_info[0], news_been_read_info[1]))

if __name__ == '__main__':
    train_set_file = 'data/train_data.edit.txt'
    sortByTime(train_set_file)
    train_set_file = 'data/train_data.sort.txt'
    user_id_map, user_count, news_id_map, news_count, user_read_count_map, news_been_read_count_map = \
        dataPreprocess(train_set_file)
    print 'number of users:%d number of news:%d' %(user_count, news_count)
    printNewsReadCountInfo(user_read_count_map, news_been_read_count_map)
    getReverseIdMap(user_id_map, news_id_map)