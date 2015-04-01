'''
Created on Nov 11, 2013
@attention: This module imports apps and their information from outer sources
@author: tynguyen
'''

import csv, sys
from google_api.getAppByCategory import get_app_by_category, get_app_by_keyword

from google_api.googleplay import GooglePlayAPI
from google_api.__init__ import *
from create_tables import *
from sqlalchemy import *
from sqlalchemy.orm import *
import datetime
def write_log(list):
    with open("re_import_app.csv", "a+b") as f:
        writer = csv.writer(f,delimiter ='\t', quotechar=''  ,quoting=csv.QUOTE_NONE)
        writer.writerow(list)
    

def remove_quotes(s):
    return ' '.join(c for c in s if c not in ('"', "'"))


#Connect to the Database
engine = create_engine('mysql://root:mobapac2013@localhost/MOBAPAC')
engine.echo = False  
Session = sessionmaker(autoflush=False)
Session.configure(bind=engine)
session = Session()


#Start process
print"Start import_app process!"
write_log([datetime.datetime.utcnow(),'Start import_app process!'])
#Read 100 app;
import_app_at = datetime.datetime.utcnow() 
N_inserted_app = 0
N_general_app = 0
with open('import_app.csv', 'a+b') as f:
    reader = csv.reader(f)
    try:
        for row in reader:
            if N_general_app > 7:
                break
            try:
                AppTemp =  remove_quotes(row).split(' ')[1].decode('utf8')
                N_general_app +=1
            except UnicodeDecodeError as e:
                print "Error %s with row:" %(e, row)
                write_log([datetime.datetime.utcnow(), "Error %s with row:"%(e, row)])
                continue
            #Mark the time:
            if N_general_app== 10:
                write_log(["Time to finish importing %d apps:"%N_general_app, (datetime.datetime.utcnow() - import_app_at)])
            elif N_general_app%100==0:
                write_log(["Time to finish importing %d apps:"%N_general_app, (datetime.datetime.utcnow() - import_app_at)])
            elif N_general_app%1000==0:
                write_log(["Time to finish importing %d apps:"%N_general_app, (datetime.datetime.utcnow() - import_app_at)])
            elif N_general_app% 10000==0:
                write_log(["Time to finish importing %d apps:"%N_general_app, (datetime.datetime.utcnow() - import_app_at)])
            elif N_general_app%100000==0:
                write_log(["Time to finish importing %d apps:"%N_general_app, (datetime.datetime.utcnow() - import_app_at)])
            
            
            try: 
                if session.query(func.count(Id.app_id)).filter(Id.app_id ==AppTemp).scalar():
#                     print "%s existed!",  remove_quotes(row).split(' ')[1]
                    continue
                else:
                    IdTemp = Id(AppTemp)
                    session.flush()  
                    session.add(IdTemp)
                    
                    session.commit() 
                    N_inserted_app += 1
        #             print "Inserted!"
                
            
            except:
                print "Error!Can not insert this app from import_app.csv into id table"
                write_log([datetime.datetime.utcnow(), "Error!Can not insert this app from import_app.csv into id table"])
                print "Current line on file:", reader.line_num
                write_log([datetime.datetime.utcnow(),"Current line on file:%d"%reader.line_num])
                raise
#                 continue
            
    except csv.Error as e:
        write_log([datetime.datetime.utcnow(),'file %s, line %d: %s' % ('import_app.csv', reader.line_num, e)])
        sys.exit('file %s, line %d: %s' % ('import_app.csv', reader.line_num, e))
 
write_log(["*************Summarize!**********************"])
write_log(["Number of new apps from file: %d"%N_general_app])
write_log(["Number of new apps imported from file: %d"%N_inserted_app])
write_log(["Start time of importing apps:", import_app_at])
write_log([" Inserting new apps to id table at: ", datetime.datetime.utcnow()])
write_log(["*************END*****************************"]) 
print "Start time of importing apps:", import_app_at
print "Finish Inserting new apps to id table at: ", datetime.datetime.utcnow()

session.close()




