# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-
import math
import Rate
import FinalView
import UserViewNewsRank
from cjw.preprocess.UserViewTimeDistribute import *
# from cjw.AlreadyPublishNews import *
from cjw.PLSA.plsaRecommend import *
# from cjw.preprocess.UserViewTimeDistribute import *

INTERVAL = 10

class ItemBasedCF:
    def __init__(self,train_file):
        self.recommend_members = 0
        self.train_file = train_file
        # self.test_file = test_file
        self.readData()
    def readData(self):
        #读取文件，并生成用户-物品的评分表和测试集
        self.train = dict()     #用户-物品的评分表
        for line in open(self.train_file):
            # user,item,score = line.strip().split(",")
            user, item, score = line.strip().split("\t")
            self.train.setdefault(user, {})
            self.train[user][item] = 1.0#float(score)
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
        for user,items in self.train.items():
            for i in items.keys():
                N.setdefault(i,0)
                N[i] += 1
                C.setdefault(i,{})
                for j in items.keys():
                    if i == j: continue
                    C[i].setdefault(j,0)
                    C[i][j] += 1
        #计算相似度矩阵
        self.W = dict()
        for i,related_items in C.items():
            self.W.setdefault(i,{})
            for j,cij in related_items.items():
                self.W[i][j] = cij / math.sqrt((N[i] * N[j]))#(N[i] + N[j] - cij)
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
    def Recommend(self,user,K=3,N=1,user_final_view_news={}, user_final_view_news1={},userViewNewsRank={},user_view_time={}):
        rank = dict()
        # print len(user_final_view_news[user])
        # if len(user_final_view_news[user]) = 1:
        #     self.recommend_members += 1
        #     return 0, dict()

        if len(user_view_time[user]) <= 3:
            print '以用户最后一条浏览的新闻为基准进行推荐'
            action_item = user_final_view_news[user]     #用户user产生过行为的item和评分
            item = action_item
            score = self.train[user][item]
            for j,wj in dict(sorted(self.W[item].items(),key=lambda x:x[1],reverse=True)[0:K]).items():
                if j in self.train[user].keys():
                    continue
                rank.setdefault(j,0)
                rank[j] += score * wj
        # else:
        #     print '考虑用户浏览的所有新闻'
        #     action_item = user_final_view_news1[user]     #用户user产生过行为的item和评分
        #     print '以用户最后一天浏览的新闻为基准进行推荐'
        #     for item in action_item:
        #         score = self.train[user][item]
        #         for j,wj in self.W[item].items():#sorted(self.W[item].items(),key=lambda x:x[1],reverse=True)[0:K]:
        #             if j in self.train[user].keys():
        #                 continue
        #             rank.setdefault(j,0)
        #             rank[j] += score * wj
        '''
        action_item = self.train[user]     #用户user产生过行为的item和评分
            for item in action_item:
                # contribute_coeff = userViewNewsRank[user][item][1]
                score = self.train[user][item]
                for j,wj in self.W[item].items():#sorted(self.W[item].items(),key=lambda x:x[1],reverse=True)[0:K]:
                    if j in self.train[user].keys():
                        continue
                # print user, j, userViewNewsRank[user], userViewNewsRank[user][j]
                    rank.setdefault(j,0)
                    rank[j] += score * wj
                    # if contribute_coeff < 5:
                    #     rank[j] += score * wj / math.pow(100, contribute_coeff)
                '''
        return len(rank), dict(sorted(rank.items(),key=lambda x:x[1],reverse=True)[0:N])

    def filter(self, ori_rec_dict, user, user_may_read_news, N, doc_publish_time, user_view_time):
        fin_rec = dict()
        cnt = 0
        need_filter = False
        if len(user_view_time[user]) <= 1:
            need_filter = True
        if need_filter == False:
            for news, score in ori_rec_dict.items():
                if cnt == N:
                    break
                fin_rec[news] = score
                cnt += 1
        else:
            for news, score in ori_rec_dict.items():
                if cnt == N:
                    break
                news_publish_time = doc_publish_time[news]
                if timeInterval(user_view_time[user][0][0], news_publish_time) <= INTERVAL:
                    fin_rec[news] = score
                    cnt += 1
        return fin_rec

    def printRecommendList(self,K=9999,N=2,user_set={}, user_click_count={}, doc_publish_time={}, user_view_time={}, \
                           user_final_view_news={},user_final_view_news1={},userViewNewsRank={}):
        fp_recommend_set = open('../../recommend/itemBasedRecomemnd.csv', 'w')
        fp_recommend_set.write('userid,newsid\n')
        can_recommend_num = 0
        for user_id in user_set:
            # if len(user_view_time[user_id]) > 3:
            #     continue
            inc, recommend_news = self.Recommend(user_id, K, N, user_final_view_news, user_final_view_news1, userViewNewsRank, user_view_time)
            can_recommend_num += inc
            # print recommend_news
            # fin_recommend_news = self.filter(recommend_news, user_id, user_may_read_news, N, doc_publish_time, user_view_time)
            # print fin_recommend_news
            for recommend_news_id in recommend_news:
                fp_recommend_set.write('%s,%s\n' %(user_id, recommend_news_id))
        print can_recommend_num
        print 'total recommend members:', self.recommend_members

