# -*- encoding: utf-8 -*-
'''
Created on 2014年5月30日

@author: Chenan
'''

import news_popular
import random

def read_data(filename):
    news_dict = dict()
    user_dict = dict()

    fr = open(filename, 'r')
    for line in fr.readlines():
        lineArr = line.split('\t')
        user_id = int(lineArr[0])
        news_id = int(lineArr[1])
        read_time = news_popular.translate_to_ms(lineArr[2])
        edit_time = news_popular.translate_to_ms(lineArr[3])
        title = lineArr[4]

        user_dict.setdefault(user_id, [])
        user_dict[user_id].append((news_id, read_time))
        news_dict.setdefault(news_id, edit_time)
        if read_time < edit_time:
            news_dict[news_id] = read_time

    return user_dict, news_dict


def process_user_dict(user_dict):
    ret_set = []
    ret_dict = {}
    for user_id, news in user_dict.items():
        last_read_time = 0
        ret_dict.setdefault(user_id, {})
        for news_id, read_time in news:
            ret_set.append((1, news_id, read_time))
            if read_time > last_read_time:
                last_read_time = read_time
            ret_dict.setdefault(news_id, 0)
        ret_set.append((2, user_id, last_read_time + 1))
    return ret_set, ret_dict


def process_news_dict(news_dict):
    ret_set = news_dict.items()
    return ret_set


def sigmoid(inx):
    import math
    return 3/(1.0+math.exp(inx))


def getRecommend(news_hit_dict, read_time, news_time_dict, user_news_dict):
    item_list = dict()
    import math
    #print 'news_hit_dict %d'%len(news_hit_dict)
    for news_id, hit in news_hit_dict.items():
        diff = (read_time - news_time_dict[news_id])/86400
        if diff < 7:
            item_list.setdefault(news_id,  math.log(hit/5.0+2) + sigmoid(diff*1.0/7))

    recm_list = sorted(item_list.iteritems(), key=lambda d: d[1], reverse=True)
    ret_set = []
    for news_id, hot in recm_list:
        if news_id in user_news_dict:
            continue
        else:
            ret_set.append(news_id)
    return ret_set

def process_data_set(user_set, user_dict, news_time_dict):
    data_set = sorted(user_set, key=lambda d: d[2])
    print 'user_set, data_set %d,%d'%(len(user_set), len(data_set))
    news_hit_dict = {}
    recm_list = []
    for item in data_set:
        if item[0] == 0:
            news_hit_dict.setdefault(item[1], 0)
        if item[0] == 1:
            news_hit_dict.setdefault(item[1], 0)
            news_hit_dict[item[1]] += 1
        else:
            item_list = getRecommend(news_hit_dict, item[2], news_time_dict, user_dict[item[1]])
            #print 'len(item_list) = %d'%len(item_list)
            #r1 = random.uniform(0, len(item_list) - 1)
            #r2 = random.uniform(0, len(item_list) - 1)
            recm_list.append((item[1], item_list[0]))
            recm_list.append((item[1], item_list[1]))
    return recm_list

def process():
    user_dict, news_dict = read_data('total_set.txt')
    print('pass read_data')
    print('user_dict %d'%len(user_dict))
    user_news_set, user_news_dict = process_user_dict(user_dict)

    print('pass process_user_dict')
    #print('user_news_set, user_news_dict, %d, %d'%(len(user_news_set), len(user_news_dict)))
    recm_list = process_data_set(user_news_set, user_news_dict, news_dict)
    print('pass process_data_set')
    fw = open('rec3.csv', 'w')
    fw.write('userid,newsid\n')
    for user_id, news_id in recm_list:
        fw.write('%d,%d\n'% (user_id, news_id))

    fw.close()
    print('finished')

#process()