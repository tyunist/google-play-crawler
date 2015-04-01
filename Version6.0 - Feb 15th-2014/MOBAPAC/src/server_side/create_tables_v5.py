'''
Updated on Nov 19, 2013

@author: tynguyen
'''
'''
Created on Nov 8, 2013
@attention: This module aimed at creating mapped-object (table & python objects)
@author: tynguyen
'''
import sys
import datetime
from sqlalchemy import Column, ForeignKey, create_engine, event, Table, Integer
from sqlalchemy.dialects.mysql import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm.interfaces import MapperExtension
from MySQLdb.constants.FLAG import UNSIGNED
from sqlalchemy.types import Unicode, UnicodeText, Text
from duplicity.tempdir import default

class BaseMixin(object):

    __table_args__ = {'mysql_engine': 'InnoDB',
                      'mysql_charset': 'utf8'}

    created_at = Column('created_at', DATETIME, nullable=False)
    updated_at = Column('updated_at', DATETIME, nullable=True)

    @staticmethod
    def create_time(mapper, connection, instance):
        now = datetime.datetime.utcnow()
        instance.created_at = now

    @staticmethod
    def update_time(mapper, connection, instance):
        now = datetime.datetime.utcnow()
        instance.updated_at = now

    @classmethod
    def register(cls):
        event.listen(cls, 'before_insert', cls.create_time)
        event.listen(cls, 'before_update', cls.update_time)


# Create base object & engine
Base = declarative_base()
engine = create_engine('mysql://root:mobapac2013@localhost/MOBA')
engine.echo = False  # Try changing this to True

#===============================================================================
# Create tables 
#===============================================================================

class Id(Base, BaseMixin):
    """ Id of application entity class """
    __tablename__ = 'id'
#     __table_args__ = {
#         'mysql_engine': 'InnoDB',
#         'mysql_charset': 'utf8'
#     } 

    app_index = Column(INTEGER(UNSIGNED=True), nullable=False, primary_key=True)
#     app_description = Column(UnicodeText)
    app_id = Column(Unicode(255), nullable=False, unique=True)
    # So far, exclusive type_index and category_index
    children = relationship("Id_died")
    children = relationship("Comments")
    children = relationship("Updated_infor") 
    
    def __init__(self, app_id):
#         self.app_description = app_description
        self.app_id = app_id
        self.register()

#     def __repr__(self):
#         return "<Id('%s','%s', '%s','%s','%s' )>" % (self.app_index, self.created_at, self.updated_at, self.app_id, self.app_description)
    def __repr__(self):
        return "<Id('%s','%s', '%s','%s')>" % (self.app_index, self.created_at, self.updated_at, self.app_id)


class Updated_infor(Base, BaseMixin):
    """ Updated Information of application entity class """
    __tablename__ = 'updated_infor'
