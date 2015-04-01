import multiprocessing
import time


import multiprocessing as mp
import logging
import sys

def worker():
    print 'Doing some work'
    sys.stdout.flush()

if __name__ == '__main__':
    mp.log_to_stderr(logging.DEBUG)
    p = mp.Process(target=worker)
    p.start()
    p.join()
    

# def worker():
#     name = multiprocessing.current_process().name
#     print name, 'Starting'
#     time.sleep(2)
#     print name, 'Exiting'
# 
# def my_service(bool):
#     while bool:
#         name = multiprocessing.current_process().name
#         print name, 'Starting'
#         time.sleep(3)
#         print name, 'Exiting'
# 
# if __name__ == '__main__':
# #     service = multiprocessing.Process(name='my_service', target=my_service)
#     worker_1 = multiprocessing.Process(name='worker 1', target=worker)
#     worker_3 = multiprocessing.Process(name='worker 3', target=worker)
#      # use default name
#     
#     worker_1.start()
#     worker_1.join()
#     worker_3.start()
#     num = worker_3.is_alive()
#     service_1 = multiprocessing.Process(name='service 1',target=my_service, args=(num,))
#     service_1.start()
#     worker_3.join()
#     service_1.join()
#     
#     
#     
    
    
    
    
    
#     if worker_3.is_alive() is False:
#         worker_2.start()
#     service.start()