def icfRecommend():
    print '建立doc映射表'
    doc_set_file = '../../data/document.csv'
    total_set_file = '../../data/total_set.txt'
    user_set, doc_set, user_map_r2v, user_map_v2r, doc_map1, doc_map2, user_click_count, doc_click_count, user_doc_click_count = \
    createDocMapAndClickInfo(total_set_file, doc_set_file)
    doc_publish_time = {}
    print '计算初始评分矩阵'
    Rate.getUserItemRate()
    itemBasedCF = ItemBasedCF('../../data/user_item_rate.csv')
    itemBasedCF.ItemSimilarity()
    print '生成最近的新闻列表'
    #generate news list which viewed time is nearly closed to the final viewed time
    # nearly_news_for_final_time_by_specific_user_dict = getNearlyDayNews.generateNearlyNewsForFinalTimeBySpecificUserDict()
    print '计算用户最后一条浏览的新闻'
    user_final_view_news = FinalView.getUserFinalViewNews()

    print '计算用户最后一天浏览的新闻列表'
    user_final_view_news1 = FinalView.getUserFinalDayViewNews()

    print '基于item based进行推荐'
    # user_may_read_news = {}#getAlreadyPublishNews()
    print '过滤新闻列表计算结束'
    userViewNewsRank = UserViewNewsRank.userViewNewsRank()
    user_view_time = userViewTimeDistribute(user_final_view_news1)
    itemBasedCF.printRecommendList(6183,1,user_set, user_click_count, doc_publish_time, user_view_time, \
                                   user_final_view_news, user_final_view_news1, userViewNewsRank)
    # user_final_view_news_num = dict()
    # for user in user_final_view_news:
    #     user_final_view_news_num.setdefault(user, len(user_final_view_news[user]))
    # fp_final_view = open('../../data/final_view_info.csv', 'w')
    # user_final_view_news_num = sorted(user_final_view_news_num.items(), key=lambda d:d[1], reverse=True)
    # for tup in user_final_view_news_num:
    #     fp_final_view.write('%s\t%s\t|:' %(tup[0], tup[1]))
    #     # for user, view_news in user_final_view_news.items():
    #     #     fp_final_view.write('[%s]\t' %view_news)
    #     fp_final_view.write('\n')
    # fp_final_view.close()

    # fp_already_read = open('../../recommend/already_read.csv', 'w')
    # fp_already_read.write('userid,newsid\n')
    # for user, news_dict in user_final_view_news1.items():
    #     for news in news_dict:
    #         fp_already_read.write('%s,%s\n' %(user, news))
    # fp_already_read.close()

if __name__ == '__main__':
    icfRecommend()