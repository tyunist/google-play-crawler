'''
Created on Nov 11, 2013
@attention: This module imports apps and their information from outer sources
@author: tynguyen
'''

import csv, sys
from google_api.getAppByCategory import get_app_by_category, get_app_by_keyword
from google_api.googleplay import GooglePlayAPI
from google_api.config import *
from create_tables import *
from sqlalchemy import *
from sqlalchemy.orm import *
import datetime

def remove_quotes(s):
    return ' '.join(c for c in s if c not in ('"', "'"))

#Connect to the Database
engine = create_engine('mysql://root:mobapac2013@localhost/MOBAPAC')
engine.echo = False  
Session = sessionmaker(autoflush=False)
Session.configure(bind=engine)
session = Session()

import_app_at = datetime.datetime.now() 
N_inserted_app = 0
with open('import_app.csv', 'a+b') as f:
    reader = csv.reader(f)
    try:
        for row in reader:
            try:
                AppTemp =  remove_quotes(row).split(' ')[1].decode('utf8')
            except UnicodeDecodeError as e:
                print "Error %s with row:" %(e, row)
                continue
            try: 
                if session.query(Id).filter(Id.app_id ==AppTemp).count():
                    print "%s existed!",  remove_quotes(row).split(' ')[1]
                    continue
                else:
                    IdTemp = Id(AppTemp)
        #             session.flush()
                    session.add(IdTemp)
                    session.commit() 
                    N_inserted_app += 1
        #             print "Inserted!"
                    continue
            except:
                print "Error!Can not insert this app from import_app.csv into id table"
                print "Current line on file:", reader.line_num
                raise
                continue
    except csv.Error as e:
        sys.exit('file %s, line %d: %s' % ('import_app.csv', reader.line_num, e))
 

print "Number of new apps imported from file: %d"%N_inserted_app   
print "Start time of importing apps:", import_app_at     
print "Finish Inserting new apps to id table at: ", datetime.datetime.now()




