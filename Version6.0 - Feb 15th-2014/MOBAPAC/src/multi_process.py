'''
Created on Nov 18, 2013

@author: tynguyen
'''
from server_side.__init__ import *
import multiprocessing, csv, datetime
from server_side.search_app_only_category import search_app_only_category
from server_side.search_app_only_keyword import search_app_only_keyword 
from server_side.import_app_v5 import import_app
from server_side.search_comment_v5 import search_comment
from server_side.update_infor_v5 import update_infor

    
def write_log(list):
    with open(LOG_PATH+"/multi_process.csv", "a+b") as f:
        writer = csv.writer(f,delimiter ='\t', quotechar=''  ,quoting=csv.QUOTE_NONE)
        writer.writerow(list)  

if __name__ == '__main__':
    print datetime.datetime.utcnow(), "Start multi-processing"
    write_log([datetime.datetime.utcnow(), "Start multi-processing"])
    write_log(["----------------------------------------------"])
    write_log([datetime.datetime.utcnow(), "Creating processes"])
    
    
    search_app_only_category = multiprocessing.Process(name='search_app_only_category', target=search_app_only_category)
    search_app_only_keyword  = multiprocessing.Process(name='ssearch_app_only_keyword ', target=search_app_only_keyword )
    import_app = multiprocessing.Process(name='import_app', target=import_app)
    search_comment = multiprocessing.Process(name='search_comment', target=search_comment) # use default name
    update_infor = multiprocessing.Process(name='update_infor', target=update_infor)
    
    write_log(["----------------------------------------------"])
    write_log([datetime.datetime.utcnow(), "Start import_app process"])
    start_import_app_at = datetime.datetime.utcnow() 
    import_app.start()
    import_app.join()
    write_log(["----------------------------------------------"])
    write_log([datetime.datetime.utcnow(), "End import_app process"])
    write_log(["Time for import_app process:", datetime.datetime.utcnow() - start_import_app_at])
    
    write_log(["----------------------------------------------"])
    write_log([datetime.datetime.utcnow(), "Start other processes"])
    search_app_only_category.start()
    search_app_only_keyword .start()
    search_comment.start()
    update_infor.start()
    
    search_app_only_category.join()
    search_app_only_keyword .join()
    search_comment.join()
    update_infor.join()
    
     
    write_log([datetime.datetime.utcnow(), "End of the multi-process!"])
    print "Multiprocess    End of the multi-process"
    write_log(["**************************END***************************************"])

    
