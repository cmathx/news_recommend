# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

class News:
    news_id = -1
    news_click_count = 0
    def __init__(self, _news_id, _news_click_count):
        news_id = _news_id
        news_click_count = _news_click_count

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

def hotNewsRecommend(test_set_file, publish_time_news_dict):
    fp_test_set = open(test_set_file, 'r')
    fp_hot_news_recommend = open('../recommend/hot_news_recommend.csv', 'w')
    fp_hot_news_recommend.write('userid,newsid\n')
    for line in fp_test_set:
        ele = line.split('\t')
        # user_id = int(ele[0])
        publish_time = ele[3]
        publish_time = publish_time.split('-')[0]
        if publish_time_news_dict.has_key(publish_time) == False:
            continue
        t_dict = publish_time_news_dict[publish_time]
        cnt = 0
        for news in t_dict:
            if cnt < 10:
                cnt += 1
                fp_hot_news_recommend.write('%s,%d\n' %(ele[0], int(news)))
            else:
                break

if __name__ == '__main__':
   set_file = '../data/train_set.txt'
   publish_time_news_dict = newsInfoCount(set_file)
   test_set_file = '../data/test_set_sort_by_publish_time1.txt'
   hotNewsRecommend(test_set_file, publish_time_news_dict)