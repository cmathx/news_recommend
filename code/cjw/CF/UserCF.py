# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-
import math
import Rate
import FinalView
from cjw.preprocess.UserViewTimeDistribute import *
from cjw.PLSA.plsaRecommend import *

class UserBasedCF:
    def __init__(self,train_file,test_file):
        self.train_file = train_file
        # self.test_file = test_file
        self.readData()
    def readData(self):
        #读取文件，并生成用户-物品的评分表和测试集
        self.train = dict()     #用户-物品的评分表
        for line in open(self.train_file):
            # user,item,score = line.strip().split(",")
            user,item,score_ = line.strip().split("\t")
            self.train.setdefault(user,{})
            self.train[user][item] = 1#int(score)
        # self.test = dict()      #测试集
        # for line in open(self.test_file):
        #     user,item,score = line.strip().split(",")
            # user,item,score,_ = line.strip().split("\t")
            # self.test.setdefault(user,{})
            # self.test[user][item] = int(score)
    def UserSimilarity(self):
        #建立物品-用户的倒排表
        self.item_users = dict()  #item_user[i]:购买过物品i的用户集合
        for user,items in self.train.items():
            for i in items.keys():
                if i not in self.item_users:
                    self.item_users[i] = set()
                self.item_users[i].add(user)
        #计算用户-用户相关性矩阵
        C = dict()  #用户-用户共现矩阵(C[i][j]:用户i和用户j浏览相同物品的数量)
        N = dict()  #用户产生行为的物品个数（N[i]:用户i所产生行为的物品个数）
        for i,users in self.item_users.items():
            for u in users:
                N.setdefault(u,0)
                N[u] += 1
                C.setdefault(u,{})
                for v in users:
                    if u == v:
                        continue
                    C[u].setdefault(v,0)
                    C[u][v] += 1
        #计算用户-用户相似度，余弦相似度
        self.W = dict()      #相似度矩阵(W[i][j]:用户i和用户j的相似度)
        for u,related_users in C.items():
            self.W.setdefault(u,{})
            for v,cuv in related_users.items():
                self.W[u][v] = cuv / math.sqrt(N[u] * N[v])
        return self.W
    #给用户user推荐，前K个相关用户
    def Recommend(self,user,K=3,N=10):
        rank = dict()
        action_item = self.train[user].keys()     #用户user产生过行为的item
        for v,wuv in self.W[user].items():#sorted(self.W[user].items(),key=lambda x:x[1],reverse=True)[0:K]:#self.W[user].items():
            #遍历前K个与user最相关的用户
            for i,rvi in self.train[v].items():
                if i in action_item:
                    continue
                rank.setdefault(i,0)
                rank[i] += wuv * rvi
        # return dict(sorted(rank.items(),key=lambda x:x[1],reverse=True))
        return dict(sorted(rank.items(),key=lambda x:x[1],reverse=True)[0:N])   #推荐结果的取前N个

    def filter(self, ori_rec_dict, user, nearly_news_for_final_time_by_specific_user_dict,N):
        fin_rec = dict()
        cnt = 0
        for news, score in ori_rec_dict.items():
            if cnt == N:
                break
            if news in nearly_news_for_final_time_by_specific_user_dict[user]:
                fin_rec[news] = score
                cnt += 1
        return fin_rec

    def printRecommendList(self,K=9999,N=2,user_set={}, nearly_news_for_final_time_by_specific_user_dict={},user_view_time={}):
        fp_recommend_set = open('../../recommend/usedBasedRecomemnd.csv', 'w')
        fp_recommend_set.write('userid,newsid\n')
        for user_id in user_set:
            if len(user_view_time[user_id]) > 3:
                recommend_news = self.Recommend(user_id, K, N)
            # print recommend_news
            # fin_recommend_news = self.filter(recommend_news, user_id, nearly_news_for_final_time_by_specific_user_dict, N)
            # print fin_recommend_news
                for recommend_news_id in recommend_news:
                    fp_recommend_set.write('%s,%s\n' %(user_id, recommend_news_id))


def ucfRecommend():
    print '建立doc映射表'
    doc_set_file = '../../data/document.csv'
    total_set_file = '../../data/total_set.txt'
    user_set, doc_set, user_map_r2v, user_map_v2r, doc_map1, doc_map2, user_click_count, doc_click_count, user_doc_click_count = \
    createDocMapAndClickInfo(total_set_file, doc_set_file)
    print '计算初始评分矩阵'
    Rate.getUserItemRate()
    userBasedCF = UserBasedCF('../../data/user_item_rate.csv', '')
    userBasedCF.UserSimilarity()
    print '生成最近的新闻列表'
    #generate news list which viewed time is nearly closed to the final viewed time
    nearly_news_for_final_time_by_specific_user_dict = {}#getNearlyDayNews.generateNearlyNewsForFinalTimeBySpecificUserDict()
    print '基于user based进行推荐'
    user_final_view_news1 = FinalView.getUserFinalDayViewNews()
    user_view_time = userViewTimeDistribute(user_final_view_news1)
    userBasedCF.printRecommendList(1000,1,user_set, nearly_news_for_final_time_by_specific_user_dict, user_view_time)

if __name__ == '__main__':
    ucfRecommend()