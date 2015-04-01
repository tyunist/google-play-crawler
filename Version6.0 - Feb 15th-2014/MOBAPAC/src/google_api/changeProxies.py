# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Ty"
__date__ ="$Oct 21, 2013 8:48:54 AM$"

if __name__ == "__main__":
    print "Change Proxies"

fileproxylist = open('proxylist.txt', 'r')
proxyList = fileproxylist.readlines()
indexproxy = 0
totalproxy = len(proxyList)

#Now for each proxy in list, call the following function:
#http://love-python.blogspot.com/2008/03/use-proxy-in-your-spider.html
def get_source_html_proxy(url, pip):

    proxy_handler = urllib2.ProxyHandler({'http': pip})
    opener = urllib2.build_opener(proxy_handler)
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib2.install_opener(opener)
    req=urllib2.Request(url)
    sock=urllib2.urlopen(req)
    data = sock.read()
    return data

#http://stackoverflow.com/questions/9340856/working-with-proxies
"""I have build a script(by help of internet resources) which takes list 
of available proxies from a particular website and then it check one by one to find the working proxy. 
Once it found it build and opener from that proxy. Here is my code."""
import urllib2
import urllib
import cookielib
import socket
import time
import re

def getOpener(pip=None):
    if pip:
        proxy_handler = urllib2.ProxyHandler({'http': pip})
        opener = urllib2.build_opener(proxy_handler)
    else:
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1')]
    urllib2.install_opener(opener)
    return opener

def getContent(opnr, url):
    req = urllib2.Request(url)
    sock = opnr.open(req)
    return sock.read()

def is_bad_proxy(pip):
    try:
        opnr = getOpener(pip)
        data = getContent(opnr, 'http://www.google.com')
    except urllib2.HTTPError, e:
        return e.code
    except Exception, detail:
        return True
    return False

def getProxiesList():
    proxies = []
    opnr = getOpener()
    content = getContent(opnr, 'http://somesite.com/')
    urls = re.findall("<a href='([^']+)'[^>]*>.*?HTTP Proxies.*?</a>", content)
    for eachURL in urls:
        content = getContent(opnr, eachURL)
        proxies.extend(re.findall('\d{,3}\.\d{,3}\.\d{,3}\.\d{,3}:\d+', content))
    return proxies

def getWorkingProxy(proxyList, i=-1):
    for j in range(i+1, len(proxyList)):
        currentProxy = proxyList[j]
        if not is_bad_proxy(currentProxy):
            log("%s is working" % (currentProxy))
            return currentProxy, j
        else:
            log("Bad Proxy %s" % (currentProxy))
    return None, -1

if __name__ == "__main__":
    socket.setdefaulttimeout(60)
    proxyList = getProxiesList()
    proxy, index = getWorkingProxy(proxyList)
    if proxy:
        _web = getOpener(proxy)