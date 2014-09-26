# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

import datetime
from datetime import *

TOTAL_SET_FILE = '../data/train_set.txt'#替换
TEST_SET_FILE = '../data/test_set1.txt'#替换


#SampleSet with movies
movies = {'Marcel Caraciolo': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
                               'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
                               'The Night Listener': 3.0},
          'Luciana Nunes': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
                            'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 3.5},
          'Leopoldo Pires': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
                             'Superman Returns': 3.5, 'The Night Listener': 4.0},
          'Lorena Abreu': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
                           'The Night Listener': 4.5, 'Superman Returns': 4.0,
                           'You, Me and Dupree': 2.5},
          'Steve Gates': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                          'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
                          'You, Me and Dupree': 2.0},
          'Sheldom': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                      'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
          'Penny Frewman': {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0, 'Superman Returns': 4.0}}


def loadDataset(path=""):
    """ To load the dataSet"
        Parameter: The folder where the data files are stored
        Return: the dictionary with the data
    """
    #Recover the titles of the books
    # books = {}
    # for line in open(path + "BX-Books.csv"):
    #     line = line.replace('"', "")
    #     (id, title) = line.split(";")[0:2]
    #     books[id] = title

    #Load the data
    prefs = {}
    count = 0
    lineNum = 0
    for line in open(path + "user-item-ratings.csv"):
    # for line in open(path + "BX-Book-Ratings.csv"):
    # for line in open(path + "testCF.csv"):
        lineNum += 1
        line = line.replace('"', "")
        line = line.replace("\\", "")
        (user, bookid, rating) = line.split(";")
        try:
            if float(rating) > 0.0:
                prefs.setdefault(user, {})
                # prefs[user][books[bookid]] = float(rating)
                prefs[user][bookid] = float(rating)
        except ValueError:
            count += 1
            # print "value error found! " + user + bookid + rating
        except KeyError:
            count += 1
            # print "key error found! " + user + " " + bookid
    # print 'the number of non-exist book:', count
    return prefs


from math import sqrt

#Returns a distance-base similarity score for person1 and person2
def sim_distance(prefs, person1, person2):
    #Get the list of shared_items
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    #if they have no rating in common, return 0
    if len(si) == 0:
        return 0

    #Add up the squares of all differences

    euler_dis_list = [pow(prefs[person1][item] - prefs[person2][item], 2) for item in prefs[person1] if item in prefs[person2]]
    sum_of_squares = sum(euler_dis_list)
    ret = len(euler_dis_list) / (1 + sqrt(sum_of_squares))
    if ret > 1.0:
        return 1.0
    if ret < -1.0:
        return -1.0
    return ret


#Returns the Pearson correlation coefficient for p1 and p2
def sim_pearson(prefs, p1, p2):
    #Get the list of mutually rated items
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1

    #if they are no rating in common, return 0
    if len(si) == 0:
        return 0

    #sum calculations
    n = len(si)

    #sum of all preferences
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    #Sum of the squares
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])

    #Sum of the products
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

    #Calculate r (Pearson score)
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0:
        return 0

    r = num / den

    return r


#Returns the best matches for person from the prefs dictionary
#Number of the results and similiraty function are optional params.
def topMatches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other)
              for other in prefs if other != person]
    scores.sort()
    scores.reverse()
    return scores[0:n]

import HotNews
NEARLY_DAYS = 5
def getNearlyNews(view_time):
    publish_time_news_dict = HotNews.newsInfoCount(TOTAL_SET_FILE)
    # fp_test_set = open('../data/test_set.txt', 'r')
    nearly_news_list = []
    view_year = int(view_time.split('/')[0])
    view_month = int(view_time.split('/')[1])
    view_day = int(view_time.split('/')[2])
    for i in xrange(NEARLY_DAYS):
        import datetime
        t_datetime = datetime.datetime(view_year, view_month, view_day) - datetime.timedelta(i)
        t_publish_time = '%04d/%02d/%02d' %(t_datetime.year, t_datetime.month, t_datetime.day)
        for t_news_id in publish_time_news_dict[t_publish_time]:
            s_news_id = '%s' %(t_news_id)
            nearly_news_list.append(s_news_id)
    return nearly_news_list

    # for line in fp_test_set:
    #     tup = line.split('\t')
    #     user_id = tup[0]

def getNearlyNewsForEveryDay():
    nearly_news_dict = {}
    for i in xrange(1, 32):
        cur_view_time = '2014/03/%02d' %i
        nearly_news_dict[cur_view_time] = getNearlyNews(cur_view_time)
    return nearly_news_dict

def getNearlyNewForFinalViewTime(nearly_news_dict):
    nearly_news_for_final_viewtime_dict = {}
    fp_test_set = open(TEST_SET_FILE, 'r')
    for line in fp_test_set:
        tup = line.split('\t')
        user_id = tup[0]
        final_view_time = tup[2].split('-')[0]
        nearly_news_for_final_viewtime_dict[user_id] = nearly_news_dict[final_view_time]
    return nearly_news_for_final_viewtime_dict

def generateNearlyNewsForFinalTimeBySpecificUserDict():
    #nearly_news_dict: (key,value)-(view_time, total nearly viewed news)
    nearly_news_dict = getNearlyNewsForEveryDay()
    #nearly_news_for_final_time_by_specific_user_dict: (key,value)-(user, total nearly viewed news )
    nearly_news_for_final_time_by_specific_user_dict = getNearlyNewForFinalViewTime(nearly_news_dict)
    print 'generate nearly_news_for_final_time_dict finished'
    return nearly_news_for_final_time_by_specific_user_dict


