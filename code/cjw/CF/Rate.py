# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

def getUserItemRate():
    user_item_rate = dict()
    fp_total_set = open('../../data/total_set.txt', 'r')
    for line in fp_total_set:
        words = line.split('\t')
        user_item_rate.setdefault(words[0], {})
        user_item_rate[words[0]].setdefault(words[1], 0)
        user_item_rate[words[0]][words[1]] += 1
    fp_rate_set = open('../../data/user_item_rate.csv', 'w')
    for user, item_score in user_item_rate.items():
        for item in item_score.keys():
            fp_rate_set.write('%s\t%s\t%s\n' %(user, item, item_score[item]))
    fp_rate_set.close()
    fp_total_set.close()