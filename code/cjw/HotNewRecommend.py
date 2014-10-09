# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-
import IDMap

def hotNewsMap(hot_news_file, reverse_news_id_map):
    fp_hot_news = open(hot_news_file, 'r')
    real_hot_news_list = []
    for line in fp_hot_news:
        news_id = int(line)
        real_news_id = reverse_news_id_map[news_id]
        real_hot_news_list.append(real_news_id)
    return real_hot_news_list


if  __name__ == '__main__':
    reverse_user_id_map, reverse_news_id_map = IDMap.id_map('result/reverse_user_id_map.txt', \
                                                             'result/reverse_news_id_map.txt')
    hot_news_file = 'result/hotNews.txt'
    real_hot_news_list = hotNewsMap(hot_news_file, reverse_news_id_map)
    user_id_map_file = 'result/user_id_map.txt'
    fp_user_id_map = open(user_id_map_file, 'r')
    fp_hot_news_recommend = open('recommend/hot_news_recommend.csv', 'w')
    fp_hot_news_recommend.write('userid,newsid\n')
    for line in fp_user_id_map:
        word = line.split('\t')
        real_user_id = int(word[0])
        for cur_hot_news_id in real_hot_news_list:
            fp_hot_news_recommend.write('%d,%d\n' %(real_user_id, cur_hot_news_id))