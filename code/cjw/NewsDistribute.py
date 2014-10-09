# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

def newsDistribute(train_set_file):
    news_distribute_dict = {}
    fp_train_set = open(train_set_file, 'r')
    for line in fp_train_set:
        tup = line.split('\t')
        #user_id, news_id, view_time, publish_time, title, content
        news_id = tup[0]
        news_distribute_dict.setdefault(news_id, 1)
        news_distribute_dict[news_id] += 1
        # publish_time = tup[3].split('-')[0]
        # news_distribute_dict.setdefault(publish_time, 1)
        # news_distribute_dict[publish_time] += 1
    return news_distribute_dict

def printNewsDateDistribute(news_distribute_dict):
    fp_news_distribute = open('../data/user_click_count.csv', 'w')
    news_distribute_list = sorted(news_distribute_dict.iteritems(), key = lambda d:d[1], reverse=True)
    for item in news_distribute_list:
        fp_news_distribute.write('%s,%s\n' %(item[0], item[1]))

if __name__ == '__main__':
    news_distribute_dict = newsDistribute('../data/total_set.txt')
    printNewsDateDistribute(news_distribute_dict)