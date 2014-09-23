# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

def splitData():
    fp_data = open('data/train_data.sort.txt', 'r')
    data_list = []
    for line in fp_data:
        element = line.split('\t')
        user_id = int(element[0])
        news_id = int(element[1])
        time = int(element[2])
        title = element[3]
        content = element[4]
        publish_time = element[5]
        t_list = (user_id, news_id, time, title, content, publish_time)
        data_list.append(t_list)
    data_list.sort(key = lambda d:(d[0], d[2]), reverse = True)
    fp_train_set = open('data/train_set.txt', 'w')
    fp_test_set = open('data/test_set.txt', 'w')
    fp_total_set = open('data/total_set.txt', 'w')
    tag = True
    for item in data_list:
        fp_total_set.write('%d\t%d\t%d\t%s\t%s\t%s' %(int(item[0]), int(item[1]), int(item[2]), \
                                                     item[3], item[4], item[5]))
        if tag:
            tag = False
            cur_user_id = int(item[0])
            fp_test_set.write('%d\t%d\t%d\t%s\t%s\t%s' %(int(item[0]), int(item[1]), int(item[2]),\
                                                          item[3], item[4], item[5]))
        else:
            if cur_user_id != int(item[0]):
                fp_test_set.write('%d\t%d\t%d\t%s\t%s\t%s' %(int(item[0]), int(item[1]), int(item[2]),\
                                                              item[3], item[4], item[5]))
                cur_user_id = int(item[0])
            else:
                fp_train_set.write('%d\t%d\t%d\t%s\t%s\t%s' %(int(item[0]), int(item[1]), int(item[2]),\
                                                               item[3], item[4], item[5]))

if __name__ == '__main__':
    splitData()
    fp_test_set = open('data/test_set.txt', 'r')
    lst = []
    for line in fp_test_set:
        word = line.split('\t')
        tList = (int(word[0]), int(word[1]), int(word[2]), word[3], word[4], word[5])
        lst.append(tList)
    lst.sort(key = lambda d : d[5], reverse = True)
    fp_test_set_sort_by_time = open('data/test_set_sort_by_time.txt', 'w')
    for item in lst:
        tmp = item[5].split('\n')
        fp_test_set_sort_by_time.write('%d\t%d\t%s\t%s\n' %(int(item[0]), int(item[1]), tmp[0], item[3]))