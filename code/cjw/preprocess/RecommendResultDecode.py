# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-
import IDMap

def decode(reverse_user_id_map, reverse_news_id_map):
    recommend_file = 'E:/Plan-Action/CCF/myMahout/datafile/itemCF_movie_recommendation.csv'
    real_recommend_file = 'E:/Plan-Action/CCF/code/recommend/itemCF_movie_recommendation.csv'
    fp_recommend = open(recommend_file, 'r')
    fp_real_recommend = open(real_recommend_file, 'w')
    tag = True
    for line in fp_recommend:
        if tag:
            tag = False
            fp_real_recommend.write('userid,newsid\n')
        else:
            word = line.split(',')
            user_id = reverse_user_id_map[int(word[0])]
            news_id = reverse_news_id_map[int(word[1])]
            fp_real_recommend.write('%d,%d\n' %(user_id, news_id))

if __name__ == '__main__':
    reverse_user_id_map, reverse_news_id_map = IDMap.id_map('result/reverse_user_id_map.txt', \
                                                             'result/reverse_news_id_map.txt')
    decode(reverse_user_id_map, reverse_news_id_map)