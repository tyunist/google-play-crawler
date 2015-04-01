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

GOOGLE_LOGIN = GOOGLE_PASSWORD = AUTH_TOKEN = None
from requests.exceptions import SSLError
from google_api.getCommentById import get_comment_dict
from google_api.googleplay import GooglePlayAPI
from google_api.__init__ import *
from create_tables import *
from sqlalchemy import *
from sqlalchemy.orm import *
import datetime, time

           
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
Searching new comment for each id
'''

#Fetch app_id from id table, returned result is a tuple of app_id:
print "Fetching IDs from id table!"
fetch_id_at = datetime.datetime.utcnow()
app_tuple = session.query(Id).all()
print "Number of apps:", session.query(Id.app_index).count()


#Search comments for each app_id to get lists of comment_dict and then, pass them to a list
total_dict = {}
print "Searching for new comments!"
search_comment_at = datetime.datetime.utcnow()
for pack in app_tuple:
    try:
        comment_list_of_dict = get_comment_dict(pack.app_id, api)
        total_dict.update({pack.app_index:comment_list_of_dict})
    except SSLError:
        print "SSL Error occur!"
        time.sleep(10)
        #Log in a gain
        api = GooglePlayAPI(ANDROID_ID)
        api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)
        continue
  

print "type of total dict:", type(total_dict)  
# print "total dict is:", total_dict
    

#------------------------------------------------------------------------------ 
#Insert comments into comments table:
#------------------------------------------------------------------------------ 

#Get set of app_index in total dict:
print "Fetching app_index!"
fetch_index_at = datetime.datetime.utcnow()
# print "Total dict:", total_dict
new_set_app_index = set(total_dict.iterkeys())
print "new_set_app_index", new_set_app_index

#Now, choose app_index that does not exist in comments table and inserts the whole of its comments:
print "Inserting new comments of new apps!"
N_comment_new_app = 0
N_comment_old_app = 0
insert_comment__at = datetime.datetime.utcnow()
for i in new_set_app_index:
    if session.query(Comments.app_index).filter(Comments.app_index==i).count() is None:
        print "i:", i ,"type:",type(i)
        comment_list_of_dict = total_dict[i]
        for comment_dict in comment_list_of_dict:
            comments = Comments(
                           app_index = i, app_version_string = comment_dict.get('documentVersion',''.decode('utf8')), 
                           given_by_user = comment_dict.get('commentId',''.decode('utf8')),
                           comment_given_at = comment_dict.get('timestampMsec',0),
                           rating = comment_dict.get('starRating',0),
                           title = comment_dict.get('title',''.decode('utf8')),
                           comment = comment_dict.get('comment',''.decode('utf8')),
                           device_name = comment_dict.get('deviceName',''.decode('utf8'))
                           )
            session.add(comments)
            session.flush()
            N_comment_new_app += 1
        session.commit()
        print "Finish inserting new comments of new apps!"  
        #Continue... consider app_index that does exist in comments table and inserts not the whole but the new comments
        print "Inserting new comments of old apps!"
    
    else: #Consider each comment_list_of_dict of each app_index
        comment_list_of_dict = total_dict[i]
        for comment_dict in comment_list_of_dict:  #Consider each comment_dict of each app_index
#Case 5:
            if session.query(Comments.app_index).filter(and_(
                               Comments.app_index == i,
                               Comments.app_version_string == comment_dict.get('documentVersion',''.decode('utf8')), 
                               Comments.given_by_user == comment_dict.get('commentId',''.decode('utf8')),
                               Comments.comment_given_at == comment_dict.get('timestampMsec',0))).count(): #Case 5 mention at the beginning of the process
                print "Comment existed!"
                continue

#Case 4:        
            comments =  session.query(Comments.app_index).filter(and_(
                               Comments.app_index == i,
                               Comments.app_version_string == comment_dict.get('documentVersion',''.decode('utf8')), 
                               Comments.given_by_user == comment_dict.get('commentId',''.decode('utf8')))).first()
            if comments is not None:
                comments.comment = comment_dict.get('comment',''.decode('utf8'))    #Update comment text (user might edited his comment recently
                session.flush()
          
#The remaing cases
        #Just insert all comments
            comments = Comments(
                           app_index=i, app_version_string=comment_dict.get('documentVersion',''.decode('utf8')),
                           given_by_user=comment_dict.get('commentId',''.decode('utf8')), 
                           comment_given_at=comment_dict.get('timestampMsec',0),
                           rating=comment_dict.get('starRating',0),
                           title=comment_dict.get('title', ''.decode('utf8')),
                           comment=comment_dict.get('comment', ''.decode('utf8')),
                           device_name=comment_dict.get('deviceName', ''.decode('utf8'))
                           )
            session.add(comments)
            session.flush()
            N_comment_old_app += 1
session.commit()



print "Finish inserting new comments of old apps!"
print "No of new comments of new apps:", N_comment_new_app
print "No of new comments of old apps:", N_comment_old_app
print "Searching for new comments at:!", search_comment_at
print "Inserting new comments of new apps at!", insert_comment__at
print "End process at:", datetime.datetime.utcnow()
print "Title of a comment: ", session.query(Comments.title).filter(Comments.app_index == 5).first() 
print "Title of a comment: ", session.query(Comments.title).filter(Comments.app_index == 2).first()
print "Title of a comment: ", session.query(Comments.title).filter(Comments.app_index == 3).first()  
print "Type: ", type(session.query(Comments.title).filter(Comments.app_index == 3).first())
print "Type 2:", type(session.query(Comments.title).filter(Comments.app_index == 3).all()  )
print "Calcu", session.query(Comments.id).first()*2
print "type 3:%d"% type(session.query(Comments.id).first()*2)
session.close()



        

