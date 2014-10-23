# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-
import math
import Rate
# from cjw.AlreadyPublishNews import *
from cjw.PLSA.plsaRecommend import *
from cjw.preprocess.UserViewTimeDistribute import *

LEFT_INTERVAL = 10
RIGHT_INTERVAL = 0


class ItemBasedCF:
<<<<<<< HEAD
    def __init__(self, train_file, test_file):
=======
    def __init__(self,train_file):
>>>>>>> dacec8f2e378b773a87c73d9a4df98e2922c84a4
        self.train_file = train_file
        # self.test_file = test_file
        self.readData()

    def readData(self):
        #读取文件，并生成用户-物品的评分表和测试集
        self.train = dict()  #用户-物品的评分表
        for line in open(self.train_file):
            # user,item,score = line.strip().split(",")
            user, item, score = line.strip().split("\t")
            self.train.setdefault(user, {})
            self.train[user][item] = float(score)
            # self.test = dict()      #测试集
            # for line in open(self.test_file):
            #     user, item, score = line.strip().split(",")
            # user,item,score,_ = line.strip().split("\t")
            # self.test.setdefault(user,{})
            # self.test[user][item] = int(score)

    def ItemSimilarity(self):
        #建立物品-物品的共现矩阵
        C = dict()  #物品-物品的共现矩阵
        N = dict()  #物品被多少个不同用户购买
        for user, items in self.train.items():
            for i in items.keys():
                N.setdefault(i, 0)
                N[i] += 1
                C.setdefault(i, {})
                for j in items.keys():
                    if i == j: continue
<<<<<<< HEAD
                    C[i].setdefault(j, 0)
                    C[i][j] += 1
        #计算相似度矩阵
        self.W = dict()
        for i, related_items in C.items():
            self.W.setdefault(i, {})
            for j, cij in related_items.items():
                self.W[i][j] = cij / (math.sqrt(N[i] * N[j]))  #(N[i] + N[j] - cij)
=======
                    C[i].setdefault(j,0)
                    C[i][j] += 1
        #计算相似度矩阵
        self.W = dict()
        for i,related_items in C.items():
            self.W.setdefault(i,{})
            for j,cij in related_items.items():
                self.W[i][j] = cij / (N[i] * N[j])#(N[i] + N[j] - cij)
>>>>>>> dacec8f2e378b773a87c73d9a4df98e2922c84a4
        return self.W

    #根据topic model计算结果读入文档的相似度
    def ItemSimilarityByTopicModel(self, sims_arr, v2r_doc_map):
        doc_size = len(sims_arr)
        self.W1 = dict()
        for i in xrange(doc_size):
            for j in xrange(doc_size):
                if self.W[v2r_doc_map[i]].has_key(v2r_doc_map[j]) == True:
                    self.W1.setdefault(v2r_doc_map[i], {})
                    self.W1[v2r_doc_map[i]][v2r_doc_map[j]] = sims_arr[i][j]
                    # return self.W

    def FinalItemSimilarity(self, v2r_doc_map):
        self.W_fin = dict()
        for uu, ii_sim in self.W.items():
            self.W_fin.setdefault(uu, {})
            for ii, sim in ii_sim.items():
                self.W_fin[uu].setdefault(ii, sim * self.W1[uu][ii])

    #给用户user推荐，前K个相关用户
    def Recommend(self, user, K=3, N=1):
        rank = dict()
<<<<<<< HEAD
        action_item = self.train[user]  #用户user产生过行为的item和评分
        for item, score in action_item.items():
            for j, wj in self.W[item].items():  #sorted(self.W[item].items(),key=lambda x:x[1],reverse=True):#[0:K]:
=======
        action_item = self.train[user]     #用户user产生过行为的item和评分
        for item,score in action_item.items():
            for j,wj in sorted(self.W[item].items(),key=lambda x:x[1],reverse=True)[0:K]:
>>>>>>> dacec8f2e378b773a87c73d9a4df98e2922c84a4
                if j in action_item.keys():
                    continue
                rank.setdefault(j, 0)
                rank[j] += score * wj
<<<<<<< HEAD
        # return dict(sorted(rank.items(),key=lambda x:x[1],reverse=True)[0:N])
        return rank
=======
        return len(rank), dict(sorted(rank.items(),key=lambda x:x[1],reverse=True)[0:N])
