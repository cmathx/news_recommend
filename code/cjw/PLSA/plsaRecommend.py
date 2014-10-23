# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-
import os
import glob
import sys
import datetime
import pynlpir
import plsaForNewsCluster
import getNearlyDayNews

def createDocMapAndClickInfo(total_set_file, doc_set_file):
    user_map_r2v = {}
    user_map_v2r = {}
    doc_map_r2v = {}  #doc map(Facilitate the calculation in PLSA)
    doc_map_v2r = {}  #not use
    user_set = set()  #total users
    doc_set = set()  #total documents
    doc_click_count = {}  #clicks in every document
    user_doc_click_count = {}  #clicks in specific document from specific user

    if os.path.isfile(doc_set_file):
        is_write_need_file = True
    else:
        is_write_need_file = False
    fp_total_set = open(total_set_file, 'r')
    if is_write_need_file == False:
        fp_doc_set = open(doc_set_file, 'w')
        fp_doc_map_r2v = open('../PLSA/data/doc_map_r2v.csv', 'w')
        fp_doc_map_v2r = open('../PLSA/data/doc_map_v2r.csv', 'w')
        fp_doc_click_count = open('../PLSA/data/doc_click_count.csv', 'w')
        fp_user_doc_click_count = open('../PLSA/data/user_doc_click_count.csv', 'w')
    cnt = 0
    cnt1 = 0
    pynlpir.open()
    for line in fp_total_set:
        word = line.split('\t')
        user_set.add(word[0])
        doc_set.add(word[1])
        doc_click_count.setdefault(word[1], 0)
        doc_click_count[word[1]] += 1
        user_doc_click_count.setdefault(word[0], {})
        if user_doc_click_count[word[0]].has_key(word[1]) == False:
            user_doc_click_count[word[0]][word[1]] = 0
        user_doc_click_count[word[0]][word[1]] += 1
        if user_map_r2v.has_key(word[0]) == False:
            user_map_r2v[word[0]] = cnt1
            user_map_v2r[cnt1] = word[0]
            cnt1 += 1
        if doc_map_r2v.has_key(word[1]) == False:
            doc_map_r2v[word[1]] = cnt
            doc_map_v2r[cnt] = word[1]
            cnt += 1
            if is_write_need_file == False:
                title_split_result = pynlpir.nlpir.ParagraphProcess(word[4], True)
                content_split_result = pynlpir.nlpir.ParagraphProcess(word[5], True)
                #make sure that news id map is true
                fp_doc_set.write('%s\t%s\t%s' %(word[1], title_split_result, content_split_result))#, content_split_result))

    # doc_map = sorted(doc_map_r2v.items(), key=lambda d:d[1], reverse=False)
    if is_write_need_file == False:
        for d, dtag in doc_map_r2v.items():
            fp_doc_map_r2v.write('%s %d\n' %(d, dtag))
        for dtag, d in doc_map_v2r.items():
            fp_doc_map_v2r.write('%d %s\n' %(dtag, d))
        for d, dclicks in doc_click_count.items():
            fp_doc_click_count.write('%s %d\n' %(d, dclicks))
    user_clicks = 0
    for u, uitem in user_doc_click_count.items():
        for d in uitem.keys():
            if is_write_need_file == False:
                fp_user_doc_click_count.write('%s %s %d\n' %(u, d, uitem[d]))
            user_clicks += uitem[d]
    print 'user clicks = ', user_clicks

    pynlpir.close()
    if is_write_need_file == False:
        fp_doc_set.close()
        fp_total_set.close()
    print 'number of users:', len(user_set)
    print 'number of documents:', len(doc_set)

    print 'createDocMap end'
    #user_set (real_user_id) doc_set(real_news_id)
    #doc_map_r2v (real_news_id -> virtual_news_id)
    #doc_map_v2r (virtual_news_id -> real_news_id)
    #doc_click_count (real_news_id -> clicks)
    #user_doc_click_count (real_user_id, real_news_id -> clicks)
    return user_set, doc_set, user_map_r2v, user_map_v2r, doc_map_r2v, doc_map_v2r, doc_click_count, user_doc_click_count

# def splitNewsTitleAndContent(doc_set_file):
#     fp_doc_set_file = open(doc_set_file, 'r')
#     for line in fp_doc_set_file:
#         element = line.split('\t')

def computeNewsCluster(corpus, number_of_topics):
    fp_doc_cluster = open('data//doc_cluster.csv', 'w')
    D = len(corpus.documents) # number of documents
    news_cluster = {}
    for d in range(D):
        topic_prob = corpus.document_topic_prob[d, :]
        max_prob = -1
        maxi = -1
        for i in range(number_of_topics):
            if topic_prob[i] > max_prob:
                max_prob = topic_prob[i]
                maxi = i
        news_cluster[d] = maxi
        fp_doc_cluster.write('%d,%d\n' %(d, news_cluster[d]))
    return news_cluster  #i, cluster which news i belongs to

