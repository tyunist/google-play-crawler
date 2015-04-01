'''
@attention: This module returns list of comment_dict for each app_id
'''
__author__="Ty"
__date__ ="$Oct 3, 2013 11:10:57 AM$"

if __name__ == "__main__":
    print "Search reviews for an App"

#from source.config import SEPARATOR
from config import *
from googleplay import GooglePlayAPI
import urllib2
import time

def get_comment_dict(app_id,api):
    #Initial a list of comment dict ( comment  represented in dict type)
    comment_list_of_dict = []
    print "Nextline:", app_id
    filterByDevice=False
    #Search comment for each id with different type of order
    for sort in range(4):
        print "Sort type is :", sort
        for m in range(MAX_RESULTS/NB_RES): 
            print "m:",m
            try:
                response = api.toDict(api.reviews(app_id, filterByDevice, sort, "20",str(m*20)))['getResponse']['review'] #Result is a list of comment dict 
                #Response is a comment dict. We need to check whether each comment dict existed already in comment_list_of_dict
                for comment_dict in response:
                    if comment_dict in comment_list_of_dict:
                        continue
                    else:
                        comment_list_of_dict += [comment_dict]
            except:
                print "App_id is wrong or end of results! m = ",m
                break 
    print "Number of app for %s: %d"%(app_id, len(comment_list_of_dict))
    return comment_list_of_dict            



#0: time
#1: star
#2: latest version
#3: 





