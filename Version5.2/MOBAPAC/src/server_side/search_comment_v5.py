'''
Updated on Nov 19, 2013

@author: tynguyen
'''
'''
Created on Nov 16, 2013
@change: This module v4.0 is aimed at changing the method of getting comments for application.
In details, the procedure is as following:
       - Fetch app id one by one -> request comments -> store in a comment
@author: tynguyen
'''
'''
Created on Nov 12, 2013
@attention: This module search comments for each app_id stored in id table which are then inserted into comments table
            The procedure to decide whether a comment should be inserted or updated into comments table:
        1.     New app_id                                                                          -> Insert
        2. Existed app_id     New given_by_user                                                    -> Insert
        3. Existed app_id     Existed given_by_user   New app_version_string                              -> Insert
        4. Existed app_id     Existed given_by_user   Existed app_version_string     New comment_given_at  -> Update
        5. Existed app_id     Existed given_by_user   Existed app_version_string     Existed comment_given_at  -> DO NO THING
@author: tynguyen
'''
from __init__ import *
GOOGLE_LOGIN = GOOGLE_PASSWORD = AUTH_TOKEN = None
import csv
from requests.exceptions import SSLError
from google_api.getCommentById import get_comment_dict, ConnectionError
from google_api.googleplay import GooglePlayAPI
from google_api.__init__ import *
from create_tables_v5 import *
from sqlalchemy import *
from sqlalchemy.orm import *
import time, datetime, requests, multiprocessing


api = GooglePlayAPI(ANDROID_ID)
def log_in():
    try:
        api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)
    except requests.exceptions.ConnectionError:
        print "Connection error"
        write_log(["server_side.search_comment: ",datetime.datetime.utcnow(),"Connection Error while trying to log in Google Store"])
        raise   
       
def write_log(list):
    with open(LOG_PATH+"/re_search_comment_v5.csv", "a+b") as f:
        writer = csv.writer(f,delimiter ='\t', quotechar=''  ,quoting=csv.QUOTE_NONE)
        writer.writerow(list)    

def search_comment():
    name = multiprocessing.current_process().name
    #Connect to the Database
    engine = create_engine('mysql://root:mobapac2013@localhost/MOBA')
    engine.echo = False  # Try changing this to True
    Session = sessionmaker(autoflush=False)
    Session.configure(bind=engine)
    session = Session()
    
    #Secondly, log in to Google Play server
    log_in()
    
    print"Start search_comment process!"
    write_log(["server_side.search_comment: ",datetime.datetime.utcnow(),'Start search_comment process!'])
    started_at = datetime.datetime.utcnow()
    N_app_total = 0
    N_comment_searched_total = 0
    N_comment_inserted_total = 0
    N_comment_inserted_new_app = 0
    N_comment_searched_each = 0
    N_comment_inserted_each = 0
    N_comment_updated_total = 0
    N_comment_updated_each = 0
   
    #Search comments for each app_id to get lists of comment_dict and then, pass them to a list
    print "Searching for new comments!"
    write_log(["server_side.search_comment: ",datetime.datetime.utcnow(),"Searching for new comments"])
    
    N_app_total = session.query(func.count(Id.app_index)).scalar()
    for AppTemp in session.query(Id).all():
        if session.query(func.count(Id_died.app_index)).filter(Id_died.app_index==AppTemp.app_index).scalar() != 0: # If app is died, skip it from searching comments
            current_app_index = AppTemp.app_index
            write_log(["server_side.search_comment: ",datetime.datetime.utcnow(),"Current app_index:%d, app_id: %s. App is died!"%(AppTemp.app_index,AppTemp.app_id)])
            continue
        write_log(["server_side.search_comment: ",datetime.datetime.utcnow(),"--Current app_index:%d, app_id: %s. Searching comments"%(AppTemp.app_index,AppTemp.app_id)])        
        try:
            comment_list_of_dict = get_comment_dict(AppTemp.app_id, api)
        except ConnectionError as e:
            write_log(["server_side.search_comment: ",datetime.datetime.utcnow(),e])
            time.sleep(60)
            #Log in a gain
            log_in()
            continue