#     __table_args__ = {
#         'mysql_engine': 'InnoDB',
#         'mysql_charset': 'utf8'
#     } 
    updated_infor_id = Column(BIGINT(UNSIGNED=True), nullable=False, primary_key=True)
    app_index = Column(INTEGER(UNSIGNED=True), ForeignKey('id.app_index', ondelete='cascade',onupdate='cascade'), nullable=False)
    app_title = Column(Unicode(50), default="".decode('utf8')) 
    app_google_pluses = Column(INTEGER(unsigned=True), default= 0) 
    app_one_ratings = Column(INTEGER(UNSIGNED=True), default= 0)
    app_two_ratings = Column(INTEGER(UNSIGNED=True), default= 0)
    app_three_ratings = Column(INTEGER(UNSIGNED=True), default= 0)
    app_four_ratings = Column(INTEGER(UNSIGNED=True), default= 0)
    app_five_ratings = Column(INTEGER(UNSIGNED=True), default= 0)
    app_ratings = Column(INTEGER(UNSIGNED=True), default= 0)
    app_avar_rating = Column(FLOAT(4.3), default= 0)
    app_comments = Column(INTEGER(UNSIGNED=True), default= 0)
    app_description = Column(UnicodeText, default="".decode('utf8'))
    type_index = Column(TINYINT(UNSIGNED=True), ForeignKey('types.type_index', ondelete='cascade',onupdate='cascade'), nullable=False)
    app_permission = Column(Unicode(300), default="".decode('utf8')) 
    app_content_rating = Column(TINYINT(UNSIGNED=True), nullable=False)
    developer_index = Column(INTEGER(UNSIGNED=True), ForeignKey('developers.developer_index', ondelete='cascade',onupdate='cascade'), nullable=False)
    app_version_string = Column(UnicodeText, nullable=False) 
    category_index = Column(TINYINT(UNSIGNED=True), ForeignKey('categories.category_index', ondelete='cascade',onupdate='cascade'), nullable=False)
    app_size = Column(Unicode(10), nullable=False )
    app_released_at = Column(Unicode(15), default="".decode('utf8'))
    app_version_number = Column(INTEGER(UNSIGNED=True), nullable=False)
    app_what_new = Column(UnicodeText, default="".decode('utf8'))
    app_downloads = Column(Unicode(25), default="".decode('utf8'))
    app_detail_url = Column(UnicodeText, default="".decode('utf8'))
    app_currency = Column(Unicode(10), default='USD'.decode('utf8'))
    app_price = Column(Unicode(10), default="".decode('utf8'))
    restriction_channel_id = Column(INTEGER(UNSIGNED=True), default= 0)
    restriction_device = Column(INTEGER(UNSIGNED=True), default= 0)
    restriction_android_id = Column(BIGINT(UNSIGNED=True), default= 0)
    
    
    

    def __init__(self,
                 app_index ,
                 app_title ,
                 app_google_pluses ,
                 app_one_ratings ,
                 app_two_ratings ,
                 app_three_ratings ,
                 app_four_ratings ,
                 app_five_ratings ,
                 app_ratings ,
                 app_avar_rating ,
                 app_comments ,
                 app_description ,
                 type_index ,
                 app_permission ,
                 app_content_rating ,
                 developer_index ,
                 app_version_string ,
                 category_index ,
                 app_size ,
                 app_released_at ,
                 app_version_number ,
                 app_what_new ,
                 app_downloads ,
                 app_detail_url ,
                 app_currency ,
                 app_price ,
                 restriction_channel_id ,
                 restriction_device ,
                 restriction_android_id ,
                              ):

        self.app_index = app_index 
        self.app_title =app_title 
        self.app_google_pluses =app_google_pluses 
        self.app_one_ratings =app_one_ratings 
        self.app_two_ratings =app_two_ratings 
        self.app_three_ratings =app_three_ratings 
        self.app_four_ratings =app_four_ratings 
        self.app_five_ratings =app_five_ratings 
        self.app_ratings =app_ratings 
        self.app_avar_rating =app_avar_rating 
        self.app_comments =app_comments 
        self.app_description =app_description 
        self.type_index =type_index 
        self.app_permission =app_permission 
        self.app_content_rating =app_content_rating 
        self.developer_index =developer_index 
        self.app_version_string =app_version_string 
        self.category_index =category_index 
        self.app_size =app_size 
        self.app_released_at =app_released_at 
        self.app_version_number =app_version_number 
        self.app_what_new =app_what_new 
        self.app_downloads =app_downloads 
        self.app_detail_url =app_detail_url 
        self.app_currency =app_currency 
        self.app_price =app_price 
        self.restriction_channel_id =restriction_channel_id 
        self.restriction_device =restriction_device 
        self.restriction_android_id =restriction_android_id 
        self.register()


    def __repr__(self):
        return """<Updated_infor('%s','%s','%s','%s','%s','%s','%s',
                               '%s','%s','%s','%s','%s','%s',
                               '%s','%s','%s','%s','%s','%s','%s',
                               '%s','%s','%s','%s','%s','%s','%s',
                               '%s', '%s','%s','%s','%s')>""" \
                     % (self.created_at,
                        self.updated_at,
                        self.updated_infor_id ,
                        self.app_index ,
                        self.app_title ,
                        self.app_google_pluses ,
                        self.app_one_ratings ,
                        self.app_two_ratings ,
                        self.app_three_ratings ,
                        self.app_four_ratings ,
                        self.app_five_ratings ,
                        self.app_ratings ,
                        self.app_avar_rating ,
                        self.app_comments ,
                        self.app_description ,
                        self.type_index ,
                        self.app_permission ,
                        self.app_content_rating ,
                        self.developer_index ,
                        self.app_version_string ,
                        self.category_index ,
                        self.app_size ,
                        self.app_released_at ,
                        self.app_version_number ,
                        self.app_what_new ,
                        self.app_downloads ,
                        self.app_detail_url ,
                        self.app_currency ,
                        self.app_price ,
                        self.restriction_channel_id ,
                        self.restriction_device ,
                        self.restriction_android_id ,
                        )                         
                                                
    

