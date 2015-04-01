__author__="Ty"
__date__ ="$Oct 4, 2013 5:39:20 PM$"
if __name__ == "__main__":
    print "Get app's details"

GOOGLE_LOGIN = GOOGLE_PASSWORD = AUTH_TOKEN = None
from __init__ import *
import time
from googleplay import GooglePlayAPI

def get_infor_dict(app_id,api):
    print "Nextline:", app_id
    try:
        response = api.toDict(api.details(app_id).docV2) #Result is a list of infor dict 
        print "response:", response
    except:
        print "%s is a wrong app_id or connection fail! ", app_id
        raise
    return response         

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





