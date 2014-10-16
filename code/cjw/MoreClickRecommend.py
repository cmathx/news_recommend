# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

from cjw.PLSA.plsaRecommend import createDocMapAndClickInfo
from cjw.getNearlyDayNews import generateNearlyNewsForFinalTimeBySpecificUserDict
from cjw.computeF1 import printF1Info

print '建立doc映射表'
doc_set_file = 'gensim/data/document.csv'
total_set_file = '../data/total_set.txt'
user_set, doc_set, doc_map1, doc_map2, doc_click_count, user_doc_click_count = \
    createDocMapAndClickInfo(total_set_file, doc_set_file)

#generate news list which viewed time is nearly closed to the final viewed time
nearly_news_for_final_time_by_specific_user_dict = generateNearlyNewsForFinalTimeBySpecificUserDict()

recommend_file = '../recommend/more_clicks_recommend.csv'
fp_more_clicks_recommend = open(recommend_file, 'w')
fp_more_clicks_recommend.write('userid,newsid\n')
RECOMMEND_NUM = 20
for user_id in user_set:
    nearly_news = nearly_news_for_final_time_by_specific_user_dict[user_id]
    nearly_news_clicks = dict()
    for t_news in nearly_news:
        nearly_news_clicks[t_news] = doc_click_count[t_news]
    sorted_nearly_news_click = sorted(nearly_news_clicks, key=lambda d:d[1], reverse=True)
    cnt = 0
    for nearly_news_id in sorted_nearly_news_click:
        if cnt == RECOMMEND_NUM:
            break
        if nearly_news_id not in user_doc_click_count[user_id]:
            cnt += 1
            fp_more_clicks_recommend.write('%s,%s\n' %(user_id, nearly_news_id))

test_set_file = '../data/test_set.txt'
# printF1Info(recommend_file)
