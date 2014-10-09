# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-
import math

class UserBasedCF:
    def __init__(self,train_file,test_file):
        self.train_file = train_file
        self.test_file = test_file
        self.readData()
    def readData(self):
        #读取文件，并生成用户-物品的评分表和测试集
        self.train = dict()     #用户-物品的评分表
        for line in open(self.train_file):
            # user,item,score = line.strip().split(",")
            user,item,score,_ = line.strip().split("\t")
            self.train.setdefault(user,{})
            self.train[user][item] = int(score)
        self.test = dict()      #测试集
        for line in open(self.test_file):
            # user,item,score = line.strip().split(",")
            user,item,score,_ = line.strip().split("\t")
            self.test.setdefault(user,{})
            self.test[user][item] = int(score)
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
        for v,wuv in sorted(self.W[user].items(),key=lambda x:x[1],reverse=True)[0:K]:
            #遍历前K个与user最相关的用户
            for i,rvi in self.train[v].items():
                if i in action_item:
                    continue
                rank.setdefault(i,0)
                rank[i] += wuv * rvi
        return dict(sorted(rank.items(),key=lambda x:x[1],reverse=True)[0:N])   #推荐结果的取前N个

