# -*- encoding: utf-8 -*-
'''
Created on 2014年5月30日

@author: Chenan
'''


def translate_to_ms(string):
    import time
    number = filter(str.isdigit, string)
    length = len(number)
    if length < 12:
        minute = 0
    else:
        minute = number[10:12]
    if length < 10:
        hour = 0
    else:
        hour = number[8:10]
    if length < 8:
        day = 0
    else:
        day = number[6:8]
    if length < 6:
        month = 0
    else:
        month = number[4:6]
    if length < 4:
        return 0
    else:
        year = number[0:4]

    tmlist = [int(year), int(month), int(day), int(hour), int(minute), 0, 0, 0, 0]
    return time.mktime(tmlist)



def get_news_count(filename):
    fr = open(filename, 'r')
    news_dict = dict()
    news_set = []
    user_dict = dict()
    total = 0
    for lines in fr.readlines():
        lineArr = lines.split('\t')
        user_id = int(lineArr[0])
        news_id = int(lineArr[1])
        read_time = int(lineArr[2])
        publish_time = translate_to_ms(lineArr[5])
        user_dict.setdefault(user_id, {})
        user_dict[user_id].setdefault(news_id, 1)
        if publish_time == 0:
            publish_time = read_time
        if news_id in news_dict.keys():
            index = news_dict[news_id]
            tmp_item = news_set[index]
            news_set[index] = (tmp_item[0], tmp_item[1], tmp_item[2] + 1)
        else:
            news_dict.setdefault(news_id, total)
            news_set.append((news_id, int(publish_time), 1))
            total += 1
    fr.close()
    return user_dict, news_set


def sort_by_time(news_set):
    time_sort = sorted(news_set, key=lambda d: d[1], reverse=True)
    #fw = open('news_sort_time.txt', 'w')
    #for item in time_sort:
    #    fw.write('%d %d %d\n' %(item[0], item[1], item[2]))
    #fw.close()
    ret_sort = []
    ref_time = translate_to_ms('2014-04-01 00:00')
    for item in time_sort:
        if ref_time - item[1] <= 604800:
            ret_sort.append(item)
        else:
            break
    return ret_sort

def sigmoid(inx):
    print inx
    import math
    return 10.0/(1.0 + math.exp(inx))


def process():
    user_dict, news_set = get_news_count('train_data.sort.txt')
    ret_news = sort_by_time(news_set)
    ref_time = translate_to_ms('2014-04-01 00:00')

    for item in ret_news:
        item = (item[0], item[1], item[2] + sigmoid((ref_time - item[1])/604800.0))

    hot_news = sorted(ret_news, key=lambda d: d[2], reverse=True)
    import random
    len_hot_news = len(hot_news) -1
    fw = open('recommend.csv', 'w')
    fw.write('userid,newsid\n')
    for key in user_dict.keys():
        x  = random.randint(0, len_hot_news)
        while hot_news[x][0] in user_dict[key].keys():
            x = random.randint(0, len_hot_news)
        fw.write('%d,%d\n'%(key, hot_news[x][0]))
        y = random.randint(0, len_hot_news)
        while x == y or hot_news[y][0] in user_dict[key].keys():
            y = random.randint(0, len_hot_news)
        fw.write('%d,%d\n'%(key, hot_news[y][1]))
    fw.close()
process()
