# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

def computeF1(recommend_file, test_set_file):
    hits = 0
    recommend_num = 0
    user_news_recommend_dict = {}
    fp_recommend = open(recommend_file, 'r')
    tag = True
    for line in fp_recommend:
        if tag:
            tag = False
        else:
            recommend_num += 1
            tup = line.split(',')
            user_id = int(tup[0])
            news_id = int(tup[1])
            if user_news_recommend_dict.has_key(user_id) == False:
                t_list = [news_id]
                user_news_recommend_dict[user_id] = t_list
            else:
                user_news_recommend_dict[user_id].append(news_id)
    fp_test_set = open(test_set_file, 'r')
    for line in fp_test_set:
        tup = line.split('\t')
        user_id = int(tup[0])
        news_id = int(tup[1])
        if user_news_recommend_dict.has_key(user_id) == False:
            continue
        news_recommend_for_specific_user = user_news_recommend_dict[user_id]
        flag = False
        for t_news in news_recommend_for_specific_user:
            if t_news == news_id:
                flag = True
                hits += 1
                break
    precision = 1.0 * hits / recommend_num
    recall = 1.0 * hits / 10000
    return recommend_num, precision, recall, 2.0 * precision * recall / (precision + recall)

if __name__ == '__main__':
    recommend_file = '../recommend/UCFRecommend.csv'
    test_set_file = '../data/test_set.txt'
    recommend_num, precision, recall, F1= computeF1(recommend_file, test_set_file)
    print 'recommend number = ', recommend_num
    print 'hits = ', int(1.0 * recommend_num * precision)
    print 'precision = ', precision
    print 'recall = ', recall
    print 'F1 =', F1
