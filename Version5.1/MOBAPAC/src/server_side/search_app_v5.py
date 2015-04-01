'''
Updated on Nov 19, 2013

@author: tynguyen
'''
'''
Created on Nov 9, 2013
@attention: This module search apps by two methods: categories & keywords that updated manually ( categories.txt & keywords.txt)
Then, insert new apps into id table
@author: tynguyen
'''
from __init__ import *
import sys
from google_api.getAppByCategory import get_app_by_category, get_app_by_keyword, ConnectionError
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
        write_log(["server_side.search_app: ",datetime.datetime.utcnow(),"Connection Error while trying to log in Google Store"])
        raise   
    
def write_log(list):
    with open(LOG_PATH+"/re_search_app_v5.csv", "a+b") as f:
        writer = csv.writer(f,delimiter ='\t', quotechar=''  ,quoting=csv.QUOTE_NONE)
        writer.writerow(list)  

#This function read a file and return list of rows in the file.
def input_row(filename):
    with open(filename,"rb") as f:
        try:
            return [line.rstrip() for line in f]
        except IOError:
            raise IOError
    
    
def search_app():    
    name = multiprocessing.current_process().name
    #Connect to the Database
    engine = create_engine('mysql://root:mobapac2013@localhost/MOBA')
    engine.echo = False  # Try changing this to True
    Session = sessionmaker(autoflush=False)
    Session.configure(bind=engine)
    session = Session()
    
    #Secondly, log in to Google Play server
    log_in()
    
    '''
    #1: Searching new apps by categories
    '''
    #===============================================================================
    #Read categories.txt file and insert new rows into categories table
    #===============================================================================
     
    print "Importing categories into Database."
    write_log(["server_side.search_app: ",datetime.datetime.utcnow(),"Importing categories into Database"])
    CategoryList = []
    N_category_inserted = 0
    try:
        CategoryList = input_row(IMPORT_PATH+"/categories.txt")
    except IOError:
        print "Cannot read cateogories.txt file!"
        write_log(["server_side.search_app: ",datetime.datetime.utcnow(),"Cannot read cateogories.txt file!"])
        pass
    
    if len(CategoryList) == 0:
        write_log(["server_side.search_app: ",datetime.datetime.utcnow(),"cateogories.txt file is empty!"])
        print "File is empty!"
    else:
        for i in range(len(CategoryList)):
            temp = CategoryList[i].decode('utf8')
            categories = Categories(temp)
            if session.query(func.count(Categories.category_index)).filter(Categories.category_name == temp).scalar():
                print "%s existed already!"%temp
                write_log(["server_side.search_app: ",datetime.datetime.utcnow(),"%s existed already!"%temp])
                continue 
                 
            else:
                session.add(categories)
                print "category inserted:",temp
                write_log(["server_side.search_app: ",datetime.datetime.utcnow(),"%s is inserted!"%temp])
                N_category_inserted +=1
                # Success, commit
                session.commit()
    
    print "Finish importing categories into Database!"
    write_log(["server_side.search_app: ",datetime.datetime.utcnow(),"Finish importing %d categories into Database!"%N_category_inserted]) 
    #===============================================================================
    # Search apps and write them to a list
    #===============================================================================
    print "Searching for new apps #1!"
    write_log(["*****************************************************************"]) 
    write_log(["server_side.search_app: ",datetime.datetime.utcnow(),"Searching for new apps using categories"]) 
    write_log(["*****************************************************************"])
    search_by_category_at = datetime.datetime.utcnow()
    # #Read categories from categories table
    CategoryList = session.query(Categories.category_name).all()
    # print "CategoryList:",CategoryList
    SubcategoryList = ["apps_topselling_new_free", "apps_topselling_free", 
                        "apps_topselling_new_paid", "apps_topselling_paid"]
    app_list_by_category_each = []
    N_app_inserted_category_total = 0
    N_app_inserted_category_each = 0
    #Now, search new apps with each category and subcategory
    for categories in session.query(Categories).all():
        for j in range(len(SubcategoryList)):
            category = categories.category_name 
            print "category:",category
            subcategory = SubcategoryList[j]
            print "subcategory:",subcategory
            write_log(["server_side.search_app: ",datetime.datetime.utcnow(),"Current category, subcategory:%s, %s"%(category, subcategory)]) 
            search_by_category_each_at = datetime.datetime.utcnow()
            try:
                app_list_by_category_each = get_app_by_category(api, category, subcategory)
            except SSLError:
                print "SSL Error occur!"
                write_log(["server_side.search_app: ",datetime.datetime.utcnow(),"SSLError while search apps by category"]) 
                sys.exit(1)
            except ConnectionError as e:
                print e
                write_log(["server_side.search_app: ",datetime.datetime.utcnow(), e]) 
                sys.exit(1)
            
            else:
                write_log(["server_side.search_app: ",datetime.datetime.utcnow(),"Time to search apps for this category:",datetime.datetime.utcnow() - search_by_category_each_at]) 
                write_log(["server_side.search_app: ",datetime.datetime.utcnow(),"Category& subcategory:%s, %s searched %d apps"%(category, subcategory, len(app_list_by_category_each))]) 
                
                #Now, insert news apps into id table
                write_log(["--------------------------------------------------------"])
                write_log(["server_side.search_app: ",datetime.datetime.utcnow(),"Inserting searched apps to id table"]) 
                N_app_inserted_category_each = 0
                insert_app_category_each_at = datetime.datetime.utcnow()
                for i in range(len(app_list_by_category_each)):  
                    if session.query(func.count(Id.app_id)).filter(Id.app_id ==app_list_by_category_each[i]).scalar():
                        print "App existed!"
                        continue
                    else:
                        IdTemp = Id(app_list_by_category_each[i])
                        session.add(IdTemp)
                        session.commit() 
                        N_app_inserted_category_each += 1
                write_log(["server_side.search_app: ",datetime.datetime.utcnow(),"Inserted %d app with category& subcategory = %s, %s"%(N_app_inserted_category_each, category, subcategory)])         
                write_log(["server_side.search_app: ",datetime.datetime.utcnow(),"Time to insert %d apps into id table:"%N_app_inserted_category_each, datetime.datetime.utcnow() - insert_app_category_each_at]) 
                N_app_inserted_category_total += N_app_inserted_category_each
    write_log(["server_side.search_app: ",datetime.datetime.utcnow(),"Time to finish search apps by category:",datetime.datetime.utcnow() - search_by_category_at])   
    write_log(["server_side.search_app: ",datetime.datetime.utcnow(),"Finish search-by-comment! "]) 
    write_log(["*****************************************************************"])

    
    #------------------------------------------------------------------------------ 
    
    '''
    #2: Searching new apps by keywords
    '''
    #===============================================================================
    #Read keywords.txt file and input into a list
    #===============================================================================
    write_log(["server_side.search_app: ",datetime.datetime.utcnow(),"Reading keywords from keywords.txt file"])
    WordList = []
    try:
        WordList = input_row(IMPORT_PATH+"/keywords.txt")
    except IOError:
        print "Cannot read keywords.txt file!"
        write_log(["server_side.search_app: ",datetime.datetime.utcnow(),"Cannot read keywords.txt file!"])
        pass
    else:
        write_log(["server_side.search_app: ",datetime.datetime.utcnow(),"Finish reading keywords from keywords.txt file"])
    #===============================================================================
    # Search apps and write them to a list
    #===============================================================================
    print "Searching for new apps #2!"
    write_log(["server_side.search_app: ",datetime.datetime.utcnow(),"Searching for new apps by keywords"])
    app_list_by_keyword_each = []
    N_app_inserted_keyword_each = 0
    N_app_inserted_keyword_total = 0 
    search_by_keyword_at = datetime.datetime.utcnow()
    
    #Now, search new apps with each KeyWord
    for KeyWord in WordList:
        print "KeyWord:",KeyWord
        write_log(["server_side.search_app: ",datetime.datetime.utcnow(),"Current KeyWord:%s"%KeyWord]) 
        search_by_keyword_each_at = datetime.datetime.utcnow()
        try:
            app_list_by_keyword_each = get_app_by_keyword(api, KeyWord)
        except SSLError:
                print "SSL Error occur!"
                write_log(["server_side.search_app: ",datetime.datetime.utcnow(),"SSLError while search apps by keyword %s"%KeyWord]) 
                sys.exit(1)
        except ConnectionError as e:
            print e
            write_log(["server_side.search_app: ",datetime.datetime.utcnow(), e]) 
            sys.exit(1)
        
        else:
            write_log(["server_side.search_app: ",datetime.datetime.utcnow(),"Time to search apps for this keyword:",datetime.datetime.utcnow() - search_by_keyword_each_at]) 
            write_log(["server_side.search_app: ",datetime.datetime.utcnow(),"Key word:%s searched %d apps"%(KeyWord, len(app_list_by_keyword_each))]) 
            
            #Now, insert news apps into id table
            write_log(["--------------------------------------------------------"])
            write_log(["server_side.search_app: ",datetime.datetime.utcnow(),"Inserting searched apps to id table"]) 
            N_app_inserted_keyword_each = 0
            insert_app_keyword_each_at = datetime.datetime.utcnow()
            for i in range(len(app_list_by_keyword_each)):  
                if session.query(func.count(Id.app_id)).filter(Id.app_id ==app_list_by_keyword_each[i]).scalar():
                    print "App existed!"
                    continue
                else:
                    IdTemp = Id(app_list_by_keyword_each[i])
                    session.add(IdTemp)
                    session.commit() 
                    N_app_inserted_keyword_each += 1
            write_log(["server_side.search_app: ",datetime.datetime.utcnow(),"Inserted %d app with keyword = %s "%(N_app_inserted_keyword_each, KeyWord)])         
            write_log(["server_side.search_app: ",datetime.datetime.utcnow(),"Time to insert %d apps into id table:"%N_app_inserted_keyword_each, datetime.datetime.utcnow() - insert_app_keyword_each_at]) 
            N_app_inserted_keyword_total += N_app_inserted_keyword_each
    write_log(["server_side.search_app: ",datetime.datetime.utcnow(),"Time to finish search apps by keyword:",datetime.datetime.utcnow() - search_by_keyword_at])   
    write_log(["server_side.search_app: ",datetime.datetime.utcnow(),"Finish search-by-keyword! "]) 
    write_log(["*****************************************************************"])
            
    write_log(["server_side.search_app: ",datetime.datetime.utcnow(),"Number of apps Inserted with searching by category:%d "%N_app_inserted_category_total])
    write_log(["server_side.search_app: ",datetime.datetime.utcnow(),"Number of apps Inserted with searching by keyword:%d "%N_app_inserted_keyword_total])
    
    session.close()
    
    
    
    
