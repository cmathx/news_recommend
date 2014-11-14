__author__ = 'Administrator'
#_*_coding: cp936_*_

def userViewNewsRank():
    user_view_newsAndrank = dict()
    fp_total_set = open('../../data/total_set.txt', 'r')
    for line in fp_total_set:
        tup = line.split('\t')
        user_view_newsAndrank.setdefault(tup[0], {})
        user_view_newsAndrank[tup[0]].setdefault(tup[1], [tup[2], 0])
    fp_total_set.close()
    for user in user_view_newsAndrank:
        user_view_newsAndrank[user] = dict(sorted(user_view_newsAndrank[user].items(), key=lambda d:d[1][0], reverse=True))
        cnt = 0
        for user, news_viewTimeAndRank in user_view_newsAndrank[user].items():
            news_viewTimeAndRank[1] = cnt
            cnt += 1
    return user_view_newsAndrank