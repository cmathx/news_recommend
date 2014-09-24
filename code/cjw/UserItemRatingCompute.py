# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

def userItemRatingCompute(train_set_file):
    fp_train_set = open(train_set_file, 'r')
    prefs = {}
    for line in fp_train_set:
        tup = line.split('\t')
        user_id = int(tup[0])
        news_id = int(tup[1])
        #user_id, news_id, view_time, publish_time, title, content
        if prefs.has_key(user_id) == False:
            prefs.setdefault(user_id, {})
            prefs[user_id][news_id] = 1
        else:
            # if prefs[user_id].has_key(news_id) == False:
            prefs[user_id][news_id] = 1
            # else:
            #     prefs[user_id][news_id] += 1
    fp_init_rate = open('../data/user-item-ratings.csv', 'w')
    click_dict = {}
    min = 100000
    max = -1
    for item1 in prefs:
        for item2 in prefs[item1]:
            fp_init_rate.write('"%d";"%d";"%d"\n' %(item1, item2, prefs[item1][item2]))
            click_dict.setdefault(prefs[item1][item2], 1)
            click_dict[prefs[item1][item2]] += 1
            if prefs[item1][item2] < min:
                min = prefs[item1][item2]
            if prefs[item1][item2] > max:
                max = prefs[item1][item2]
    print min, max
    fp_click_count = open('../data/click_count.csv', 'w')
    sorted(click_dict.iteritems(), key = lambda d : d[1], reverse=True)
    for item in click_dict:
        fp_click_count.write('%s,%d\n' %(item, click_dict[item]))
    return prefs

if __name__ == '__main__':
    train_set_file = '../data/total_set.txt'
    userItemRatingCompute(train_set_file)