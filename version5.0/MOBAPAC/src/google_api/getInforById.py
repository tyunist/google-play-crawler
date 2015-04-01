__author__="Ty"
__date__ ="$Oct 4, 2013 5:39:20 PM$"
if __name__ == "__main__":
    print "Get app's details"

GOOGLE_LOGIN = GOOGLE_PASSWORD = AUTH_TOKEN = None
from __init__ import *
import time, requests, sys
from googleplay import GooglePlayAPI


class ConnectionError(Exception):
    def __init__(self, value):
         self.value = value
    def __str__(self):
        return repr(self.value)

def get_infor_dict(app_id,api):
    print "Nextline:", app_id
    try:
        response = api.toDict(api.details(app_id).docV2) #Result is a list of infor dict 
    except requests.exceptions.ConnectionError as e:
        print e, "Current app_id is %s "%app_id
        raise ConnectionError("Connection Error while searching app information")
    else:
        return response

app_id = "com.doraemon.doraemonRepairShop"
try:
    api = GooglePlayAPI(ANDROID_ID)
    api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)
      
except requests.exceptions.ConnectionError as e:
    print "Connection error:", e
    raise
try:
    t = get_infor_dict(app_id,api) 
except ConnectionError as e:
    print e
    print "f"
    sys.exit(1)
else:
    print t
if t is None:
    print "NOne"
else:
    print t
if any(t):
    print "f"
else:
    print "ping"

# app_id = "com.eztakes.TheRedSkeltonCollectionDisc2_0170764"
# api = GooglePlayAPI(ANDROID_ID)
# api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)
# get_infor_dict(app_id, api)
#for i in range(MAX_RESULTS/NB_RESULTS):
    
# response = api.details(app_id)
# #j = response.getResponse
# c = response.docV2
# 
# CATEGORY = c.details.appDetails.appCategory
# print "anh yeu em"
# print c
#             #print j.docid.encode('utf8')
#             #write_result_line(j,saveFile)
# print "Em khong yeu anh"
# print_details_line(c)
# l = [           
#                
#                 c.docid, # unicode type
#                 c.title, # unicode type
#                 c.details.appDetails.appCategory, # class type
#                 c.details.appDetails.versionString,   #unicode type
#                 c.details.appDetails.uploadDate,
#                 
#                 c.creator, # unicode type
#                 c.details.appDetails.recentChangesHtml,  # unicode type
#                 c.descriptionHtml, # need to remove control characters
#                 c.offer[0].formattedAmount,
#                             
# #                c.details.appDetails.versionCode, # long type
#                 c.details.appDetails.numDownloads,  # unicode type
#                
#                 c.details.appDetails.installationSize, # long type
#                  "%.2f" % c.aggregateRating.starRating, # str type
#                
#                 c.aggregateRating.ratingsCount, # long type
#                 c.aggregateRating.oneStarRatings, # long type
#                 c.aggregateRating.twoStarRatings, # long type
#                 c.aggregateRating.commentCount,  # long type
#                 c.details.appDetails.permission[0], #There are several permissions
#                 
#               
#                 
#                 
#                 c.details.appDetails.appType,  # unicode type
#                
#                 
#              ]





