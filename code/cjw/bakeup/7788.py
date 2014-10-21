# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-
import datetime

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

fp_test = open('../../data/test_set.txt', 'r')
fp_output = open('../../data/test_set_by_view_time.txt', 'w')
lst = []
for line in fp_test:
    tup = line.split('\t')
    t_tup = (tup[0], tup[1], tup[2], tup[3], tup[4])
    lst.append(t_tup)
lst.sort(key = lambda d : (d[2], d[0]), reverse=True)
for t_tup in lst:
    fp_output.write('%s\t%s\t%s\t%s\t%s\n' %(t_tup[0], t_tup[1], t_tup[2], t_tup[3], t_tup[4]))