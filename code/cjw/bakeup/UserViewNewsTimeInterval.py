# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

import datetime

def userViewNewsTimeInterval(train_set_file):
    fp_train_set = open(train_set_file, 'r')
    time_interval_dict = {}
    tag = True
    for line in fp_train_set:
        tup = line.split('\t')
        user_id = int(tup[0])
        view_time = tup[2].split('-')[0].split('/')
        cur_year = int(view_time[0])
        cur_month = int(view_time[1])
        cur_day = int(view_time[2])
        time_interval_dict.setdefault(user_id, [0, 0])
        time_interval_dict[user_id][1] += 1
        if tag:
            tag = False
            pre_user_id = user_id
        else:
            if pre_user_id == user_id:
                cur_time_interval = (datetime.datetime(pre_year, pre_month, pre_day) - datetime.datetime(cur_year, cur_month, cur_day)).days
                if cur_time_interval == 0:
                    time_interval_dict[user_id][0] += 1#cur_time_interval
            else:
                pre_user_id = user_id
        pre_year = int(view_time[0])
        pre_month = int(view_time[1])
        pre_day = int(view_time[2])
    time_interval_list = sorted(time_interval_dict.iteritems(), key = lambda d:1.0 * d[1][0] / d[1][1], reverse=True)
    fp_time_interval = open('time_interval.csv', 'w')
    sum1 = 0
    sum2= 0
    for item in time_interval_list:
        sum1 += item[1][0]
        sum2 += item[1][1]
        fp_time_interval.write('%d,%d,%d,%.2lf\n' %(item[0], item[1][0], item[1][1], 1.0 * item[1][0] / item[1][1]))
    print 1.0 * sum1 / sum2

if __name__ == '__main__':
    userViewNewsTimeInterval('../../data/total_set.txt')

