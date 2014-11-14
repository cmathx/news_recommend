# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-
import datetime

fp_already_read = open('../../recommend/already_read.csv', 'w')
fp_already_read.write('userid,newsid\n')
for line in open('../../data/user_item_rate.csv', 'r'):
    tup = line.split('\t')
    fp_already_read.write('%s,%s\n' %(tup[0], tup[1]))
fp_already_read.close()

# MAX_N = 1
# count = [0 for i in range(MAX_N)]
# fp_train_set = open('../../data/total_set.txt', 'r')
# for line in fp_train_set:
#     tup = line.split('\t')
#     year1 = tup[2].split('-')[0].split('/')[0]
#     month1 = tup[2].split('-')[0].split('/')[1]
#     day1 = tup[2].split('-')[0].split('/')[2]
#     year2 = tup[3].split('-')[0].split('/')[0]
#     month2 = tup[3].split('-')[0].split('/')[1]
#     day2 = tup[3].split('-')[0].split('/')[2]
#     days_interval = (datetime.datetime(int(year1), int(month1), int(day1)) - datetime.datetime(int(year2), int(month2), int(day2))).days
#     for i in xrange(MAX_N):
#         if days_interval == i:
#             print tup[2].split('-')[0], tup[3].split('-')[0]
#             count[i] += 1
# sum = 0
# for i in xrange(MAX_N):
#     sum += count[i]
#     print '%d ' %count[i]
# print 'sum = ', sum

# user_news_click = dict()
# news_user_click = dict()
# news_click = dict()
# news_pub_time = dict()
# user_final_view_time = dict()
# fp_total_set = open('../../data/total_set.txt', 'r')
# fp_test_set = open('../../data/test_set.txt', 'r')
# for line in fp_test_set:
#     tup = line.split('\t')
#     user_final_view_time.setdefault(tup[0], tup[2])
# fp_test_set.close()
# for line in fp_total_set:
#     tup = line.split('\t')
#     news_user_click.setdefault(tup[1], {})
#     news_user_click[tup[1]].setdefault(tup[0], 0)
#     if news_user_click[tup[1]][tup[0]] == 0:
#         news_click.setdefault(tup[1], 0)
#         news_pub_time.setdefault(tup[1], tup[3])
#         news_click[tup[1]] += 1
#     news_user_click[tup[1]][tup[0]] += 1
#     user_news_click.setdefault(tup[0], {})
#     user_news_click[tup[0]].setdefault(tup[1], 0)
#     user_news_click[tup[0]][tup[1]] += 1
# news_click = sorted(news_click.items(), key=lambda d:d[1], reverse=True)
# fp_news_user_click = open('../../data/news_user_click.csv', 'w')
# for tup in news_click:
#     fp_news_user_click.write('%s,%s,%s\n' %(tup[0], news_pub_time[tup[0]], len(news_user_click[tup[0]])))
# fp_total_set.close()
# fp_news_user_click.close()
# news_click = dict(news_click[0:100])
# print news_click
# #recommend
# fp_most_click_recommend = open('../../recommend/most_click_recommend.csv', 'w')
# fp_most_click_recommend.write('userid,newsid\n')
# for user, final_view_time in user_final_view_time.items():
#     cnt = 0
#     rec_num = 0
#     for news, click in news_click.items():
#         if cnt >= 100:
#             break
#         if final_view_time > news_pub_time[news]:
#             if news not in user_news_click[user]:
#                 fp_most_click_recommend.write('%s,%s\n' %(user, news))
#                 rec_num += 1
#         cnt += 1
#     print rec_num
# fp_most_click_recommend.close()

# fp_test = open('../../data/test_set.txt', 'r')
# fp_output = open('../../data/test_set_by_view_time.txt', 'w')
# lst = []
# for line in fp_test:
#     tup = line.split('\t')
#     t_tup = (tup[0], tup[1], tup[2], tup[3], tup[4])
#     lst.append(t_tup)
# lst.sort(key = lambda d : (d[2], d[0]), reverse=True)
# for t_tup in lst:
#     fp_output.write('%s\t%s\t%s\t%s\t%s\n' %(t_tup[0], t_tup[1], t_tup[2], t_tup[3], t_tup[4]))