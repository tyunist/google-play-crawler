'''
Created on Nov 8, 2013
@attention: This module aimed at creating mapped-object (table & python objects)
@author: tynguyen
'''
import sys
import datetime
from sqlalchemy import Column, ForeignKey, create_engine, event
from sqlalchemy.dialects.mysql import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
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
engine = create_engine('mysql://root:mobapac2013@localhost/MOBAPAC')
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
    app_id = Column(Unicode(80), nullable=False, unique=True)
    # So far, exclusive type_index and category_index
#     def __init__(self, app_description, app_id):
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
    app_description = Column(UnicodeText)
    app_index = Column(INTEGER(UNSIGNED=True), nullable=False)
    category_index = Column(TINYINT(UNSIGNED=True), nullable=False)
    developer_index = Column(INTEGER(UNSIGNED=True), nullable=False)
    permissions = Column(Unicode(290))         #Max: 145 permissions + 144 commas 
    app_version = Column(UnicodeText, nullable=False) 
    app_downloads = Column(Unicode(25), nullable=False, )
    app_comments = Column(Unicode(11), nullable=False, )
    app_avar_rating = Column(Unicode(5), nullable=False, )
    app_ratings = Column(Unicode(11), nullable=False, )
    app_one_ratings = Column(Unicode(11), nullable=False, )
    app_two_ratings = Column(Unicode(11), nullable=False, )
    app_three_ratings = Column(Unicode(11), nullable=False, )
    app_four_ratings = Column(Unicode(11), nullable=False, )
    app_five_ratings = Column(Unicode(11), nullable=False, )
    app_released_at = Column(Unicode(15), nullable=False, )
    app_size = Column(Unicode(10), nullable=False, )
    app_new_description = Column(UnicodeText)
    app_what_new = Column(UnicodeText)
    app_price = Column(Unicode(10), nullable=False, )
    app_currency = Column(Unicode(10), nullable=False, default='USD'.decode('utf8'))
    restriction_android_id = Column(Unicode(20))
    restriction_device = Column(Unicode(1))
    restriction_channel_id = Column(Unicode(1))
    app_google_pluses = Column(INTEGER(unsigned=True), nullable=False, ) 

    def __init__(self,
                 app_index, app_version, app_downloads, 
                 app_comments, app_description, category_index,
                 developer_index,permissions,
                 app_avar_rating, app_ratings, app_one_ratings, app_two_ratings,
                 app_three_ratings, app_four_ratings, app_five_ratings,
                 app_released_at, app_size, app_new_description, app_what_new,
                 app_price, app_currency, restriction_android_id,
                 restriction_device, restricion_channel_id, app_google_pluses):
        self.app_index = app_index
        self.app_version = app_version
        self.app_downloads = app_downloads
        self.app_comments = app_comments
        self.app_description = app_description
        self.category_index = category_index
        self.developer_index = developer_index
        self.permissions = permissions
        self.app_avar_rating = app_avar_rating
        self.app_ratings = app_ratings
        self.app_one_ratings = app_one_ratings
        self.app_two_ratings = app_two_ratings
        self.app_three_ratings = app_three_ratings
        self.app_four_ratings = app_four_ratings
        self.app_five_ratings = app_five_ratings
        self.app_released_at = app_released_at
        self.app_size = app_size 
        self.app_new_description = app_new_description
        self.app_what_new = app_what_new
        self.app_price = app_price
        self.app_currency = app_currency
        self.restriction_android_id = restriction_android_id
        self.restriction_device = restriction_device
        self.restriction_channel_id = restricion_channel_id
        self.app_google_pluses = app_google_pluses
        
        self.register()


    def __repr__(self):
        return """<Updated_infor('%s','%s','%s','%s','%s','%s','%s',
                               '%s','%s','%s','%s','%s',
                               '%s','%s','%s','%s','%s','%s','%s',
                               '%s','%s','%s','%s','%s','%s','%s',
                               '%s', '%s' )>""" \
                % (self.updated_infor_id, self.created_at, self.updated_at, self.app_index,
                self.app_version, self.comment_id , self.app_description, 
                self.category_index, self.developer_index, self.permissions,
                self.thump_ups ,
                self.thump_downs , self.given_at , self.rating ,
                self.title, self.comment, self.device_name, self.app_size,
                self.app_five_ratings, self.app_released_at, self.app_new_description,
                self.app_what_new, self.app_price, self.app_currency, self.restriction_android_id,
                self.restriction_device, self.restriction_channel_id, self.app_google_pluses)                         
                                                
    

