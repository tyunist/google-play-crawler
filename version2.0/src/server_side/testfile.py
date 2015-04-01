'''
Created on Nov 9, 2013

@author: tynguyen
'''
import datetime
import time
from sqlalchemy import *
# from mysql import *

def input_categories(filename):
    return [line for line in open(filename,"ra")]

CategoryList = input_categories("categories.txt")
try: 
    for i in range(len(CategoryList)):
        print "phan tu thu i:", CategoryList[i]
        categories = (CategoryList[i].split(":")[0],CategoryList[i].split(":")[1])
        
        print categories               
    # Success, commit everything
except:
    # Make sure the transaction is rolled back ...
    print "Fail to read file"

# print str(datetime.datetime.now()).split(" ")[0]
m = datetime.datetime.now()
k = datetime.date
print m
