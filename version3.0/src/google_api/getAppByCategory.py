'''
Created on Nov 7, 2013
@attention: This module aimed at searching apps in google store.
@author: tynguyen
'''

from __init__ import *
from googleplay import GooglePlayAPI
import urllib2
import time

def get_app_by_category(api, category, subcategory):
    app_list_by_category = []
    for s in range(MAX_RESULTS/NB_RES):
        print "s =", s
        time.sleep(0.1)
        response = api.list(category, subcategory, str(NB_RES),str(s*NB_RES))
        if response is not None:
            print "Get apps with s = %s"%s
        else:
            print "No apps with s = %s"%s 
        try:
            d = response.doc[0]
            for c in d.child:
                app_list_by_category.append(c.docid)
        except IndexError:
            break
    print "Getting %d to %d ..." %(s*20,(s+1)*20)
    
    return app_list_by_category

 
 
def get_app_by_keyword(api, keyword):
    app_list_by_category = []
    for s in range(MAX_RESULTS/NB_RES):
        print "s =", s
        time.sleep(0.1)
        response = api.search(keyword, str(NB_RES), str(s*NB_RES))
        if response is not None:
            print "Get apps with s = %s"%s
        else:
            print "No apps with s = %s"%s 
        try:
            d = response.doc[0]
            for c in d.child:
                app_list_by_category.append(c.docid)
        except IndexError:
            break
    print "Getting %d to %d ..." %(s*20,(s+1)*20)
     
    return app_list_by_category


 
















#===============================================================================
#The following program uses proxy! 
#===============================================================================
# def get_app_by_category(pip, category, subcategory):
#     app_list_by_category = []
#     try:
#         api = GooglePlayAPI(ANDROID_ID)
#         api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN,pip)
#         for s in range(MAX_RESULTS/NB_RES):
#             print "s =", s
# #             time.sleep(2)
#             response = api.list(category, subcategory, str(NB_RES),str(s*NB_RES),pip)
#             try:
#                 d = response.doc[0]
#                 for c in d.child:
#                     app_list_by_category += c.docid
# 
#             except IndexError:
#                 break
#         print "Getting %d to %d ..." %(s*20,(s+1)*20)
#         print "See file %s.%s.csv to see results" %(category, subcategory)
#     except urllib2.HTTPError:
#         print "Proxy %s is bad!" %pip
#     return app_list_by_category
