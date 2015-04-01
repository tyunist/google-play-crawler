# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Ty"
__date__ ="$Oct 4, 2013 5:39:20 PM$"

if __name__ == "__main__":
    print "Get app's details"

GOOGLE_LOGIN = GOOGLE_PASSWORD = AUTH_TOKEN = None

#from source.config import SEPARATOR
import sys
from pprint import pprint

from config import *
from googleplay import GooglePlayAPI
from helpers import sizeof_fmt
from helpers import print_details_line
from UnicodeWriter import*


#packageName = "com.WiredDFW.DIRECTV.unWiredRemoteLite" #Default value
packageName = "com.taleb.sexSounds"

if (len(sys.argv) == 1):
    print "You did not provide AppID. This parameter default is com.WiredDFW.DIRECTV.unWiredRemoteLite"

elif (len(sys.argv) == 2):
    packageName = sys.argv[1]
   
elif (len(sys.argv) >= 3):
    print "Wrong input, there may be a tab character!"
    sys.exit(0)


# Check request content   
print "packageName:",packageName


api = GooglePlayAPI(ANDROID_ID)
api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)

#for i in range(MAX_RESULTS/NB_RESULTS):
    
response = api.details(packageName)
#j = response.getResponse
c = response.docV2

CATEGORY = c.details.appDetails.appCategory
print "anh yeu em"
print c
            #print j.docid.encode('utf8')
            #write_result_line(j,saveFile)
print "Em khong yeu anh"
print_details_line(c)
l = [           
               
                c.docid, # unicode type
                c.title, # unicode type
                c.details.appDetails.appCategory, # class type
                c.details.appDetails.versionString,   #unicode type
                c.details.appDetails.uploadDate,
                
                c.creator, # unicode type
                c.details.appDetails.recentChangesHtml,  # unicode type
                c.descriptionHtml, # need to remove control characters
                c.offer[0].formattedAmount,
                            
#                c.details.appDetails.versionCode, # long type
                c.details.appDetails.numDownloads,  # unicode type
               
                c.details.appDetails.installationSize, # long type
                 "%.2f" % c.aggregateRating.starRating, # str type
               
                c.aggregateRating.ratingsCount, # long type
                c.aggregateRating.oneStarRatings, # long type
                c.aggregateRating.twoStarRatings, # long type
                c.aggregateRating.commentCount,  # long type
                c.details.appDetails.permission[0], #There are several permissions
                
              
                
                
                c.details.appDetails.appType,  # unicode type
               
                
               
               
                                                ]
                                                
#write to file
fileName = "%s.csv" %(packageName)
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
    


#wb.writerow(l)

    
#wb.writerow([SEPARATOR.join(i.decode('utf8') for i in l)])


#    except IndexError:
#        break
#    print "Getting %d to %d ..." %(i*20,(i+1)*20)
    
#print "See file %s.%s.csv to see results" %(packageName)





