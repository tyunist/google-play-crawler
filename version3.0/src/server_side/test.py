'''
Created on Nov 12, 2013

@author: tynguyen
'''
GOOGLE_LOGIN = GOOGLE_PASSWORD = AUTH_TOKEN = None
from requests.exceptions import SSLError
from google_api.getCommentById import get_comment_dict
from google_api.googleplay import GooglePlayAPI
from google_api.__init__ import *
from create_tables import *
from sqlalchemy import *
from sqlalchemy.orm import *
import datetime, time
# 
#            
#Connect to the Database
engine = create_engine('mysql://root:mobapac2013@localhost/MOBAPAC')
engine.echo = False  # Try changing this to True
Session = sessionmaker(autoflush=False)
Session.configure(bind=engine)
session = Session()
  
# testId = session.query(Id.app_index).filter(Id.app_index<2).scalar()
# print testId
# print "type:", type(testId)
# 
# testId = session.query(Id.app_id).filter(Id.app_index<2).scalar()
# print testId
# print "type:", type(testId)
# 
# 
# testId = session.query(Id.created_at).filter(Id.app_index<2).scalar()
# print testId
# print "type:", type(testId)
# # 
testId = session.query(func.count(Comments.app_index)).filter(Comments.app_index==100).scalar()
# testId = 100
# .filter(Comments.id == 13343)
print "testId =", testId
print "type:", type(testId)
# session.add(testId)
session.commit()
session.close()
print "datetime: %s"% datetime.datetime.now()

# string = ""
# string = [1,2,5]
# u = str(string)
# print type(u)
# print u[:-1]
# print type(long(u[1]))
# print string
# print type(string)
# print type(string[1])
# dict = {1: "a", 2:"b"}
# print type(dict.get("key","".decode('utf8'))), "is"
# if dict.get("key","".decode('utf8')) is not None:
#     print " not Null"
# print type(long(0))
# a = [4,5,6,7]
# b = str(a).decode('utf8')
# print b
# print type(b)
# for i in b:
#     print i


# data = {}
# # data = data.fromkeys(range(2),[])
# # data[1].append('hello')
# print type(data)
# 
# com.ASeePro
# com.softdyssee.sports.french_sport_p\9D\9Dtanque
# com.ASeePro
# com.emoquiz
# 
# giggle.app.fortunefacemaker 
# stickler.mal.lyric      
# com.softdyssee.sports.french_sp                 |


