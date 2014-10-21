# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

TOTAL_SET_FILE = '../data/total_set.txt'
TEST_SET_FILE = '../data/test_set.txt'

#计算每天发布的新闻以及各新闻的点击次数
def newsInfoCount(set_file):
    fp_total_set = open(set_file, 'r')
    publish_time_news_dict = {}
    news_click_dict = {}
    for line in fp_total_set:
        ele = line.split('\t')
        publish_time = ele[3]
        publish_time = publish_time.split('-')[0]
        news_id = ele[1]
        if news_click_dict.has_key(news_id) == False:
            news_click_dict[news_id] = 1
        else:
            news_click_dict[news_id] += 1
        if publish_time_news_dict.has_key(publish_time) == False:
            t_dict = {}
            t_dict[news_id] = news_click_dict[news_id]
            publish_time_news_dict[publish_time] = t_dict
        else:
            publish_time_news_dict[publish_time][news_id] = news_click_dict[news_id]
    for item in publish_time_news_dict:
        sorted(publish_time_news_dict[item].iteritems(), key = lambda d : d[1], reverse=True)
    # total_count = 0
    # for item in publish_time_news_dict:
    #     for d_item in publish_time_news_dict[item]:
    #         total_count += publish_time_news_dict[item][d_item]
    # print 'total_count = ', total_count
    return publish_time_news_dict

NEARLY_DAYS = 2
#计算出距离发布新闻事件最近几天的新闻
def getNearlyNews(view_time):
    publish_time_news_dict = newsInfoCount(TOTAL_SET_FILE)
    # fp_test_set = open('../data/test_set.txt', 'r')
    nearly_news_list = []
    view_year = int(view_time.split('/')[0])
    view_month = int(view_time.split('/')[1])
    view_day = int(view_time.split('/')[2])
    for i in xrange(NEARLY_DAYS):
        import datetime
        t_datetime = datetime.datetime(view_year, view_month, view_day) - datetime.timedelta(i)
        t_publish_time = '%04d/%02d/%02d' %(t_datetime.year, t_datetime.month, t_datetime.day)
        for t_news_id in publish_time_news_dict[t_publish_time]:
            s_news_id = '%s' %(t_news_id)
            nearly_news_list.append(s_news_id)
    return nearly_news_list

    # for line in fp_test_set:
    #     tup = line.split('\t')
    #     user_id = tup[0]

#计算出3月份每天最近几天发布出来的新闻，key:时间，value:所需的新闻
def getNearlyNewsForEveryDay():
    nearly_news_dict = {}
    for i in xrange(1, 32):
        cur_view_time = '2014/03/%02d' %i
        nearly_news_dict[cur_view_time] = getNearlyNews(cur_view_time)
    return nearly_news_dict

#计算出各用户最后浏览新闻那天之前几天发布的所有新闻，key:用户，value:所需的新闻
def getNearlyNewForFinalViewTime(nearly_news_dict):
    nearly_news_for_final_viewtime_dict = {}
    fp_test_set = open(TEST_SET_FILE, 'r')
    for line in fp_test_set:
        tup = line.split('\t')
        user_id = tup[0]
        final_view_time = tup[2].split('-')[0]
        nearly_news_for_final_viewtime_dict[user_id] = nearly_news_dict[final_view_time]
    return nearly_news_for_final_viewtime_dict

#generate news list which viewed time is nearly closed to the final viewed time
def generateNearlyNewsForFinalTimeBySpecificUserDict():
    #nearly_news_dict: (key,value)-(view_time, total nearly viewed news)
    nearly_news_dict = getNearlyNewsForEveryDay()
    #nearly_news_for_final_time_by_specific_user_dict: (key,value)-(user, total nearly viewed news )
    nearly_news_for_final_time_by_specific_user_dict = getNearlyNewForFinalViewTime(nearly_news_dict)
    print 'generate nearly_news_for_final_time_dict finished'
    return nearly_news_for_final_time_by_specific_user_dict

