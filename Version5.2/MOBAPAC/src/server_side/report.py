'''
Created on Dec 14, 2013

@author: tynguyen
'''
from __init__ import *
from create_tables_v5 import *
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.exc import IntegrityError
import datetime, time, csv, requests, multiprocessing

 
def write_log(list):
    with open(LOG_PATH+"/report_v5.csv", "a+b") as f:
        writer = csv.writer(f,delimiter ='\t', quotechar=''  ,quoting=csv.QUOTE_NONE)
        writer.writerow(list)
 
 
def report():
    name = multiprocessing.current_process().name
    #Connect to the Database
    engine = create_engine('mysql://root:mobapac2013@localhost/MOBA')
    engine.echo = False  # Try changing this to True
    Session = sessionmaker(autoflush=True)
    Session.configure(bind=engine)
    session = Session()
    session2=Session()
         
    '''
    Fetch number of apps, comments...
    '''
    print "Start reporting!"
    write_log(["server_side.report: ",datetime.datetime.utcnow(),"Start reporting"])
    started_at = datetime.datetime.utcnow()
    N_app = session.query(func.count(Id.app_index)).scalar()
    N_died_app = session.query(func.count(Id_died.app_died_id)).scalar()
    N_comment = session.query(func.count(Comments.comment_id)).scalar()
    N_developer = session.query(func.count(Developers.developer_index)).scalar()
    N_category = session.query(func.count(Categories.category_index)).scalar()
    
    '''
    Insert into report table
    '''
    report = Report(N_app,N_died_app,N_comment,N_developer,N_category)
    session.add(report)
    session.commit()  
         
    write_log(["server_side.report: ","*************Summarize!**********************"])
    write_log(["server_side.report: ","Number of apps:",N_app])
    write_log(["server_side.report: ","Number of died apps:",N_died_app])
    write_log(["server_side.report: ","Number of comments:",N_comment])
    write_log(["server_side.report: ","Number of developers:",N_developer])
    write_log(["server_side.report: ","Number of categories:",N_category])
    write_log(["server_side.report: ","Start reporting at:", started_at])
    write_log(["server_side.report: ","End process at:",datetime.datetime.utcnow()])
    write_log(["server_side.report: ","Total time:",(datetime.datetime.utcnow()-started_at)])
    write_log(["server_side.report: ","*************END*****************************"]) 
         
    print "Start searching app information details at:", started_at
    print "End of the process at:", datetime.datetime.utcnow()
    
    #End of the process
    session.close()
 
if __name__ == '__main__':
    report()