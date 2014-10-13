# -*- encoding: utf-8 -*-
'''
Created on 2014年5月30日

@author: Chenan
'''

import news_popular
import math

def read_set(filename):
    '''
    :param filename: dataset following the format: user_id, news_id, read_time, edit_time, title (, content)
    :return:user_news_dict, type dict, user_id=>news_id=>read_time
            user_time_dict, type dict, user_id=>time, the time is the predicting time for each user
            news_dict, type, dict, news_id=>time, time is the edit time of this piece of news
    '''
    fr = open(filename, 'r')
    news_dict = {}
    user_news_dict = {}
    user_time_dict = {}

    for line in fr.readlines():
        lineArr = line.split('\t')
        user_id = int(lineArr[0])
        news_id = int(lineArr[1])
        read_time = news_popular.translate_to_ms(lineArr[2])
        edit_time = news_popular.translate_to_ms(lineArr[3])
        news_title = lineArr[4]
        #if one read one piece of news more than twice, then we just count as one
        user_news_dict.setdefault(user_id, {})
        user_news_dict[user_id].setdefault(news_id, read_time)
        if read_time < user_news_dict[user_id][news_id]:
            user_news_dict[user_id][news_id] = read_time
        #to predict last read time of each user
        user_time_dict.setdefault(user_id, 0)
        if read_time + 1 > user_time_dict[user_id]:
            user_time_dict[user_id] = read_time + 1
        #get total news and it's edit time
        news_dict.setdefault(news_id, edit_time)
        if read_time < edit_time:
            news_dict[news_id] = read_time - 1

    return user_news_dict, user_time_dict, news_dict


def get_sorted_time_news(user_news_dict, user_time_dict):
    '''
    :param user_news_dict: record , user_i read news_j in time_t
    :param user_time_dict: record, user_i read news_p in time_t, news_p is to predict
    :return:user_news_set sorted by time in ascending order
            notice that, suppose item is one data in user_news_set
            then, item[0] = 0 means that news item[2] was read by user item[1]
            item[0] = 1 means that you should predict for user item[1]
            len(item) = 4
    '''
    user_news_set = []
    for user_id, news in user_news_dict.items():
        #add record to user_news_set
        for news_id, read_time in news.items():
            user_news_set.append((0, user_id, news_id, read_time))
        #add predict_time into user_news_set
        predict_time = user_time_dict[user_id]
        user_news_set.append((1, user_id, 0, predict_time))

    return sorted(user_news_set, key=lambda d: d[3])


def sigmoid(inx):
    #print inx
    import math
    return 3/(1.0+math.exp(inx))

def get_recommend_list(user_id, user_news_dict, news_user_dict):
    '''get_recommend_list
    :param user_id: the one to predict
    :param user_news_dict: type dict, user_id=>news_id=>time
    :param news_user_dict: type dict, news_id=>user_id
    :return:recommend news list, each element is a tuple (news_id, d) sorted by d in descending order
    '''
    user_mat = dict()
    recm_news_dict = dict()
    #get user who had read the same news
    for news_id in user_news_dict[user_id].keys():
        for t_user in news_user_dict[news_id]:
            if t_user != user_id:
                user_mat.setdefault(t_user, 0)
                user_mat[t_user] += 1
    #caculate the similarity of user_id and t_user
    for t_user, contrib in user_mat.items():
        user_mat[t_user] = contrib * 1.0 / math.sqrt((len(user_news_dict[user_id]) * len(user_news_dict[t_user])))
        #joint recm_news_dict and usesr_news_dict[t_user]
        #recm_news_dict = dict(recm_news_dict, ** user_news_dict[t_user])

    #recommend
    print len(user_mat)
    for t_user, contrib in user_mat.items():
        for news_id in user_news_dict[t_user].keys():
            if news_id in user_news_dict[user_id].keys():
                continue
            recm_news_dict.setdefault(news_id, 0)
            recm_news_dict[news_id] += contrib
    return sorted(recm_news_dict.iteritems(), key=lambda d: d[1], reverse=True)


def get_recommend_news_based(user_id, user_news_dict, news_dict, predict_time):
    hot_dict = dict()
    news_hit_dict = dict()
    for t_user, news in user_news_dict.items():
        for news_id, read_time in news.items():
            news_hit_dict.setdefault(news_id, 0)
            news_hit_dict[news_id] += 1
    for news_id, hit in news_hit_dict.items():
        diff = (predict_time - news_dict[news_id])/86400
        if diff > 7:
            continue
            #hot_dict.setdefault(news_id, math.log(hit/5.0+2))
        else:
            hot_dict.setdefault(news_id, math.log(hit/5.0+2) + sigmoid(diff*1.0/7))
    recm_list = sorted(hot_dict.iteritems(), key=lambda d: d[0], reverse=True)
    recm_set = []
    for news_id, hot in recm_list:
        if news_id in user_news_dict[user_id]:
            continue
        else:
            recm_set.append((news_id, hot))
    return recm_set


def process_sorted_news(user_news_set, news_dict):
    recommend_list = []
    news_user_dict = dict()
    tu_news_dict = dict()
    for rtype, user_id, news_id, read_time in user_news_set:
        if rtype == 0:
            news_user_dict.setdefault(news_id, [])
            news_user_dict[news_id].append(user_id)

            tu_news_dict.setdefault(user_id, {})
            tu_news_dict[user_id].setdefault(news_id, read_time)

        elif rtype == 1:
            u_recm = get_recommend_list(user_id, tu_news_dict, news_user_dict)
            #recommend first two piece of news
            if len(u_recm) <= 1:
                u_recm = get_recommend_news_based(user_id, tu_news_dict, news_dict, read_time)
            #print 'len(u_recm) %d\n' % len(u_recm)
            for i in range(0, 2):
                recommend_list.append((user_id, u_recm[i][0]))
    return recommend_list


def test(recommend_list, user_news_dict):
    for user_id, news_id in recommend_list():
        if news_id in user_news_dict[user_id].keys():
            print 'test fail'
            return False
    print 'test success'
    return True

def retest():
    user_news_dict, user_time_dict, news_dict = read_set('total_set0924.txt')
    fr = open('news_read_time_UCF.csv', 'r')
    fr.readline()
    for line in fr.readlines():
        lineArr = map(int, line.split(','))
        user_id = lineArr[0]
        news_id = lineArr[1]
        if news_id in user_news_dict[user_id]:
            print 'test fail'
            return False
    print 'test success'
    return True

def process():
    '''
    read from data_set.txt and recommend the last news for each user, based the last time of reading
    write the recommend information to csv
    :return:
    '''
    print 'begin'
    user_news_dict, user_time_dict, news_dict = read_set('total_set0924.txt')
    print len(user_time_dict)
    print 'read_data finished\n'
    user_news_set = get_sorted_time_news(user_news_dict, user_time_dict)
    print len(user_news_set)
    print 'sort news fininshed\n'
    recommend_list = process_sorted_news(user_news_set, news_dict)
    print 'recommend finished\n'
    fw = open('news_read_time_UCF.csv', 'w')
    fw.write('userid, newsid\n')
    for user_id, news_id in recommend_list:
        fw.write('%d,%d\n' %(user_id, news_id))
    fw.close()
    print 'write finished\n'

    test(recommend_list=recommend_list, user_news_dict=user_news_dict)
    print 'test finished\n'

    print 'finished\n'


if __name__ == '__main__':
    process()
    retest()