def getNewsClusterFromDisk(news_cluster_file):
    news_cluster = {}
    fp_news_cluster = open(news_cluster_file, 'r')
    for line in fp_news_cluster:
        word = line.split(',')
        news_cluster[int(word[0])] = int(word[1])
    return news_cluster

def computeUserItemScoreAndRecommend(user_set, doc_set, doc_map1, doc_click_count, user_doc_click_count, news_cluster, K, nearly_news_for_final_time_by_specific_user_dict):
    cluster_click_count = {}  #total clicks in specific cluster of news
    for d, cnt in doc_click_count.items():
        clu = news_cluster[doc_map1[d]]
        cluster_click_count.setdefault(clu, 0)
        cluster_click_count[clu] += cnt

    fp_recommend = open('../../../code/recommend/plsa_recommend.csv', 'w')
    fp_recommend.write('userid,newsid\n')
    starttime = datetime.datetime.now()
    print 'start to recommend'
    for u in user_set:
        user_click_total_count = 0  #total clicks from specific user
        user_cluster_click_total_count = {}  #clicks in specific cluster of news from specific user
        for d, cnt in user_doc_click_count[u].items():
            clu = news_cluster[doc_map1[d]]
            user_click_total_count += cnt
            user_cluster_click_total_count.setdefault(clu, 0)
            user_cluster_click_total_count[clu] += cnt

        user_item_socre = {}
        for d in doc_set:
            if d not in user_doc_click_count[u]:
                user_item_socre.setdefault(d, 0)
                for clu, cnt in user_cluster_click_total_count.items():
                    p_clu_user = 1.0 * user_cluster_click_total_count[clu] / user_click_total_count
                    p_clu_user = p_clu_user * doc_click_count[d] / cluster_click_count[news_cluster[doc_map1[d]]]
                    user_item_socre[d] += p_clu_user
        topk_user_item_score = sorted(user_item_socre.items(), key=lambda d:d[1], reverse=True)[0:K]
        # cur_recommend_num = 0
        for obj in topk_user_item_score:
            # if cur_recommend_num == K:
            #     break
            d = obj[0]
            #only consider nearly day news
            # if d in nearly_news_for_final_time_by_specific_user_dict[u]:
            fp_recommend.write('%s,%s\n' %(u, d))
                # cur_recommend_num += 1
    fp_recommend.close()
    endtime = datetime.datetime.now()
    minutes = (endtime - starttime).seconds / 60
    print "Recommend costs %d minutes and %d seconds" %(minutes, (endtime - starttime).seconds - minutes * 60)


if __name__ == '__main__':
    total_set_file = '../../data/total_set.txt'
    doc_set_file = 'data//document.csv'
    user_set, doc_set, doc_map1, doc_map2, doc_click_count, user_doc_click_count = createDocMapAndClickInfo(total_set_file, doc_set_file)

    news_cluster_file = 'data//doc_cluster.csv'
    if os.path.isfile(news_cluster_file):
        is_write_doc_cluster_file = True
    else:
        is_write_doc_cluster_file = False
    if is_write_doc_cluster_file == False:
        corpus = plsaForNewsCluster.Corpus() # instantiate corpus
        # splitNewsTitleAndContent(doc_set_file)
        # sample news
        fp_doc_set = open(doc_set_file, 'r')
        for line in fp_doc_set:
            ele = line.split('\t')
            document = plsaForNewsCluster.Document("", ele[1])  #prepare words which has been segmented
            document.split()
            corpus.add_document(document)
        corpus.build_vocabulary()
        number_of_main_words = int(sys.argv[1])
        # corpus.extract_main_vocabulary(number_of_main_words)
        print "Main Vocabulary size:" + str(len(corpus.main_vocabulary))
        print "Number of documents:" + str(len(corpus.documents))
        number_of_topics = int(sys.argv[2])
        max_iterations = int(sys.argv[3])
        corpus.plsa(number_of_topics, max_iterations, number_of_main_words)
        news_cluster = computeNewsCluster(corpus, number_of_topics)
    else:
        news_cluster_file = 'data//doc_cluster.csv'
        news_cluster = getNewsClusterFromDisk(news_cluster_file)

    #generate news list which viewed time is nearly closed to the final viewed time
    nearly_news_for_final_time_by_specific_user_dict = getNearlyDayNews.generateNearlyNewsForFinalTimeBySpecificUserDict()

    K = 2  #recommend K news for every user
    computeUserItemScoreAndRecommend(user_set, doc_set, doc_map1, doc_click_count, user_doc_click_count, news_cluster, K, nearly_news_for_final_time_by_specific_user_dict)