class Categories(Base, BaseMixin):
    """ Categories of applications entity class """
    __tablename__ = 'categories'
#     __table_args__ = {
#         'mysql_engine': 'InnoDB',
#         'mysql_charset': 'utf8'
#     } 
    category_index = Column(TINYINT(UNSIGNED=True), nullable=False, primary_key=True)
    category_name = Column(Unicode(30), nullable=False, unique=True)
    children = relationship("Updated_infor")
    def __init__(self, category_name):
        self.category_name = category_name
        self.register()

    def __repr__(self):
        return "<Categories('%s','%s','%s','%s' )>" % (self.category_index, self.created_at,self.updated_at, self.category_name)
       
    
class Developers(Base, BaseMixin):
    """ Developers of applications entity class """
    __tablename__ = 'developers'
#     __table_args__ = {
#         'mysql_engine': 'InnoDB',
#         'mysql_charset': 'utf8'
#     } 
    developer_index = Column(INTEGER(UNSIGNED=True), nullable=False, primary_key=True)
    developer_name = Column(Unicode(170), nullable=False)
    developer_email = Column(Unicode(254), nullable=False)
    developer_website = Column(Unicode(254))
    children = relationship("Updated_infor")
    
    def __init__(self, developer_name, developer_email, developer_website):
        self.developer_name = developer_name
        self.developer_email = developer_email
        self.developer_website = developer_website
        self.register()

    def __repr__(self):
        return "<Developers('%s','%s', '%s','%s','%s', '%s' )>" % (self.developer_index, self.created_at, self.updated_at, self.developer_name , self.developer_email, self.developer_website)
    

class Permissions(Base, BaseMixin):
    """ Permissions of applications entity class """
    __tablename__ = 'permissions'
#     __table_args__ = {
#         'mysql_engine': 'InnoDB',
#         'mysql_charset': 'utf8'
#     } 
    permission_index = Column(SMALLINT(UNSIGNED=True), nullable=False, primary_key=True)
    permission_name = Column(Unicode(120), nullable=False, unique=True)
    
    def __init__(self, permission_name):
        self.permission_name = permission_name
        self.register()

    def __repr__(self):
        return "<Permissions('%s','%s', '%s', '%s' )>" % (self.permission_index, self.created_at, self.updated_at, self.permission_name)
    

    
class Types(Base, BaseMixin):
    """ Types of applications entity class """
    __tablename__ = 'types'
#     __table_args__ = {
#         'mysql_engine': 'InnoDB',
#         'mysql_charset': 'utf8'
#     } 
    type_index = Column(TINYINT(UNSIGNED=True), nullable=False, primary_key=True)
    type_name = Column(Unicode(15), nullable=False, unique=True)
    children = relationship("Updated_infor")
    
    def __init__(self, type_name):
        self.type_name = type_name
        self.register()


    def __repr__(self):
        return "<Types('%s','%s', '%s', %s')>" % (self.type_index, self.created_at, self.updated_at, self.type_name)
    
 

class Comments(Base, BaseMixin):
    """ Comments of application entity class """
    __tablename__ = 'comments'
#     __table_args__ = {
#         'mysql_engine': 'InnoDB',
#         'mysql_charset': 'utf8'
#     } 
    id = Column('comment_id', BIGINT(UNSIGNED=True), nullable=False, primary_key=True)
    app_index = Column(INTEGER(UNSIGNED=True), ForeignKey('id.app_index', ondelete='cascade',onupdate='cascade'), nullable=False)
    app_version_string = Column(UnicodeText, default="".decode('utf8')) #use UnicodeText due to a wide range of possible app version that consists of an integer number + string
    given_by_user = Column(UnicodeText, default="".decode('utf8')) #Given as same as developer ID due to unavailable reference
    comment_given_at = Column(BIGINT(UNSIGNED=True), nullable=False, )
