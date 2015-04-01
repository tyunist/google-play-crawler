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
#            print "Component 5 is:",rb.next()[5]
            line = rb.next()
            IdTemp = line[5].decode("utf-8")
            TimeTemp = long(line[1].rsplit(".")[0])
            print TimeTemp
            if all([id == IdTemp, time == TimeTemp]):
#                    raise hasInFileError('This review existed already!')
                return True
    except StopIteration:
        pass
    return False
    
commentId = "lg:AOqpTOFO_Sc3eDB81_4OVdmzCKoqTTQdTtmhicXOL2CPPX-2X0JKyKFXm_67G7eNnUqxKHiECFP5Cznq-0y5gvU".decode("utf-8")
print type(commentId)
print commentId
timestampMsec = long(1372732245771)
fileName = "3.com.imdb.mobile.csv"
openfile = open(fileName,"rb")
previousFileName = "previous.com.imdb.mobile.csv" 
openPreviousFileName = open(previousFileName,"rb")
if hasInFile(openfile,commentId, timestampMsec) and hasInFile(openPreviousFileName,commentId,timestampMsec)==True:
    print "Exist"
else:
    print "No exist"

    
    