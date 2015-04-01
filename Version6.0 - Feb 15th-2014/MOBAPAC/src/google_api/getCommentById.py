'''
@attention: This module returns list of comment_dict for each app_id
'''
__author__="Ty"
__date__ ="$Oct 3, 2013 11:10:57 AM$"

if __name__ == "__main__":
    print "Search reviews for an App"

#from source.__init__ import SEPARATOR
from __init__ import *
from googleplay import GooglePlayAPI
import time, sys
import requests

class ConnectionError(Exception):
    def __init__(self, value):
         self.value = value
    def __str__(self):
        return repr(self.value)

def get_comment_dict(app_id,api):
    #Initial a list of comment dict ( comment  represented in dict type)
    comment_list_of_dict = []
    print "googleplay.get_comment_dict    Nextline:", app_id
    filterByDevice=False
    #Search comment for each id with different type of order
    for sort in range(4):
        print "googleplay.get_comment_dict    Sort type is :", sort
        for m in range(MAX_RESULTS/NB_RES): 
            print "googleplay.get_comment_dict    m:",m
            try:
                response = api.toDict(api.reviews(app_id, filterByDevice, sort, "20",str(m*20)))['getResponse']['review'] #Result is a list of comment dict 
                #Response is a comment dict. We need to check whether each comment dict existed already in comment_list_of_dict
            except requests.exceptions.ConnectionError as e:
                raise ConnectionError("Connection Error while searching comments")
            except KeyError as e:
                    print "googleplay.get_comment_dict    No more comment! current m = ",m
                    break
            
            else:
                for comment_dict in response:
                    if comment_dict in comment_list_of_dict:
                        continue
                    else:
                        comment_list_of_dict += [comment_dict]
                
        #In order to speed up searching, just stop other ordering searching if number of comments after the first ordering searching is < 500
        if len(comment_list_of_dict)< 500:
            break
    print "Number of comments for %s: %d"%(app_id, len(comment_list_of_dict))
    return comment_list_of_dict      
#     except requests.exceptions.ConnectionError as e:
#         return ["Connection Error"]
               
# 
# app_id = "com.gau.go.touchhelperex.theme.captainbot"
# try:
#     api = GooglePlayAPI(ANDROID_ID)
#     api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)
#       
# except requests.exceptions.ConnectionError as e:
#     print "Connection error:", e
#     raise
# try:
#     t = get_comment_dict(app_id,api) 
# except ConnectionError as e:
#     print e
#     print "f"
#     sys.exit(1)
# except KeyError as e:
#     print e
#     print "m"
# 
# else:
#     print len(t)
#     print "here"
#     for i in range(len(t)):
#         print "%d:"%i, t[i]

#0: time
#1: star
#2: latest version
#3: 