#     thump_ups = Column(Unicode(25), nullable=False, )
#     thump_downs = Column(Unicode(25), nullable=False, )
    rating = Column(BIGINT(UNSIGNED=True), nullable=False, default= 0)
    title = Column(UnicodeText, default="".decode('utf8')) # returned result type is string
    comment = Column(UnicodeText, default="".decode('utf8'))
    device_name = Column(UnicodeText, default="".decode('utf8')) #So far, have not found reference to it length, but returned result type is string
    
    def __init__(self,
                 app_index, app_version_string, given_by_user, 
                 comment_given_at, rating, title,
                 comment, device_name):
        
        self.app_index = app_index
        self.app_version_string = app_version_string
        self.given_by_user = given_by_user
    #         self.thump_ups = thump_ups
    #         self.thump_downs = thump_downs
        self.comment_given_at = comment_given_at
        self.rating = rating
        self.title = title
        self.comment = comment
        self.device_name = device_name
        self.register()

    def __repr__(self):
        return """<Comments('%s', '%s','%s','%s','%s',\
                                '%s','%s','%s','%s','%s',\
                                '%s'     )>"""\
             % (self.id,
                self.created_at,
                self.updated_at,
                self.app_index,
                self.app_version_string,
                self.given_by_user,
#                                                 self.thump_ups ,
#                                                 self.thump_downs ,
                self.comment_given_at ,
                self.rating ,
                self.title,
                self.comment,
                self.device_name) 
             
             
             
             
#Died id table that stores died app_ids:
class Id_died(Base, BaseMixin):
    """ Died Id of application entity class """
    __tablename__ = 'id_died'
#     __table_args__ = {
#         'mysql_engine': 'InnoDB',
#         'mysql_charset': 'utf8'
#     } 

#     app_index = Column(INTEGER(UNSIGNED=True), nullable=False, primary_key=True)
    app_died_id = Column(INTEGER(UNSIGNED=True), nullable=False, primary_key=True)
    app_index = Column(INTEGER(UNSIGNED=True), ForeignKey('id.app_index', ondelete='cascade',onupdate='cascade'))
    
#     app_description = Column(UnicodeText)
    app_id = Column(Unicode(255), nullable=False, unique=True)
    # So far, exclusive type_index and category_index
#     def __init__(self, app_description, app_id):
    def __init__(self, app_id,app_index):
#         self.app_description = app_description
        self.app_id = app_id
        self.app_index= app_index
        self.register()

#     def __repr__(self):
#         return "<Id('%s','%s', '%s','%s','%s' )>" % (self.app_index, self.created_at, self.updated_at, self.app_id, self.app_description)
    def __repr__(self):
        return "<Id('%s','%s', '%s','%s','%s')>" % (self.app_died_id,self.app_index, self.created_at, self.updated_at, self.app_id)
    
#------------------------------------------------------------------------------ 
#This following class is for testing the efficiency of searching apps by keywords.
#Remove it after testing!!
#------------------------------------------------------------------------------ 
class Id_extent(Base, BaseMixin):
    """ Id_extent of application entity class """
    __tablename__ = 'id_extent'
#     __table_args__ = {
#         'mysql_engine': 'InnoDB',
#         'mysql_charset': 'utf8'
#     } 

    app_index = Column(INTEGER(UNSIGNED=True), nullable=False, primary_key=True)
#     app_description = Column(UnicodeText)
    app_id = Column(Unicode(255), nullable=False, unique=True)
    
    def __init__(self, app_id):
#         self.app_description = app_description
        self.app_id = app_id
        self.register()

#     def __repr__(self):
#         return "<Id('%s','%s', '%s','%s','%s' )>" % (self.app_index, self.created_at, self.updated_at, self.app_id, self.app_description)
    def __repr__(self):
        return "<Id_extent('%s','%s', '%s','%s')>" % (self.app_index, self.created_at, self.updated_at, self.app_id)
                   
class Id_supplement(Base, BaseMixin):
    """ Id_supplement of application entity class """
    __tablename__ = 'id_supplement'
#     __table_args__ = {
#         'mysql_engine': 'InnoDB',
#         'mysql_charset': 'utf8'
#     } 

    app_index = Column(INTEGER(UNSIGNED=True), nullable=False, primary_key=True)
#     app_description = Column(UnicodeText)
    app_id = Column(Unicode(255), nullable=False, unique=True)
    
    def __init__(self, app_id):
#         self.app_description = app_description
        self.app_id = app_id
        self.register()

#     def __repr__(self):
#         return "<Id('%s','%s', '%s','%s','%s' )>" % (self.app_index, self.created_at, self.updated_at, self.app_id, self.app_description)
    def __repr__(self):
        return "<Id_supplement('%s','%s', '%s','%s')>" % (self.app_index, self.created_at, self.updated_at, self.app_id)
             
Base.metadata.create_all(bind=engine)

print "Creating declarative object. Finish!"    
