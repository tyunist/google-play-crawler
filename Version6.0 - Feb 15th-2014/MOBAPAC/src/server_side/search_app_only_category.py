'''
Created on Dec 1, 2013
@attention: This module search apps by only one method: categories. Then, insert new apps into id table
@author: tynguyen
'''

from __init__ import *
import sys
from google_api.getAppByCategory import get_app_by_category, ConnectionError
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
        write_log(["server_side.search_app_only_category: ",datetime.datetime.utcnow(),"Connection Error while trying to log in Google Store"])
        raise   
    
def write_log(list):
    with open(LOG_PATH+"/re_search_app_only_category.csv", "a+b") as f:
        writer = csv.writer(f,delimiter ='\t', quotechar=''  ,quoting=csv.QUOTE_NONE)
        writer.writerow(list)  

#This function read a file and return list of rows in the file.
def input_row(filename):
    with open(filename,"rb") as f:
        try:
            return [line.rstrip() for line in f]
        except IOError:
            raise IOError
    
    
def search_app_only_category():    
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
     
    print "server_side.search_app_only_category    Importing categories into Database."
    write_log(["server_side.search_app_only_category: ",datetime.datetime.utcnow(),"Importing categories into Database"])
    CategoryList = []
    N_category_inserted = 0
    try:
        CategoryList = input_row(IMPORT_PATH+"/categories.txt")
    except IOError:
        print "server_side.search_app_only_category    Cannot read cateogories.txt file!"
        write_log(["server_side.search_app_only_category: ",datetime.datetime.utcnow(),"Cannot read cateogories.txt file!"])
        pass
    
    if len(CategoryList) == 0:
        write_log(["server_side.search_app_only_category: ",datetime.datetime.utcnow(),"cateogories.txt file is empty!"])
        print "File is empty!"
    else:
        for i in range(len(CategoryList)):
            temp = CategoryList[i].decode('utf8')
            categories = Categories(temp)
            if session.query(func.count(Categories.category_index)).filter(Categories.category_name == temp).scalar():
                print "server_side.search_app_only_category    %s existed already!"%temp
                write_log(["server_side.search_app_only_category: ",datetime.datetime.utcnow(),"%s existed already!"%temp])
                continue 
                 
            else:
                session.add(categories)
                print "server_side.search_app_only_category    category inserted:",temp
                write_log(["server_side.search_app_only_category: ",datetime.datetime.utcnow(),"%s is inserted!"%temp])
                N_category_inserted +=1
                # Success, commit
                session.commit()
    
    print "server_side.search_app_only_category    Finish importing categories into Database!"
    write_log(["server_side.search_app_only_category: ",datetime.datetime.utcnow(),"Finish importing %d categories into Database!"%N_category_inserted]) 
    #===============================================================================
    # Search apps and write them to a list
    #===============================================================================
    print "server_side.search_app_only_category    Searching for new apps #1!"
    write_log(["*****************************************************************"]) 
    write_log(["server_side.search_app_only_category: ",datetime.datetime.utcnow(),"Searching for new apps using categories"]) 
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
            print "server_side.search_app_only_category    category:",category
            subcategory = SubcategoryList[j]
            print "server_side.search_app_only_category    subcategory:",subcategory
            write_log(["server_side.search_app_only_category: ",datetime.datetime.utcnow(),"Current category, subcategory:%s, %s"%(category, subcategory)]) 
            search_by_category_each_at = datetime.datetime.utcnow()
            try:
                app_list_by_category_each = get_app_by_category(api, category, subcategory)
            except SSLError:
                print "server_side.search_app_only_category    SSL Error occur!"
                write_log(["server_side.search_app_only_category: ",datetime.datetime.utcnow(),"SSLError while search apps by category"]) 
                sys.exit(1)
            except ConnectionError as e:
                print"server_side.search_app_only_category    ", e
                write_log(["server_side.search_app_only_category: ",datetime.datetime.utcnow(), e]) 
                sys.exit(1)
            
            else:
                write_log(["server_side.search_app_only_category: ",datetime.datetime.utcnow(),"Time to search apps for this category:",datetime.datetime.utcnow() - search_by_category_each_at]) 
                write_log(["server_side.search_app_only_category: ",datetime.datetime.utcnow(),"Category& subcategory:%s, %s searched %d apps"%(category, subcategory, len(app_list_by_category_each))]) 
                
                #Now, insert news apps into id table
                write_log(["--------------------------------------------------------"])
                write_log(["server_side.search_app_only_category: ",datetime.datetime.utcnow(),"Inserting searched apps to id table"]) 
                N_app_inserted_category_each = 0
                insert_app_category_each_at = datetime.datetime.utcnow()
                for i in range(len(app_list_by_category_each)):  
                    if session.query(func.count(Id_extent.app_id)).filter(Id_extent.app_id ==app_list_by_category_each[i]).scalar():
                        print "server_side.search_app_only_category. App existed!"
                        continue
                    else:
                        IdTemp = Id_extent(app_list_by_category_each[i])
                        session.add(IdTemp)
                        session.commit() 
                        N_app_inserted_category_each += 1
                write_log(["server_side.search_app_only_category: ",datetime.datetime.utcnow(),"Inserted %d app with category& subcategory = %s, %s"%(N_app_inserted_category_each, category, subcategory)])         
                write_log(["server_side.search_app_only_category: ",datetime.datetime.utcnow(),"Time to insert %d apps into id table:"%N_app_inserted_category_each, datetime.datetime.utcnow() - insert_app_category_each_at]) 
                N_app_inserted_category_total += N_app_inserted_category_each
    write_log(["server_side.search_app_only_category: ",datetime.datetime.utcnow(),"Time to finish search apps by category:",datetime.datetime.utcnow() - search_by_category_at])   
    write_log(["server_side.search_app_only_category: ",datetime.datetime.utcnow(),"Finish search-by-category! "]) 
    write_log(["*****************************************************************"])
    write_log(["server_side.search_app_only_category: ",datetime.datetime.utcnow(),"Number of apps Inserted with searching by category:%d "%N_app_inserted_category_total])  
    write_log(["**************************END***************************************"])
            
    
    
    session.close()
    