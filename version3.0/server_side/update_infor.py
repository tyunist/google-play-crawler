'''
Created on Nov 12, 2013
@attention: This module search information details for each app_id stored in id table which are then inserted into updated_infor table
@author: tynguyen
'''
from google_api.getInforById import get_infor_dict
from google_api.googleplay import GooglePlayAPI
from google_api.__init__ import *
from create_tables import *
from sqlalchemy import *
from sqlalchemy.orm import *
import datetime, time
from requests.exceptions import SSLError


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
Searching information details for each id
'''
#Fetch app_id from id table, returned result is a tuple of app_id:
print "Start searching app information details!"
started_at = datetime.datetime.utcnow()
N_updated_infor = 0
for AppTemp in session.query(Id).all():   
    if AppTemp is None:
        break
    app_id = AppTemp.app_id
    try:
        infor_dict = get_infor_dict(app_id, api) #Search information details for this app, returned result is infor_dict
        if infor_dict is None:   
            continue
        
        #Create an instance of Updated_infor class that maps Python object with rows in updated_infor table:
        updated_infor = Updated_infor(
                                        app_index = AppTemp.app_index ,
                                        app_title = "".decode('utf8'),
                                        app_google_pluses =0,
                                        app_one_ratings = "".decode('utf8'),
                                        app_two_ratings = "".decode('utf8'),
                                        app_three_ratings = "".decode('utf8'),
                                        app_four_ratings = "".decode('utf8'),
                                        app_five_ratings = "".decode('utf8'),
                                        app_ratings =0,
                                        app_avar_rating = "".decode('utf8'),
                                        app_comments = "".decode('utf8'),
                                        app_description = "".decode('utf8'),
                                        type_index = 0 ,
                                        app_permission = "".decode('utf8'),
                                        app_content_rating =0,
                                        developer_index = 0 ,
                                        app_version_string = "".decode('utf8'),
                                        category_index = 0 ,
                                        app_size = "".decode('utf8'),
                                        app_released_at = "".decode('utf8'),
                                        app_version_number =0,
                                        app_what_new = "".decode('utf8'),
                                        app_downloads = "".decode('utf8'),
                                        app_detail_url = "".decode('utf8'),
                                        app_currency = "".decode('utf8'),
                                        app_price = "".decode('utf8'),
                                        restriction_channel_id = "".decode('utf8'),
                                        restriction_device = "".decode('utf8'),
                                        restriction_android_id = "".decode('utf8'),
                                      )
        
        
        #Now, get information details from infor_dict and pass them all to the created object: updated_infor
        
        updated_infor.app_title = infor_dict.get('title',''.decode('utf8'))
        developer_name = infor_dict.get('creator', ''.decode('utf8')) 
        updated_infor.app_description = infor_dict.get('descriptionHtml', ''.decode('utf8'))
        
#------------------------------------------------------------------------------ 
        #Because if searched information details do not include a particular field, its key may be excluded from infor_dict,
        #Following, we must check whether the key is included in infor_dict. 
#------------------------------------------------------------------------------ 
        try:
            updated_infor.app_google_pluses = infor_dict['annotations']['plusOneData'].get('total', 0)
        except KeyError:
            continue
                    
        
        try:
            updated_infor.app_one_ratings = infor_dict['aggregateRating'].get('oneStarRatings', 0)
            updated_infor.app_two_ratings = infor_dict['aggregateRating'].get('twoStarRatings', 0)
            updated_infor.app_three_ratings = infor_dict['aggregateRating'].get('threeStarRatings', 0)
            updated_infor.app_four_ratings = infor_dict['aggregateRating'].get('fourStarRatings', 0)
            updated_infor.app_five_ratings = infor_dict['aggregateRating'].get('fiveStarRatings', 0)
            updated_infor.app_ratings = infor_dict['aggregateRating'].get('ratingsCount', 0)
            updated_infor.app_avar_rating = infor_dict['aggregateRating'].get('starRating', ''.decode('utf8'))     
            updated_infor.app_comments = infor_dict['aggregateRating'].get('commentCount', 0)
        except KeyError:
            continue
        
        
        try:
            updated_infor.app_size = infor_dict['details']['appDetails'].get('installationSize', ''.decode('utf8'))
            updated_infor.app_released_at = infor_dict['details']['appDetails'].get('uploadDate', ''.decode('utf8'))
            updated_infor.app_version_number = infor_dict['details']['appDetails'].get('versionCode', 0)
            updated_infor.app_what_new = infor_dict['details']['appDetails'].get('recentChangesHtml', ''.decode('utf8'))
            updated_infor.app_downloads = infor_dict['details']['appDetails'].get('numDownloads', ''.decode('utf8'))
            type_name = infor_dict['details']['appDetails'].get('appType', ''.decode('utf8'))
            permission_list = infor_dict['details']['appDetails'].get('permission', ''.decode('utf8'))
            updated_infor.app_content_rating = infor_dict['details']['appDetails'].get('contentRating', 0)
            updated_infor.app_detail_url =  infor_dict.get('details').get('detailsUrl', ''.decode('utf8'))   
            developer_email = infor_dict['details']['appDetails'].get('developerEmail', ''.decode('utf8'))
            developer_website = infor_dict['details']['appDetails'].get('developerWebsite', ''.decode('utf8'))
            updated_infor.app_version_string = infor_dict['details']['appDetails'].get('versionString', ''.decode('utf8'))
            category_name = infor_dict['details']['appDetails'].get('appCategory', ''.decode('utf8'))[0] 
        except KeyError:
            continue
        
        
        try:
            updated_infor.app_currency = infor_dict['offer'][0].get('currencyCode', ''.decode('utf8'))
            updated_infor.app_price = infor_dict['offer'][0].get('formattedAmount', ''.decode('utf8'))
        except KeyError:
            continue
        
        
        
        try:
            updated_infor.restriction_channel_id = infor_dict['availability']['perdeviceavailabilityrestriction'][0].get('channelId', 0)
            updated_infor.restriction_device = infor_dict['availability']['perdeviceavailabilityrestriction'][0].get('deviceRestriction', 0)
            updated_infor.restriction_android_id = infor_dict['availability']['perdeviceavailabilityrestriction'][0].get('androidId', 0)
        except KeyError:
            continue
        
#------------------------------------------------------------------------------ 
        #Following, with each app type_name, permission, category & developer_name, we have to check whether they exists already in database
        #in order to get their index.
#------------------------------------------------------------------------------ 
        if session.query(func.count(Types.type_index)).filter(Types.type_name==type_name).scalar()==0: #Not exist?
            #if not: insert
            types = Types(type_name) 
            session.add(types)
            session.commit()
            print "New type"
            #if existed: just get its index
        updated_infor.type_index = session.query(Types.type_index).filter(Types.type_name==type_name).scalar()
      
        
        permission_index_list = []
        print "1"
        for permission_name in permission_list:
            if session.query(func.count(Permissions.permission_index)).filter(Permissions.permission_name==permission_name).scalar()==0:
                permissions = Permissions(permission_name)
                session.add(permissions)
                session.commit()
                print "New permission:", permission_name
            permission_index = session.query(Permissions.permission_index).filter(Permissions.permission_name==permission_name).scalar()
            permission_index_list  = permission_index_list + [permission_index]
            updated_infor.app_permission = str(permission_index_list).decode('utf8')
                
        
        if session.query(func.count(Developers.developer_index)).filter(and_(Developers.developer_name==developer_name,
                                                                         Developers.developer_email==developer_email,
                                                                         Developers.developer_website==developer_website)).scalar()!=0:
            continue
        else:
            developers = Developers(developer_name, developer_email, developer_website)
            session.add(developers)
            session.commit()
            print "New developer:", developer_name

        updated_infor.developer_index = session.query(Developers.developer_index).filter(Developers.developer_name==developer_name).scalar()
         
       
        if session.query(func.count(Categories.category_index)).filter(Categories.category_name==category_name).scalar()==0:
            categories = Categories(category_name)
            session.add(categories)
            session.commit()
            print "New category:", category_name
        updated_infor.category_index = session.query(Categories.category_index).filter(Categories.category_name==category_name).scalar()
        
        
        
        print"App: %s"%app_id
        print"App_index: ",AppTemp.app_index 
        print"Developer index:",updated_infor.developer_index
        print"Category index:",updated_infor.category_index
        print"Permission:",updated_infor.app_permission 
        #Now, after all information details have been passed to updated_infor object, we just commit() the transaction and count
        session.add(updated_infor)
        session.commit()
        session.commit()
        N_updated_infor += 1
    
    except SSLError:
        print "SSL Error occur!"
        time.sleep(10)
        #Log in a gain
        api = GooglePlayAPI(ANDROID_ID)
        api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)
        print"App %s can not search!"%app_id
        continue
    
print "Start searching app information details at:", started_at
print "End of the process at:", datetime.datetime.utcnow()
print "Number of row inserted into table updated_infor:",N_updated_infor
#End of the process
session.close()

    
