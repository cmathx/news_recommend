# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-
import datetime
from cjw.CF.FinalView import *

def timeInterval(time1, time2):
    d1 = datetime.datetime(int(time1.split('/')[0]), int(time1.split('/')[1]), int(time1.split('/')[2]))
    d2 = datetime.datetime(int(time2.split('/')[0]), int(time2.split('/')[1]), int(time2.split('/')[2]))
    return (d1 - d2).days

def timeDict2Hash(t_time):
    time_ele = t_time.split('/')
    time_interval = (datetime.datetime(int(time_ele[0]), int(time_ele[1]), int(time_ele[2])) - datetime.datetime(2014, 3, 1)).days
    return time_interval

def timeHash2Dict(time_interval):
    cur_day = time_interval + 1
    return str(2014) + "\/" + str(03) + "\/" + str(cur_day)

def userViewTimeDistribute(user_final_view_news):
    fp_total_set = open('../../data/total_set.txt')
    doc_publish_time = dict()
    user_view_time = dict()
    user_news_publish_time = dict()
    user_continuous_view_time = dict()
    user_clicks = dict()
    for line in fp_total_set:
        #user_id, news_id, view_time, publish_time, title, content
        words = line.split('\t')
        view_time = words[2].split('-')[0]
        publish_time = words[3].split('-')[0]
        #doc publish time
        doc_publish_time.setdefault(words[1], publish_time)
        #user view news: view time and corresponding clicks
        user_view_time.setdefault(words[0], {})
        user_view_time[words[0]].setdefault(view_time, 0)
        user_view_time[words[0]][view_time] += 1
        #user clicks
        user_clicks.setdefault(words[0], 0)
        user_clicks[words[0]] += 1
        #user view news: publish time and corresponding clicks
        user_news_publish_time.setdefault(words[0], {})
        user_news_publish_time[words[0]].setdefault(publish_time, 0)
        user_news_publish_time[words[0]][publish_time] += 1
    fp_total_set.close()
    return user_view_time


    # cnt = 0
    # INTERVAL = 6
    # interval_cnt = 0
    # # user_clicks = sorted(user_clicks.items(), key=lambda d:d[1], reverse=True)
    # fp_user_view_time = open('../../data/user_view_time_unfocus.csv', 'w')
    # fp_user_view_days = open('../../data/user_view_time_unfocus.days.csv', 'w')
    # user_view_days = dict()
    # for user in user_clicks:
    #     user_view_days[user] = len(user_view_time[user])
    # user_view_days = sorted(user_view_days.items(), key=lambda d:d[1], reverse=True)
    # user_clicks = sorted(user_clicks.items(), key=lambda d:d[1], reverse=True)
    # for tup in user_clicks:
    #     user = tup[0]
    #     user_view_time[user] = sorted(user_view_time[user].items(), key=lambda d:d[0], reverse=False)
    #     user_news_publish_time[user] = sorted(user_news_publish_time[user].items(), key=lambda d:d[0], reverse=False)
    #     if len(user_view_time[user]) > 3:
    #         cnt += 1
    #     if len(user_view_time[user]) != 0:
    #         # if timeInterval(user_view_time[user][0][0], user_news_publish_time[user][0][0]) <= INTERVAL:
    #         #     interval_cnt += 1
    #         if len(user_view_time[user]) > 3:
    #             # print user, user_final_view_news[user]
    #             fp_user_view_time.write('%s\t%s\t' %(user, tup[1]))
    #             fp_user_view_time.write('|:\t')
    #             for tup in user_view_time[user]:
    #                 fp_user_view_time.write('[%s,%s]\t' %(tup[0], tup[1]))
    #             fp_user_view_time.write('\n')
    # fp_user_view_time.close()
    #
    # for tup in user_view_days:
    #     fp_user_view_days.write('%s,%s\n' %(tup[0], tup[1]))
    # print 'cnt = ', cnt
    # print 'interval_cnt = ', interval_cnt



if __name__ == '__main__':
    print '计算用户最后一天浏览的新闻列表'
    user_final_view_news1 = getUserFinalDayViewNews()
    user_view_time = userViewTimeDistribute(user_final_view_news1)
    # print len([user for user in user_view_time if len(user_view_time[user]) <= 3])