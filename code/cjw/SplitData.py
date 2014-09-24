# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

#输入数据格式转换后以及缺失数据处理完的数据，输出用户浏览的新闻以及最后一条浏览的新闻
def splitData():
    fp_data = open('../data/total_set.txt', 'r')
    data_list = []
    for line in fp_data:
        ele = line.split('\t')
        #user_id, news_id, view_time, publish_time, title, content
        t_list = [int(ele[0]), int(ele[1]), ele[2], ele[3], ele[4], ele[5]]
        data_list.append(t_list)
    data_list.sort(key = lambda d:(d[0], d[2]), reverse = True)
    fp_train_set = open('../data/train_set1.txt', 'w')
    fp_test_set = open('../data/test_set1.txt', 'w')
    fp_total_set = open('../data/total_set1.txt', 'w')
    tag = True
    for item in data_list:
        fp_total_set.write('%d\t%d\t%s\t%s\t%s\t%s' %(int(item[0]), int(item[1]), item[2], \
                                                     item[3], item[4], item[5]))
        if tag:
            tag = False
            cur_user_id = int(item[0])
            fp_test_set.write('%d\t%d\t%s\t%s\t%s\t%s' %(int(item[0]), int(item[1]), item[2],\
                                                          item[3], item[4], item[5]))
        else:
            if cur_user_id != int(item[0]):
                fp_test_set.write('%d\t%d\t%s\t%s\t%s\t%s' %(int(item[0]), int(item[1]), item[2],\
                                                              item[3], item[4], item[5]))
                cur_user_id = int(item[0])
            else:
                fp_train_set.write('%d\t%d\t%s\t%s\t%s\t%s' %(int(item[0]), int(item[1]), item[2],\
                                                               item[3], item[4], item[5]))

if __name__ == '__main__':
    splitData()
    #输出用户最后浏览的一条新闻，并按照发布时间进行排序
    fp_test_set = open('../data/test_set1.txt', 'r')
    lst = []
    for line in fp_test_set:
        word = line.split('\t')
        tList = (int(word[0]), int(word[1]), word[2], word[3], word[4], word[5])
        lst.append(tList)
    lst.sort(key = lambda d : (d[0], d[2]), reverse = True)
    fp_test_set_sort_by_time = open('../data/test_set_sort_by_publish_time1.txt', 'w')
    for item in lst:
        fp_test_set_sort_by_time.write('%d\t%d\t%s\t%s\t%s\t%s' %(int(item[0]), int(item[1]), item[2], item[3], item[4], item[5]))