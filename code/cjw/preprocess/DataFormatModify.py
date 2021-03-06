# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-
import datetime
import time

# CNT = 0
def timeFormatModify(init_time):
    init_time = init_time.split('\n')
    init_time = init_time[0]
    number = filter(str.isdigit, init_time)
    length = len(number)
    if length == 0:
        return "NULL"
    # tag = False
    # if length == 12:
        # tag = True
    if length < 12:
        minute = 0
        # tag = True
    else:
        minute = int(number[10:12])
    if length < 10:
        hour = 0
    else:
        hour = int(number[8:10])
    if length < 8:
        day = 0
    else:
        day = int(number[6:8])
    if length < 6:
        month = 0
    else:
        month = int(number[4:6])
    if length < 4:
        return 0
    else:
        year = int(number[0:4])
    ss = "%04d/%02d/%02d-%02d:%02d" %(year, month, day, hour, minute)
    # if tag:
    #     global CNT
    #     CNT += 1
    return ss

#用户浏览新闻的时间：格式转换为“%%%%/%%/%%-%%:%%”
def dataFormatModify(train_set_file):
    fp_train_set = open(train_set_file, 'r')
    fp_train_set_modify = open('../../data/train_data.modify.txt', 'w')
    ancient_time = datetime.datetime(1970, 1, 1, 0, 0, 0)

    # cjw_cnt = 0
    for line in fp_train_set:
        element = line.split('\t')
        user_id = int(element[0])
        news_id = int(element[1])
        view_time = int(element[2])
        title = element[3]
        content = element[4]
        publish_time = element[5]
        format = '%Y/%m/%d-%H:%M'
        value = time.localtime(view_time)
        # cur_time = ancient_time + datetime.timedelta(seconds = time)
        # if cmp(cur_time.strftime("%Y/%m/%d-%H:%M"), timeFormatModify(publish_time)) == -1:
        #     fp_temp.write('%d\t%d\t%s\t%s\n' %(user_id, news_id, cur_time.strftime("%Y/%m/%d-%H:%M"), timeFormatModify(publish_time)))
        view_time_after_transfer = time.strftime(format, value)
        publish_time_after_transfer = timeFormatModify(publish_time)
        fp_train_set_modify.write('%d\t%d\t%s\t%s\t%s\t%s\n' %(user_id, news_id, view_time_after_transfer, \
            publish_time_after_transfer, title, content))
        # if cmp(view_time_after_transfer, publish_time_after_transfer) == -1:
        #     cjw_cnt += 1
    # print 'cjw_cnt = ', cjw_cnt

#新闻发布的时间：缺失数据（为NULL）修改为“所有浏览该条新闻的最早时间”
def missDataComplete():
    fp_train_set_modify = open('../../data/train_data.modify.txt', 'r')
    fp_train_set_modify_final = open('../../data/train_data.modify.final.txt', 'w')
    fp_train_set_modify_sort = open('../../data/train_data.modify.sort.txt', 'w')
    tlst = []
    lessCnt = 0
    for line in fp_train_set_modify:
        ele = line.split('\t')
        #user_id, news_id, view_time, publish_time, title, content
        ll = [int(ele[0]), int(ele[1]), ele[2], ele[3], ele[4], ele[5]]
        tlst.append(ll)

    tlst.sort(key = lambda d : (d[3], d[1], d[2]), reverse=False)
    tag = True
    for ele in tlst:
        fp_train_set_modify_sort.write('%d\t%d\t%s\t%s\t%s\t%s' %(ele[0], ele[1], ele[2], ele[3], ele[4], ele[5]))
        if ele[3] == "NULL":
            print ele[3]
            if tag:
                tag = False
                ele[3] = ele[2]
                pre_news_id = ele[1]
                pre_time = ele[2]
            else:
                if ele[1] == pre_news_id:
                    ele[3] = pre_time
                else:
                    ele[3] = ele[2]
                    pre_time = ele[2]
                    pre_news_id = ele[1]
        fp_train_set_modify_final.write('%d\t%d\t%s\t%s\t%s\t%s' %(ele[0], ele[1], ele[2],\
            ele[3], ele[4], ele[5]))
        if cmp(ele[2], ele[3]) == -1:
            print ele[2], ele[3], ele[4], ele[5]
            lessCnt += 1
    print 'lessCnt = ', lessCnt

if __name__ == '__main__':
    train_set_file = '../../data/train_data.edit.txt'
    dataFormatModify(train_set_file)
    missDataComplete()
    # print 'CNT = ', CNT
    # fp_train_set = open('../../data/train_data.edit.txt', 'r')
    # fp_pub_time_null_set = open('../../data/pub_time_null_news.txt', 'w')
    # cnt = 0
    # null_click = 0
    # total = 0
    # user_set = dict()
    # doc_set = dict()
    # click1 = 0
    # for line in fp_train_set:
    #     element = line.split('\t')
    #     user_id = int(element[0])
    #     news_id = int(element[1])
    #     view_time = int(element[2])
    #     title = element[3]
    #     content = element[4]
    #     publish_time = element[5]
    #     if len(publish_time) == 6 and len(content) == 4:
    #         null_click += 1
    #         if user_set.has_key(user_id) == False:
    #             user_set[user_id] = 1
    #         if doc_set.has_key(news_id) == False:
    #             fp_pub_time_null_set.write('%s\t%s\t%s\t%s' %(news_id, title, content, publish_time))
    #             doc_set[news_id] = 1
    #             cnt += 1
    #     total += 1
    # print cnt, null_click, total
    # print len(user_set)

#有81条新闻新闻发布时间，正文内容以及标题全部都为空，总点击次数2868次，有1955个用户多多少少点击过这些新闻
#234条新闻发布时间和正文内容均为空，总点击次数4343次，有2454个用户多多少少点击过这些新闻
#330条新闻发布时间为NULL，总点击次数13383次,有4267各用户多多少少点击过这些新闻
#有336次点击的行为，用户浏览的时间早于新闻发布时间
#需要过滤的新闻
# def mycmp(m1, m2):
#     if m1[3] > m2[3]:
#         return 1
#     else:
#         if m1[1] > m2[1]:
#             return 1
#         else:
#             if m1[2] < m2[2]:
#                 return 1
#             else:
#                 return -1