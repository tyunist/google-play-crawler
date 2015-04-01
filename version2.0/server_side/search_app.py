'''
Created on Nov 9, 2013
@attention: This module search apps by two methods: categories & keywords that updated manually ( categories.txt & keywords.txt)
Then, insert new apps into id table
@author: tynguyen
'''
from google_api.getAppByCategory import get_app_by_category, get_app_by_keyword
from google_api.googleplay import GooglePlayAPI
from google_api.config import *
from create_tables import *
from sqlalchemy import *
from sqlalchemy.orm import *
import datetime, time
from requests.exceptions import SSLError

#This function read a file and return list of rows in the file.
def input_row(filename):
    try:
        return [line.rstrip() for line in open(filename,"rb")]
    except IOError:
        raise
            
#Connect to the Database
engine = create_engine('mysql://root:mobapac2013@localhost/MOBAPAC')
engine.echo = False  # Try changing this to True
Session = sessionmaker(autoflush=False)
Session.configure(bind=engine)
session = Session()

#Secondly, log in to Google Play server
api = GooglePlayAPI(ANDROID_ID)
api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)

'''
#1: Searching new apps by categories
'''
 
 
#===============================================================================
#Read categories.txt file and insert new rows into categories table
#===============================================================================
 
print "Importing categories into Database."
CategoryList = []
try:
    CategoryList = input_row("categories.txt")
except:
    print "Cannot read cateogories.txt file!"
    pass
if len(CategoryList) > 0:
    try: 
        for i in range(len(CategoryList)):
            temp = CategoryList[i].decode('utf8')
            categories = Categories(temp)
            if session.query(Categories).filter(Categories.category_name == temp).count():
                print "%s existed already!"%CategoryList[i]
                continue 
                 
            else:
                session.add(categories)
                print "category inserted:",temp
                # Success, commit
                session.commit()
                print "Inserting. Finish!"
    except:
    # If not sucessful, the transaction is rolled back ...
        session.rollback()
        print "Fail to import categories to categories table. "
        raise
else:
    print "No category new!"
print " Finish importing categories into Database!"
 
#===============================================================================
# Search apps and write them to a list
#===============================================================================
print "Searching for new apps #1!"
app_list_by_category = []
search_by_category_at = datetime.datetime.now()
# #Read categories from categories table
CategoryList = session.query(Categories.category_name).all()
# print "CategoryList:",CategoryList
SubcategoryList = ["apps_topselling_new_free", "apps_topselling_free", 
                    "apps_topselling_new_paid", "apps_topselling_paid"]

#Now, search new apps with each category and subcategory
for category in session.query(Categories).all():
    for j in range(len(SubcategoryList)):
        print "category:",category.category_name
        subcategory = SubcategoryList[j]
        print "subcategory:",subcategory
        try:
            app_list_by_category += get_app_by_category(api, category.category_name, subcategory)
        except SSLError:
            print "SSL Error occur!"
            time.sleep(10)
            #Log in a gain
            api = GooglePlayAPI(ANDROID_ID)
            api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)
            continue
        time.sleep(0.1)
print "applist:"
print "Number of apps searched:%d"%len(app_list_by_category)
 
#===============================================================================
#Insert app_list_by_category into id table 
#===============================================================================
print "Inserting new apps to id table #1!"
insert_app_1_at = datetime.datetime.now()
N_inserted_app_1 = 0
for i in range(len(app_list_by_category)):  
    try: 
        if session.query(Id).filter(Id.app_id ==app_list_by_category[i]).count():
            print "App existed!"
            continue
        else:
            IdTemp = Id(app_list_by_category[i])
#             session.flush()
            session.add(IdTemp)
            session.commit() 
            N_inserted_app_1 += 1
#             print "Inserted!"
            continue
    except:
        print "Error!Can not insert into id table"
        raise
        continue
 
print "Finish Inserting new apps to id table #1!"


#------------------------------------------------------------------------------ 

'''
#2: Searching new apps by keywords
'''
#===============================================================================
#Read keywords.txt file and input into a list
#===============================================================================

print "Reading keywords."
WordList = []
try:
    WordList = input_row("keywords.txt")
except:
    print "Cannot read keywords.txt file!"
    raise

print " Finish Reading keywords!"

#===============================================================================
# Search apps and write them to a list
#===============================================================================
print "Searching for new apps #2!"
app_list_by_keyword = []
search_by_keyword_at = datetime.datetime.now()

#Now, search new apps with each keyword
for keyword in WordList:
    print "keyword:",keyword
    try:
        app_list_by_keyword += get_app_by_keyword(api, keyword)
    except SSLError:
        print "SSL Error occur!"
        time.sleep(10)
        #Log in a gain
        api = GooglePlayAPI(ANDROID_ID)
        api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)
        continue
    time.sleep(0.1)
print "Number of apps searched #2:%d"%len(app_list_by_keyword)

#===============================================================================
#Insert app_list_by_keyword into id table 
#===============================================================================
print "Inserting new apps to id table #2!"
insert_app_2_at = datetime.datetime.now()
N_inserted_app_2 = 0
for i in range(len(app_list_by_keyword)):  
    try: 
        if session.query(Id).filter(Id.app_id ==app_list_by_keyword[i]).count():
            print "App existed!"
            continue
        else:
            IdTemp = Id(app_list_by_keyword[i])
#             session.flush()
            session.add(IdTemp)
            session.commit() 
            N_inserted_app_2 += 1
#             print "Inserted!"
            continue
    except:
        print "Error!Can not insert into id table"
        raise
        continue

print "Finish Inserting new apps to id table #2!"

# print "\nTime count for #1 :"
# print "Time of start searching #1:",search_by_category_at
# print "Time of start inserting apps to id table #1:",insert_app_1_at
# print "Number of new apps inserted into id table #1: %d"%N_inserted_app_1
print "\nTime count for #2 :"
print "Time of start searching #2:",search_by_keyword_at
print "Time of start inserting apps to id table #2:",insert_app_2_at
print "Number of new apps inserted into id table #2: %d"%N_inserted_app_2


#Close connection
print "Time of ending this process::",datetime.datetime.now()
session.close()




