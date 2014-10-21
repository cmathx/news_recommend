# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

def computeInitialRateArray(train_set_file, user_count, news_count):
    fp_train_set = open(train_set_file, 'r')
    user_news_initial_rate_array = [[0 for i in xrange(news_count)] for j in xrange(user_count)]
    for line in fp_train_set:
        line = line.strip('\t')
        if line == '':
            continue
        word = line.split('\t')
        user_id = int(word[0])
        news_id = int(word[1])
        # read_time = int(word[2])
        # title = word[3]
        # content = word[4]
        # publish_time = word[5]
        user_news_initial_rate_array[user_id][news_id] = 1
    return user_news_initial_rate_array

def printInitialRate(user_news_initial_rate_array, user_count, news_count):
    fp_inital_rate = open('E:/Plan-Action/CCF/myMahout/datafile/original_rate.txt', 'w')
    initial_rate_list = []
    max = -1
    maxi = -1
    maxj = -1
    for i in xrange(user_count):
        # tag = True
        for j in xrange(news_count):
            if user_news_initial_rate_array[i][j] != 0:
                tList = (i, j, user_news_initial_rate_array[i][j])
                initial_rate_list.append(tList)
            # if user_news_initial_rate_array[i][j] > max:
            #     max = user_news_initial_rate_array[i][j]
            #     maxi = i
            #     maxj = j
            # if tag:
            #     tag = False
            #     fp_inital_rate_array.write('%d' %(user_news_initial_rate_array[i][j]))
            # else:
            #     fp_inital_rate_array.write(' %d' %(user_news_initial_rate_array[i][j]))
        # fp_inital_rate_array.write('\n')
    print 'max = %d i = %d j = %d\n' %(max, maxi, maxj)
    initial_rate_list.sort(key = lambda initial_rate_list : initial_rate_list[2], reverse = True)
    for tList in initial_rate_list:
        fp_inital_rate.write('%d\t%d\t%d\n' %(tList[0], tList[1], tList[2]))

def userReadNewsInfo(user_news_initial_rate_array, user_count, news_count):
    fp_user_read_news_info = open('result/user_read_news_info.csv', 'w')
    fp_user_read_news_info.write('userid,newsid\n')
    for i in xrange(user_count):
        for j in xrange(news_count):
            if(user_news_initial_rate_array[i][j] != 0):
                fp_user_read_news_info.write('%d,%d\n' %(i, j))

if __name__ == '__main__':
    user_count = 10000
    news_count = 6183
    user_news_initial_rate_array = computeInitialRateArray('result/train_data.map.txt', user_count, news_count)
    printInitialRate(user_news_initial_rate_array, user_count, news_count)
    # userReadNewsInfo(user_news_initial_rate_array, user_count, news_count)