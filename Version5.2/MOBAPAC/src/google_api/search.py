#!/usr/bin/python

# Do not remove
GOOGLE_LOGIN = GOOGLE_PASSWORD = AUTH_TOKEN = None

import sys

from __init__ import *
from googleplay import GooglePlayAPI
from UnicodeWriter import*
request = "gun"
NB_RES = 20
OFFSET = 500
if __name__ == "__main__":
    print "Search for an app by keyword."
    
if (len(sys.argv) < 2):
    print "Search by defaut"
#    sys.exit(0)
if (len(sys.argv) == 2):
    print "NB_RES & OFFSET are set by default"
    request = sys.argv[1]
#    sys.exit(0)



if (len(sys.argv) >= 3):
     NB_RES = int(sys.argv[2])

if (len(sys.argv) >= 4):
     OFFSET = int(sys.argv[3])
    
# Check request content   
print "Request:", request
print "Number of request:", NB_RES
print "Offset:", OFFSET


api = GooglePlayAPI(ANDROID_ID)
api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)
print "NB_RES/OFFSET:",NB_RES/OFFSET
for i in range (50):
    message = api.search(request, str(NB_RES), str(i*NB_RES))
    doc = message.doc[0]
    for c in doc.child:
        print c
        l = [           
                # unicode type
                c.docid,
                c.title,
                c.creator,
                c.descriptionHtml, # need to remove control characters
                c.offer[0].formattedAmount,
                            
                c.details.appDetails.versionCode, # long type
                c.details.appDetails.versionString,   #unicode type
                c.details.appDetails.appCategory, # class type
                c.details.appDetails.installationSize, # long type
#                c.details.appDetails.permission[0], #There are several permissions
                
                # unicode type
                c.details.appDetails.numDownloads,
                c.details.appDetails.recentChangesHtml,
                c.details.appDetails.appType,
                c.details.appDetails.uploadDate,
                
               
                "%.2f" % c.aggregateRating.starRating, # str type
                # long type
                c.aggregateRating.ratingsCount,
                c.aggregateRating.oneStarRatings,
                c.aggregateRating.twoStarRatings,
                c.aggregateRating.commentCount, 
                                                ]
                                                
        #write to file
#        fileName = "%s.csv" %(request)
        fileName = "gun.csv"
        saveFile = open(fileName, "a+b")
        wb = UnicodeWriter(saveFile)
        k = []
        for i in range(len(l)):
            if isinstance(l[i], basestring):
                if isinstance(l[i],unicode):
                    l[i] = l[i].encode("utf-8")
                    l[i] = removeSpecialKey(l[i])
                    print i
                    print type(l[i])
                    print l[i]
            k = k  + [l[i]]            
        wb.writerow(k)

