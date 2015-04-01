'''
Created on Nov 12, 2013

@author: tynguyen
'''
GOOGLE_LOGIN = GOOGLE_PASSWORD = AUTH_TOKEN = None
from requests.exceptions import SSLError
from google_api.getCommentById import get_comment_dict
from google_api.googleplay import GooglePlayAPI
from google_api.config import *
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
 
testId = Id("com.emoquiz".decode('utf8'))
session.add(testId)
session.commit()
session.close()

# data = {}
# # data = data.fromkeys(range(2),[])
# # data[1].append('hello')
# print type(data)