#Gets recommendations for a person by using a weighted average
#of every other user's rankings
def getRecommendations(nearly_news_for_final_time_by_specific_user_dict, prefs, person, similarity=sim_pearson):#
    totals = {}
    simSums = {}

    # for other in nearly_news_list:
    for other in prefs:
        #don't compare me to myself
        if other == person:
            continue
        sim = similarity(prefs, person, other)

        #ignore scores of zero or lower
        if sim <= 0:
            continue
        for item in prefs[other]:
            #only score books i haven't seen yet
            if item not in prefs[person] or prefs[person][item] == 0:
                #Similarity * score
                #only consider the viewed time which is close to the final viewed for the specific user
                # if item in nearly_news_for_final_time_by_specific_user_dict[person]:
                totals.setdefault(item, 0) #setdefault:if dict hasn't this item set value = 0 else keep previous value
                totals[item] += prefs[other][item] * sim
                #Sum of similarities
                simSums.setdefault(item, 0)
                simSums[item] += sim

    #Create the normalized list
    rankings = [(total / simSums[item], item) for item, total in totals.items()]

    #Return the sorted list
    rankings.sort()
    rankings.reverse()

    #remove items which publishes after the final view time for this user
    #####

    ####

    return rankings


#Function to transform Person, item - > Item, person
def transformPrefs(prefs):
    results = {}
    for person in prefs:
        for item in prefs[person]:
            results.setdefault(item, {})

            #Flip item and person
            results[item][person] = prefs[person][item]
    return results


#Create a dictionary of items showing which other items they are most similar to.
def calculateSimilarItems(prefs, n=10):
    result = {}
    #Invert the preference matrix to be item-centric
    itemPrefs = transformPrefs(prefs)
    c = 0
    for item in itemPrefs:
        #Status updates for large datasets
        c += 1
        if c % 100 == 0:
            print "%d / %d" % (c, len(itemPrefs))
        #Find the most similar items to this one
        scores = topMatches(itemPrefs, item, n=n, similarity=sim_distance)
        result[item] = scores
    return result


def getRecommendedItems(prefs, itemMatch, user):
    userRatings = prefs[user]
    scores = {}
    totalSim = {}

    #loop over items rated by this user
    for (item, rating) in userRatings.items():

        #Loop over items similar to this one
        for (similarity, item2) in itemMatch[item]:

            #Ignore if this user has already rated this item
            if item2 in userRatings:
                continue
            #Weighted sum of rating times similarity
            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating
            #Sum of all the similarities
            totalSim.setdefault(item2, 0)
            totalSim[item2] += similarity

    #Divide each total score by total weighting to get an average
    rankings = [(score / totalSim[item], item) for item, score in scores.items()]

    #Return the rankings from highest to lowest
    rankings.sort()
    rankings.reverse()
    return rankings

RECOMMEND_NUM = 3
def printRecommendNews(critics, recommend_file):
    fp_recommend = open(recommend_file, 'w')
    fp_recommend.write('userid,newsid\n')
    user_id_list = []
    fp_test_set = open(TEST_SET_FILE, 'r')
    for line in fp_test_set:
        user_id = line.split('\t')[0]
        user_id_list.append(user_id)
    #generate news list which viewed time is nearly closed to the final viewed time
    nearly_news_for_final_time_by_specific_user_dict = generateNearlyNewsForFinalTimeBySpecificUserDict()
    for user_id in user_id_list:
        s_user_id = '%s' %user_id
        #recommend news for specific user
        t_recommend_list = getRecommendations(nearly_news_for_final_time_by_specific_user_dict, critics, s_user_id)[0:RECOMMEND_NUM]
        real_recommend_num = len(t_recommend_list)
        for i in xrange(real_recommend_num):
            fp_recommend.write('%s,%s\n' %(user_id, t_recommend_list[i][1]))


if __name__ == '__main__':
    from datetime import *
    time1 = datetime.now()
    print 'start time: ', time1
    critics = loadDataset('../data/')#news recommend version
    # critics = loadDataset('../R/')#testCF version
    # critics = loadDataset('../data/BX-CSV-Dump/')#book rating version
    # print critics
    # print sim_distance(critics,'98556', '180727')
    # print topMatches(critics,'98556',10,sim_distance)
    # print getRecommendations(critics,'180727')[0:3]
    # print sim_distance(critics,'8258428', '999572')
    # print topMatches(critics,'8258428',10,sim_pearson)
    printRecommendNews(critics, '../recommend/UCFRecommend.csv')
    time2 = datetime.now()
    print 'end time: ', time2
    print time2 - time1
    # print getRecommendations(critics,'8258428')[0:3]
    # for i in xrange(1, 6):
    #     for j in xrange(1, 6):
    #         ii = '%s' %i
    #         jj = '%s' %j
    #         print sim_distance(critics, ii, jj)
    # print sim_distance(critics,'1', '3')
    # for i in xrange(1, 6):
    #     ii = '%s' %i
    #     print topMatches(critics,ii,2,sim_distance)
    # for i in xrange(1, 6):
    #     ii = '%s' %i
    #     print getRecommendations(critics,ii)[0:2]
#