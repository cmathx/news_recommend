# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

def id_map(user_id_map_file, news_id_map_file):
    user_id_map = {}
    news_id_map = {}
    fp_user_id_map = open(user_id_map_file, 'r')
    fp_news_id_map = open(news_id_map_file, 'r')
    for line in fp_user_id_map:
        word = line.split('\t')
        user_id_map[int(word[0])] = int(word[1])
    for line in fp_news_id_map:
        word = line.split('\t')
        news_id_map[int(word[0])] = int(word[1])
    return user_id_map, news_id_map
