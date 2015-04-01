'''
Created on Nov 9, 2013

@author: tynguyen
'''
from __init__ import PIP

import urllib2
import socket

def is_bad_proxy(pip):    
    try:
        proxy_handler = urllib2.ProxyHandler({'http': pip})
        opener = urllib2.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib2.install_opener(opener)
        req=urllib2.Request('http://www.example.com')  # change the URL to test here
        sock=urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print 'Error code: ', e.code
        return e.code
    except Exception, detail:
        print "ERROR:", detail
        return True
    return False


def pip_return(filename = "proxylist.txt"):
    GoodProxies = []
    socket.setdefaulttimeout(120)
    try:
        ProxyList =  [line for line in open(filename, 'ra')]
    except IOError:
        return [PIP]
        print "Cannot open the proxylist.txt!"

    for CurrentProxy in ProxyList:
        if is_bad_proxy(CurrentProxy):
            print "Bad Proxy %s" % (CurrentProxy)
        else:
            print "%s is working" % (CurrentProxy)
            GoodProxies += CurrentProxy
    return GoodProxies
            