class Categories(Base, BaseMixin):
    """ Categories of applications entity class """
    __tablename__ = 'categories'
#     __table_args__ = {
#         'mysql_engine': 'InnoDB',
#         'mysql_charset': 'utf8'
#     } 
    category_index = Column(TINYINT(UNSIGNED=True), nullable=False, primary_key=True)
    category_name = Column(Unicode(30), nullable=False)
    
    def __init__(self, category_name):
        self.category_name = category_name
        self.register()

    def __repr__(self):
        return "<Categories('%s','%s','%s','%s' )>" % (self.category_index, self.created_at,self.updated_at, self.category_name)
       
    
class Developer(Base, BaseMixin):
    """ Developers of applications entity class """
    __tablename__ = 'developers'
#     __table_args__ = {
#         'mysql_engine': 'InnoDB',
#         'mysql_charset': 'utf8'
#     } 
    developer_index = Column(INTEGER(UNSIGNED=True), nullable=False, primary_key=True)
    developer_id = Column(Unicode(170), nullable=False, unique=True)
    developer_email = Column(Unicode(254), nullable=False, unique=True)
    developer_website = Column(Unicode(254), nullable=False)
    
    
    def __init__(self, developer_id, developer_email, developer_website):
        self.developer_id = developer_id
        self.developer_email = developer_email
        self.developer_website = developer_website
        self.register()

    def __repr__(self):
        return "<Developers('%s','%s', '%s','%s','%s', '%s' )>" % (self.developer_index, self.created_at, self.updated_at, self.developer_id , self.developer_email, self.developer_website)
    

class Permissions(Base, BaseMixin):
    """ Permissions of applications entity class """
    __tablename__ = 'permissions'
#     __table_args__ = {
#         'mysql_engine': 'InnoDB',
#         'mysql_charset': 'utf8'
#     } 
    permission_index = Column(SMALLINT(UNSIGNED=True), nullable=False, primary_key=True)
    permission_name = Column(Unicode(120), nullable=False, unique=True)
    
    
    def __init__(self, updated_at, permission_name):
        self.updated_at = updated_at
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
    app_index = Column(INTEGER(UNSIGNED=True), nullable=False)
    app_version = Column(UnicodeText) #use UnicodeText due to a wide range of possible app version that consists of an integer number + string
    given_by_user = Column(Text) #Given as same as developer ID due to unavailable reference
    comment_given_at = Column(BIGINT(UNSIGNED=True), nullable=False, )
#     thump_ups = Column(Unicode(25), nullable=False, )
#     thump_downs = Column(Unicode(25), nullable=False, )
    rating = Column(BIGINT(UNSIGNED=True), nullable=False, )
    title = Column(Text) # returned result type is string
    comment = Column(UnicodeText)
    device_name = Column(Text) #So far, have not found reference to it length, but returned result type is string
    
    def __init__(self,
                 app_index, app_version, given_by_user, 
                 comment_given_at, rating, title,
                 comment, device_name):
        self.app_index = app_index
        self.app_version = app_version
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
        return "<Comments('%s', '%s','%s','%s','%s',\
                                '%s','%s','%s','%s','%s',\
                                '%s'     )>" % (self.id,
                                                self.created_at,
                                                self.updated_at,
                                                self.app_index,
                                                self.app_version,
                                                self.given_by_user,
#                                                 self.thump_ups ,
#                                                 self.thump_downs ,
                                                self.comment_given_at ,
                                                self.rating ,
                                                self.title,
                                                self.comment,
                                                self.device_name) 
    
Base.metadata.create_all(bind=engine)

print "Creating declarative object. Finish!"    
