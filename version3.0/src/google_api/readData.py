# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Ty"
__date__ ="$Oct 18, 2013 8:59:07 PM$"

if __name__ == "__main__":
    print "Hello World"

GOOGLE_LOGIN = GOOGLE_PASSWORD = AUTH_TOKEN = None

#from source.__init__ import SEPARATOR
import sys
from pprint import pprint
import re
from __init__ import *
from googleplay import GooglePlayAPI
from androidmarket import*
from array import*
from UnicodeWriter import*
from getReviews import*
import os
import datetime



LastLine = 0
f=open("1.csv","a+b")
rb = UnicodeReader(f)
try:
    while True:
        LastLine = rb.next()
        if LastLine  == []:
            print "anh yeu em"
        else:
            print type(LastLine[1])
            print LastLine[1]
except StopIteration:
    pass
f.close()

    