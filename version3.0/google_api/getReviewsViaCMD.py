# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Ty"
__date__ ="$Oct 3, 2013 11:10:57 AM$"

if __name__ == "__main__":
    print "Search reviews for an App"
GOOGLE_LOGIN = GOOGLE_PASSWORD = AUTH_TOKEN = None

#from source.__init__ import SEPARATOR
import sys
from pprint import pprint

from __init__ import *
from googleplay import GooglePlayAPI
from helpers import sizeof_fmt
from androidmarket import*
from array import*
from UnicodeWriter import*


#class hasInFileError(Exception):
#    def __init__(self, value):
#        self.value = value
#    def __str__(self):
#        return repr(self.value)
    

def hasInFile(file,id, time):
    """Check whether (id, time) exists in file"""
    rb = UnicodeReader(file)
    try:
        while(1):
            line = rb.next()
            IdTemp = line[5].decode("utf-8")
            TimeTemp = long(line[1].rsplit(".")[0])
            if all([id == IdTemp, time == TimeTemp]):
#                    raise hasInFileError('This review existed already!')
                return True
    except StopIteration:
        pass
    return False
NB_RES = 20;
MAX_RESULTS = 500;
#packageName = "com.WiredDFW.DIRECTV.unWiredRemoteLite" #Default value
#packageName = "com.happybug.livewallpaper.jellyfishlite"
packageName = "com.disney.wheresmywater2_goo"
filterByDevice=False
sort=0


if (len(sys.argv) == 1):
    print "You did not provide AppID. This parameter default is com.WiredDFW.DIRECTV.unWiredRemoteLite"

elif (len(sys.argv) == 2):
    packageName = sys.argv[1]

elif (len(sys.argv) >= 3):
    print "Wrong input, there may be a tab character!"
    sys.exit(0)



# Check request content   
print "packageName:",packageName
print "Number of request:", NB_RES



api = GooglePlayAPI(ANDROID_ID)
api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)
ID = "AOqpTOEjTOe3SLM39KkxcHYWJ_HZ5f9pdv7pstjBjn3rwRF_0LpZrIED-Ok31aoQnlnuW8qdmwsLZeKxufpupgQ"

#response = api.reviewById(packageName, filterByDevice, ID)
#print response
#packageName = "com.WiredDFW.DIRECTV.unWiredRemoteLite" #Default value
#packageName = "com.happybug.livewallpaper.jellyfishlite"
print "Nextline:", packageName
filterByDevice=False
sort=0


api = GooglePlayAPI(ANDROID_ID)
api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)

#response = api.reviewById(packageName, filterByDevice, ID)
#print response
for s in range(4):
    sort = s
    for m in range(MAX_RESULTS/NB_RES):
        response = api.reviews(packageName, filterByDevice, sort, str(NB_RES),str(m*NB_RES))
#        print response
        for n in range(NB_RES):
            try:
                c = response.getResponse.review[n]
                l = [  

                           c.documentVersion,
                           
                           c.timestampMsec,

                           c.starRating,
                           c.title,
                           c.comment,
                           c.commentId,

                           c.deviceName,
#                               c.replyText,
#                               c.replyTimestampMsec, 
                           ]

                #Check whether comment exists
                fileName = "%d.%s.csv" %(s,packageName)
                openfile = open(fileName,"a+")

                previousFileName = "previous.%s.csv" %packageName 
                openPreviousFile = open(previousFileName,"a+")

                if hasInFile(openfile,c.commentId, c.timestampMsec) or hasInFile(openPreviousFile,c.commentId,c.timestampMsec):
                    openfile.close()
                    openPreviousFile.close()
                    continue
                else:
                    print "There is new review of s = %d m = %d n = %d" %(s,m,n)
                    saveFile = open(fileName, "a+b")
                    savePreviousFile = open(previousFileName, "a+b")
                    wpb = UnicodeWriter(savePreviousFile)
                    wb = UnicodeWriter(saveFile)
                    k = []

                    for i in range(len(l)):
                        if isinstance(l[i], basestring):
                            if isinstance(l[i],unicode):
                                l[i] = l[i].encode("utf-8")
                                l[i] = removeSpecialKey(l[i])
    #                            print i
    #                            print type(l[i])
    #                            print l[i]
                        k = k  + [l[i]]            
                    wb.writerow(k)
                    wpb.writerow(k)
                    saveFile.close()
                    savePreviousFile.close()
            except IndexError:
                print IndexError
                break
        print "Getting %d to %d ..." %(m*20,(m+1)*20)

#0: time
#1: star
#2: latest version
#3: 





