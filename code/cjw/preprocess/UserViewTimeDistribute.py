# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-
import datetime

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

def userViewTimeDistribute():
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
        doc_publish_time.setdefault(words[1], publish_time)
        user_view_time.setdefault(words[0], {})
        user_view_time[words[0]].setdefault(view_time, 0)
        user_view_time[words[0]][view_time] += 1
        user_clicks.setdefault(words[0], 0)
        user_clicks[words[0]] += 1
        user_news_publish_time.setdefault(words[0], {})
        user_news_publish_time[words[0]].setdefault(publish_time, 0)
        user_news_publish_time[words[0]][publish_time] += 1
    fp_total_set.close()
    for user_clicks_tup in user_clicks:
        user = user_clicks_tup[0]
        user_view_time[user] = sorted(user_view_time[user].items(), key=lambda d:d[0], reverse=False)
    return doc_publish_time, user_view_time
    # for user, view_time_clicks in user_view_time.items():
    #     user_continuous_view_time.
    # cnt = 0
    # cnt1 = 0
    # INTERVAL = 6
    # interval_cnt = 0
    # user_clicks = sorted(user_clicks.items(), key=lambda d:d[1], reverse=True)
    # fp_user_view_time = open('../../data/user_view_time.csv', 'w')
    # for user_clicks_tup in user_clicks:
    #     user = user_clicks_tup[0]
    #     user_view_time[user] = sorted(user_view_time[user].items(), key=lambda d:d[0], reverse=False)
    #     user_news_publish_time[user] = sorted(user_news_publish_time[user].items(), key=lambda d:d[0], reverse=False)
    #     if len(user_view_time[user]) <= 1:
    #         cnt += 1
    #     if len(user_view_time[user]) <= 1:
    #         if timeInterval(user_view_time[user][0][0], user_news_publish_time[user][0][0]) <= INTERVAL:
    #             interval_cnt += 1
    #         fp_user_view_time.write('%s\t%s\t' %(user, user_clicks_tup[1]))
    #         for tup in user_view_time[user]:
    #             fp_user_view_time.write('[%s,%s]\t' %(tup[0], tup[1]))
    #         fp_user_view_time.write('|:\t')
    #         if len(user_news_publish_time[user]) <= 2:
    #             cnt1 += 1
    #             for tup in user_news_publish_time[user]:
    #                 fp_user_view_time.write('[%s,%s]\t' %(tup[0], tup[1]))
    #         fp_user_view_time.write('\n')
    # fp_user_view_time.close()
    # print 'cnt = ', cnt
    # print 'cnt1 = ', cnt1
    # print 'interval_cnt = ', interval_cnt

if __name__ == '__main__':
    userViewTimeDistribute()