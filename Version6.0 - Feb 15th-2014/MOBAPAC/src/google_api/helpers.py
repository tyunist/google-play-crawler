from __init__ import SEPARATOR
import csv, codecs, cStringIO
from ctypes import*
def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB','TB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0

def print_header_line():
    l = [ "Title",
                "Package name",
                "Creator",
                "Super Dev",
                "Price",
                "Offer Type",
                "Version Code",
                "Size",
                "Rating",
                "Num Downloads",
                "MajorVersionNumber",
                "versionCode",
                "versionString",
                "appCategory",
                "contentRating",
                "packageName",
                "uploadDate",
                "appType",
                "installationSize",
                "recentChanges",
             ]
    print SEPARATOR.join(l)

def print_details_line(c):
    #c.offer[0].micros/1000000.0
    #c.offer[0].currencyCode
    
    l = [ 
                c.docid,
                c.title,
                c.creator,
                c.descriptionHtml, # need to remove control characters
#                len(c.annotations.badgeForCreator), # Is Super Developer?
                c.offer[0].formattedAmount,
                            
                c.details.appDetails.versionCode,
                c.details.appDetails.versionString,
                c.details.appDetails.appCategory,
                c.details.appDetails.installationSize,
                c.details.appDetails.permission[0], #There are several permissions
                
                c.details.appDetails.numDownloads,
                c.details.appDetails.recentChangesHtml,
                c.details.appDetails.appType,
                c.details.appDetails.uploadDate,
                
               
                "%.2f" % c.aggregateRating.starRating,
                c.aggregateRating.ratingsCount,
#                c.aggregateRating.type,            #2
                c.aggregateRating.oneStarRatings,
                c.aggregateRating.twoStarRatings,
#                c.aggregateRating.thumbsUpCount,    # 0
#                c.aggregateRating.thumbsDownCount,  # 0
                c.aggregateRating.commentCount, 
                
                #Addition:
#                c.detailsUrl,                
#                c.detailsReusable,
#               
#                c.containerMetadata.estimatedResults,
                                                ]
                                                
    print SEPARATOR.join(unicode(i).encode('utf8') for i in l)
    print "anh cung khong yeu em nua roi"
    for i in range(len(l)):
        print str(i) + ":"
        
        print unicode(l[i]).encode('utf8')
    print "END"

def write_result_line(c,filetowrite):
    l = [ c.title,
                c.docid,
                c.creator,
                len(c.annotations.badgeForCreator), # Is Super Developer?
                c.offer[0].formattedAmount,
                c.offer[0].offerType
                
                #str(c.details.appDetails.versionCode),
                #str(sizeof_fmt(c.details.appDetails.installationSize)),
                #str("%.2f" % c.aggregateRating.starRating),
                #str(c.details.appDetails.numDownloads)
                ]
    #wb = UnicodeWriter(filetowrite,dialect=csv.excel,encoding = 'utf-8')
    

    wb = csv.writer(filetowrite,dialect= csv.excel,delimiter = '\t')
    wb.writerow(SEPARATOR.join(unicode(i).encode('utf8') for i in l))
    