#         except KeyError as e:
#             write_log(["server_side.search_comment: ",datetime.datetime.utcnow(),"App_id: %s is wrong! "%AppTemp.app_id])
#             continue
        except SSLError as e:
            print "SSL Error occur!", e
            write_log(["server_side.search_comment: ",datetime.datetime.utcnow(),"SSL Error occur, current app_id:%s"%AppTemp.app_id])
            time.sleep(60)
            #Log in a gain
            log_in()
            continue
        else:
            N_comment_searched_each = len(comment_list_of_dict) #No of comments searched for this app_id
            N_comment_searched_total += N_comment_searched_each #No of total comments searched for the whole app_id
            N_comment_inserted_each = N_comment_searched_each
            N_comment_updated_each = 0
            write_log(["server_side.search_comment: ",datetime.datetime.utcnow(),"Number of searched comments:%d"%N_comment_searched_each])
            if N_comment_searched_each == 0: # No comment -> Skip
                continue
        #----------------------------------------------------------------------------- 
            #Insert comments into comments table:
        #------------------------------------------------------------------------------ 
        
        #If app_ip has not existed already in comments list, inserts the whole of its comments:
            if session.query(func.count(distinct(Comments.app_index))).filter(Comments.app_index== AppTemp.app_index).scalar()==0:
                write_log(["server_side.search_comment: ",datetime.datetime.utcnow(),AppTemp.app_index,"is new, preparing to insert. No of comments:", N_comment_searched_each])
                for comment_dict in comment_list_of_dict:
                    comments = Comments(
                                   app_index = AppTemp.app_index, app_version_string = comment_dict.get('documentVersion',''.decode('utf8')), 
                                   given_by_user = comment_dict.get('commentId',''.decode('utf8')),
                                   comment_given_at = comment_dict.get('timestampMsec',0),
                                   rating = comment_dict.get('starRating',0),
                                   title = comment_dict.get('title',''.decode('utf8')),
                                   comment = comment_dict.get('comment',''.decode('utf8')),
                                   device_name = comment_dict.get('deviceName',''.decode('utf8'))
                                   )
                    session.add(comments)
                    session.flush()
                session.commit()
                N_comment_inserted_total += N_comment_inserted_each
                N_comment_inserted_new_app += N_comment_inserted_each
                write_log(["server_side.search_comment: ",datetime.datetime.utcnow(),"Insert successfully! %d comments"%N_comment_inserted_each]) 
                continue
         
        #If app_ip existed already in comments list, we have to check whether a comment is new or not before inserting     
            else: 
                write_log(["server_side.search_comment: ",datetime.datetime.utcnow(),AppTemp.app_index,"is old, preparing to insert. No of comments:", N_comment_searched_each])
                for comment_dict in comment_list_of_dict:  #Consider each comment_dict of each app_index
        #Case 5:
                    if session.query(func.count(distinct(Comments.app_index))).filter(and_(
                                       Comments.app_index == AppTemp.app_index,
                                       Comments.app_version_string == comment_dict.get('documentVersion',''.decode('utf8')), 
                                       Comments.given_by_user == comment_dict.get('commentId',''.decode('utf8')),
                                       Comments.comment_given_at == comment_dict.get('timestampMsec',0))).scalar() != 0: #Case 5 mentioned at the beginning of the process
                        #This comment is completely old -> do nothing.
                        N_comment_inserted_each -= 1
                        continue
        
        #Case 4:        
                    if session.query(Comments.id).filter(and_(
                                Comments.app_index == AppTemp.app_index,
                                Comments.app_version_string == comment_dict.get('documentVersion',''.decode('utf8')), 
                                Comments.given_by_user == comment_dict.get('commentId',''.decode('utf8')))).update({
                                                                                'rating':comment_dict.get('starRating',0),                                                                              
                                                                                'comment':comment_dict.get('comment',''.decode('utf8')),    #Update comment text (user might edited his comment recently
                                                                                'comment_given_at':comment_dict.get('timestampMsec',0)}) == 1:
                        write_log(["server_side.search_comment: ",datetime.datetime.utcnow(),"Comment_by_user:",comment_dict.get('commentId',''.decode('utf8')), " is updated!"])
                        N_comment_inserted_each -=1
                        N_comment_updated_each +=1
                        session.flush()
                        write_log(["server_side.search_comment: ",datetime.datetime.utcnow(),"Comment has been updated by user. Updated!"])
                        continue
        #The remaining cases
                #Just insert all comments
                    comments = Comments(
                                   app_index=AppTemp.app_index, app_version_string=comment_dict.get('documentVersion',''.decode('utf8')),
                                   given_by_user=comment_dict.get('commentId',''.decode('utf8')), 
                                   comment_given_at=comment_dict.get('timestampMsec',0),
                                   rating=comment_dict.get('starRating',0),
                                   title=comment_dict.get('title', ''.decode('utf8')),
                                   comment=comment_dict.get('comment', ''.decode('utf8')),
                                   device_name=comment_dict.get('deviceName', ''.decode('utf8'))
                                   )
                    session.add(comments)
                    session.flush()
                session.commit()
                N_comment_inserted_total += N_comment_inserted_each
                N_comment_updated_total += N_comment_updated_each
                write_log(["server_side.search_comment: ",datetime.datetime.utcnow(),"Inserted: %d comments"%N_comment_inserted_each])
                write_log(["server_side.search_comment: ",datetime.datetime.utcnow(),"Updated: %d comments"%N_comment_updated_each])
    
    
    write_log(["server_side.search_comment: ",datetime.datetime.utcnow(),"Finish inserting comments"])
    
    write_log(["server_side.search_comment: ","*************Summarize!**********************"])
    write_log(["server_side.search_comment: ","No of apps in total:", N_app_total])
    write_log(["server_side.search_comment: ","No of searched comments in total:", N_comment_searched_total])
    write_log(["server_side.search_comment: ","No of N_comment_inserted_total:", N_comment_inserted_total])
    write_log(["server_side.search_comment: ","No of N_comment_updated_total:", N_comment_updated_total])
    write_log(["server_side.search_comment: ","No of new comments of new apps", N_comment_inserted_new_app])
    write_log(["server_side.search_comment: ","No of new comments of old apps",(N_comment_inserted_total- N_comment_inserted_new_app)])
    write_log(["server_side.search_comment: ","Start process at:", started_at])
    write_log(["server_side.search_comment: ","End process at:",datetime.datetime.utcnow()])
    write_log(["server_side.search_comment: ","Total time:",(datetime.datetime.utcnow()-started_at)])
    write_log(["server_side.search_comment: ","*************END*****************************"]) 
    
    print "No of searched comments in total:", N_comment_searched_total
    print "No of N_comment_inserted_total:", N_comment_inserted_total
    print "No of N_comment_updated_total:", N_comment_updated_total
    print "No of new comments of new apps", N_comment_inserted_new_app
    print "No of new comments of old apps",(N_comment_inserted_total- N_comment_inserted_new_app)
    print "Start process at:", started_at
    print "End process at:",datetime.datetime.utcnow()
    print "Total time:",(datetime.datetime.utcnow()-started_at)
    session.close()
    
    
