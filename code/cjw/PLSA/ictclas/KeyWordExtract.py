# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

import pynlpir
import time
import datetime

def newsContentMap(total_set):
    newsMap = {}
    fp_total_set = open(total_set, 'r')
    for line in fp_total_set:
        word = line.split('\t')
        news_id = word[1]
        news_title = word[4]
        news_content = word[5]
        if newsMap.has_key(news_id) == False:
            newsMap[news_id] = news_content
    return newsMap

def newsContentSplit(newMap):
    newsTotalWordMap = {}
    for key in newMap:
        newsTotalWordMap[key] = pynlpir.nlpir.ParagraphProcess(newMap[key], False)
    return newsTotalWordMap

if __name__ == '__main__':
    d1 = datetime.datetime.now()
    pynlpir.open()
    newsMap = newsContentMap('E://Plan-Action//CCF//news_recommend//code//data//total_set.txt')
    newsTotalWordMap = newsContentSplit(newsMap)
    pynlpir.close()
    d2 = datetime.datetime.now()
    d = d2 - d1
    d.strftime("%M:%S")
