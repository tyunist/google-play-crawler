'''
Created on Feb 15, 2014
@attention: This module search apps only one method: keywords,then, insert new apps into id table
@author: tynguyen
'''
from __init__ import *
import sys
from google_api.getAppByCategory import get_app_by_category, get_app_by_keyword, ConnectionError
from google_api.getInforById import get_infor_dict
from google_api.googleplay import GooglePlayAPI
from google_api.__init__ import *
from create_tables_v5 import *
from sqlalchemy import *
from sqlalchemy.orm import *
import datetime, time, requests, csv, multiprocessing
from requests.exceptions import SSLError


api = GooglePlayAPI(ANDROID_ID)
def log_in():
    try:
        api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)
    except requests.exceptions.ConnectionError:
        print "Connection error"
        write_log(["server_side.search_app_only_keyword: ",datetime.datetime.utcnow(),"Connection Error while trying to log in Google Store"])
        raise   
    
def write_log(list):
    with open(LOG_PATH+"/re_search_app_only_keyword.csv", "a+b") as f:
        writer = csv.writer(f,delimiter ='\t', quotechar=''  ,quoting=csv.QUOTE_NONE)
        writer.writerow(list)  

#This function read a file and return list of rows in the file.
def input_row(filename):
    with open(filename,"rb") as f:
        try:
            return [line.rstrip() for line in f]
        except IOError:
            raise IOError

def remove_quotes(s):
    return ' '.join(c for c in s if c not in ('"', "'"))        
def csv_input_row(filename):
    with open(filename,"rb") as f:
        reader = csv.reader(f)
        try:
            return [remove_quotes(row).split('  ')[1].decode('utf8') for row in reader]    
        except (UnicodeDecodeError, csv.Error) as e:
            write_log(["server_side.search_app_only_keyword: ",datetime.datetime.utcnow(),'file %s, line %d: %s' % (filename, reader.line_num, e)])
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))    
      
            
def search_app_only_keyword():    
    name = multiprocessing.current_process().name
    #Connect to the Database
    engine = create_engine('mysql://root:mobapac2013@localhost/MOBA')
    engine.echo = False  # Try changing this to True
    Session = sessionmaker(autoflush=False)
    Session.configure(bind=engine)
    session = Session()
    
    #Secondly, log in to Google Play server
    log_in()
    
    
    #------------------------------------------------------------------------------ 
    
    '''
    #2: Searching new apps by keywords
    '''
    #===============================================================================
    #Read keywords.csv file and input into a list
    #===============================================================================
    write_log(["server_side.search_app_only_keyword: ",datetime.datetime.utcnow(),"Reading keywords from keywords.xac file"])
    WordList = []
    try:
        WordList = csv_input_row(IMPORT_PATH+"/keywords.csv")
    except IOError:
        print "server_side.search_app_only_keyword    Cannot read keywords.csv file!"
        write_log(["server_side.search_app_only_keyword: ",datetime.datetime.utcnow(),"Cannot read keywords.csv file!"])
        pass
    else:
        write_log(["server_side.search_app_only_keyword: ",datetime.datetime.utcnow(),"Finish reading keywords from keywords.csv file"])
    #===============================================================================
    # Search apps and write them to a list
    #===============================================================================
    print "server_side.search_app_only_keyword    Searching for new apps by keywords!"
    write_log(["server_side.search_app_only_keyword: ",datetime.datetime.utcnow(),"Searching for new apps by keywords"])
    app_list_by_keyword_each = []
    N_app_inserted_keyword_each = 0
    N_app_inserted_keyword_total = 0 
    search_by_keyword_at = datetime.datetime.utcnow()
    
    #Now, search new apps with each KeyWord
    for KeyWord in WordList:
        print "server_side.search_app_only_keyword  KeyWord:",KeyWord
        write_log(["server_side.search_app_only_keyword: ",datetime.datetime.utcnow(),"Current KeyWord:%s"%KeyWord]) 
        search_by_keyword_each_at = datetime.datetime.utcnow()
        try:
            app_list_by_keyword_each = get_app_by_keyword(api, KeyWord)
        except SSLError:
                print "server_side.search_app_only_keyword    SSL Error occur!"
                write_log(["server_side.search_app_only_keyword: ",datetime.datetime.utcnow(),"SSLError while search apps by keyword %s"%KeyWord]) 
                sys.exit(1)
        except ConnectionError as e:
            print "server_side.search_app_only_keyword    ",e
            write_log(["server_side.search_app_only_keyword: ",datetime.datetime.utcnow(), e]) 
            sys.exit(1)
        
        else:
            write_log(["server_side.search_app_only_keyword: ",datetime.datetime.utcnow(),"Time to search apps for this keyword:",datetime.datetime.utcnow() - search_by_keyword_each_at]) 
            write_log(["server_side.search_app_only_keyword: ",datetime.datetime.utcnow(),"Key word:%s searched %d apps"%(KeyWord, len(app_list_by_keyword_each))]) 
            
            #Now, insert news apps into id table
            write_log(["--------------------------------------------------------"])
            write_log(["server_side.search_app_only_keyword: ",datetime.datetime.utcnow(),"Inserting searched apps to id table"]) 
            N_app_inserted_keyword_each = 0
            insert_app_keyword_each_at = datetime.datetime.utcnow()
            for i in range(len(app_list_by_keyword_each)):  
                if session.query(func.count(Id_supplement.app_id)).filter(Id_supplement.app_id ==app_list_by_keyword_each[i]).scalar():
                    print "server_side.search_app_only_keyword    App existed!"
                    continue
#                 #7 following code lines are For testing:
#                 try:
#                     category_name = get_infor_dict(app_list_by_keyword_each[i], api)['details']['appDetails'].get('appCategory', ''.decode('utf8'))[0]
#                 except KeyError:
#                     print "server_side.search_app_only_keyword    NO category searched for this app"
#                     continue
#                 if category_name != "MEDICAL".decode('utf8'):
#                     print "server_side.search_app_only_keyword    App's category is", category_name
#                     continue
#                 else:
                
                # Insert app ID into id table:
                IdTemp = Id_supplement(app_list_by_keyword_each[i])
                session.add(IdTemp)
                session.commit() 
                N_app_inserted_keyword_each += 1
            write_log(["server_side.search_app_only_keyword: ",datetime.datetime.utcnow(),"Inserted %d app with keyword = %s "%(N_app_inserted_keyword_each, KeyWord)])         
            write_log(["server_side.search_app_only_keyword: ",datetime.datetime.utcnow(),"Time to insert %d apps into id table:"%N_app_inserted_keyword_each, datetime.datetime.utcnow() - insert_app_keyword_each_at]) 
            N_app_inserted_keyword_total += N_app_inserted_keyword_each
            
            
    write_log(["server_side.search_app_only_keyword: ",datetime.datetime.utcnow(),"Time to finish search apps by keyword:",datetime.datetime.utcnow() - search_by_keyword_at])   
    write_log(["server_side.search_app_only_keyword: ",datetime.datetime.utcnow(),"Finish search-by-keyword! "]) 
    write_log(["*****************************************************************"])
            
    write_log(["server_side.search_app_only_keyword: ",datetime.datetime.utcnow(),"Number of apps Inserted with searching by keyword:%d "%N_app_inserted_keyword_total])
    write_log(["**************************END***************************************"])
    session.close()
    
    
    
    
