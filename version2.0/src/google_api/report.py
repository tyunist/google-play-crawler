# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Ty"
__date__ ="$Oct 18, 2013 12:51:54 AM$"

if __name__ == "__main__":
    print "Main Function"
GOOGLE_LOGIN = GOOGLE_PASSWORD = AUTH_TOKEN = None

#from source.config import SEPARATOR
import sys
from pprint import pprint
import re
from config import *
from googleplay import GooglePlayAPI
from androidmarket import*
from array import*
from UnicodeWriter import*
from getReviews import*
import os
import datetime
def ModificationDate(fileName):
    f = open(fileName, "a+")
    t = os.path.getmtime(fileName)

    f.close()
    return datetime.datetime.fromtimestamp(t)

def countLines(fileName):
    return sum(1 for line in open(fileName,"a+"))

def readOldData(fileName):
    LastLine = []
    f=open(fileName,"a+b")
    rb = UnicodeReader(f)
    try:
        while True:
            LastLine = rb.next()
    except StopIteration:
        pass
    f.close()
    return LastLine
    

#Report

with open("AppList.csv", "rb") as f:
    for line in f:
        packageName = re.sub('[^A-Za-z0-9.]+', '', line)
        OldData  = readOldData("report.%s.csv"%packageName)
        print "type of Olddata:", type(OldData)
        print "OldData:",OldData
        
        #Fetch new data:
        Lines0 = countLines("0.%s.csv"%packageName)
        Lines1 = countLines("1.%s.csv"%packageName)
        Lines2 = countLines("2.%s.csv"%packageName)
        Lines3 = countLines("3.%s.csv"%packageName)
        TotalLines = Lines0 + Lines1 + Lines2 + Lines3
        #Write new data to separate report files for each appId
        report = open("report.%s.csv"%packageName,"a+b")
        rb = UnicodeWriter(report)
        l = [
            ModificationDate("previous.%s.csv"%packageName),
            packageName,
            TotalLines,
            Lines0,
            Lines1,
            Lines2,
            Lines3,
        ]
        
        rb.writerow(l)
        report.close()
        print "type of time:",type(ModificationDate("previous.%s.csv"%packageName))
        
        #Write new data to exaggrated report file
        ExReport = open("report.csv","a+b")
        rpb = UnicodeWriter(ExReport)
#        rpb.writerow(["AppID               ", "Modification Date", "TotalReviews","NewReviews",
#            "ReviewsOfOrder0", "NewReviews of Order0",
#            "ReviewsOfOrder1", "NewReviewsOfOrder1",
#            "ReviewsOfOrder2", "NewReviewsOfOrder2",
#            "ReviewsOfOrder3", "NewReviewsOfOrder3"])
        if OldData == []:
            l = [
                packageName,
                ModificationDate("report.%s.csv"%packageName),
                TotalLines,
                0,
                Lines0,
                0,
                Lines1,
                0,
                Lines2,
                0,
                Lines3,
                0,
                            ]
        else:
            l = [
                packageName,
                ModificationDate("report.%s.csv"%packageName),
                TotalLines,
                TotalLines - int(OldData[2]),
                Lines0,
                Lines0 - int(OldData[3]),
                Lines1,
                Lines1 - int(OldData[4]),
                Lines2,
                Lines2 - int(OldData[5]),
                Lines3,
                Lines3 - int(OldData[6]),
                                ]
        rpb.writerow(l)
        ExReport.close()
ExReport = open("report.csv","a+b")
rpb = UnicodeWriter(ExReport)
rpb.writerow(["**************End of %s******************"%ModificationDate("report.csv")])
    
        

        