>>>>>>> dacec8f2e378b773a87c73d9a4df98e2922c84a4

    def filter(self, ori_rec_dict, user, user_may_read_news, N, doc_publish_time, user_view_time):
        ori_rec_dict = sorted(ori_rec_dict.items(), key=lambda x: x[1], reverse=True)
        fin_rec = dict()
        cnt = 0
        # need_filter = False
        # if len(user_view_time[user]) <= 1:
        #     need_filter = True
        # if need_filter == False:
        #     for tup in ori_rec_dict:
        #         if cnt == N:
        #             break
        #         fin_rec[tup[0]] = tup[1]
        #         cnt += 1
        # else:
        for tup in ori_rec_dict:
            if cnt == N:
                break
            news = tup[0]
            score = tup[1]
            news_publish_time = doc_publish_time[news]
            interval = timeInterval(user_view_time[user][0][0], news_publish_time)
            if interval <= LEFT_INTERVAL and interval >= 0:
                fin_rec[news] = score
                cnt += 1

        return fin_rec

<<<<<<< HEAD

def printRecommendList(self, K=9999, N=2, user_set={}, user_may_read_news={}, doc_publish_time={},
                       user_view_time={}):
    fp_recommend_set = open('../../recommend/itemBasedRecomemnd.csv', 'w')
    fp_recommend_set.write('userid,newsid\n')
    for user_id in user_set:
        recommend_news = self.Recommend(user_id, K, N)
        # print recommend_news
        fin_recommend_news = self.filter(recommend_news, user_id, user_may_read_news, N, doc_publish_time,
                                         user_view_time)
        # print fin_recommend_news
        for recommend_news_id in fin_recommend_news:
            fp_recommend_set.write('%s,%s\n' % (user_id, recommend_news_id))

=======
    def printRecommendList(self,K=9999,N=2,user_set={}, user_may_read_news={}, doc_publish_time={}, user_view_time={}):
        fp_recommend_set = open('../../recommend/itemBasedRecomemnd.csv', 'w')
        fp_recommend_set.write('userid,newsid\n')
        can_recommend_num = 0
        for user_id in user_set:
            inc, recommend_news = self.Recommend(user_id, K, N)
            can_recommend_num += inc
            # print recommend_news
            # fin_recommend_news = self.filter(recommend_news, user_id, user_may_read_news, N, doc_publish_time, user_view_time)
            # print fin_recommend_news
            for recommend_news_id in recommend_news:
                fp_recommend_set.write('%s,%s\n' %(user_id, recommend_news_id))
        print can_recommend_num
>>>>>>> dacec8f2e378b773a87c73d9a4df98e2922c84a4

def icfRecommend():
    print '建立doc映射表'
    doc_set_file = '../../data/document.csv'
    total_set_file = '../../data/total_set.txt'
    user_set, doc_set, doc_map1, doc_map2, doc_click_count, user_doc_click_count = \
<<<<<<< HEAD
        createDocMapAndClickInfo(total_set_file, doc_set_file)
    doc_publish_time, user_view_time = userViewTimeDistribute()
=======
    createDocMapAndClickInfo(total_set_file, doc_set_file)
    doc_publish_time = {}
    user_view_time = {}#userViewTimeDistribute()
>>>>>>> dacec8f2e378b773a87c73d9a4df98e2922c84a4
    print '计算初始评分矩阵'
    Rate.getUserItemRate()
    itemBasedCF = ItemBasedCF('../../data/user_item_rate.csv')
    itemBasedCF.ItemSimilarity()
    print '生成最近的新闻列表'
    #generate news list which viewed time is nearly closed to the final viewed time
    # nearly_news_for_final_time_by_specific_user_dict = getNearlyDayNews.generateNearlyNewsForFinalTimeBySpecificUserDict()
    print '基于item based进行推荐'
    user_may_read_news = {}  #getAlreadyPublishNews()
    print '过滤新闻列表计算结束'
    itemBasedCF.printRecommendList(6183, 1, user_set, user_may_read_news, doc_publish_time, user_view_time)


def diffRecommend():
    fp_recommend_set = open('../../recommend/itemBasedRecomemnd.csv', 'r')
    diff_doc = dict()
    tag = True
    cnt = 0
    for line in fp_recommend_set:
        if tag:
            tag = False
        else:
            line = line.split(',')
            if diff_doc.has_key(line[1]) == False:
                diff_doc.setdefault(line[1], 1)
                cnt += 1
    print cnt


if __name__ == '__main__':
    icfRecommend()
<<<<<<< HEAD
    # diffRecommend()
=======
>>>>>>> dacec8f2e378b773a87c73d9a4df98e2922c84a4
