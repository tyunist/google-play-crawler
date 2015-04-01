import csv, codecs, cStringIO

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
#        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect,delimiter='\t', **kwds)

    def next(self):
        row = self.reader.next()
#        return [unicode(s, "utf-8") for s in row]
        return [s for s in row]
    def __iter__(self):
        return self

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(f,dialect=dialect,delimiter='\t', **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        """
s.decode(encoding)

    <type 'str'> to <type 'unicode'>

u.encode(encoding)

    <type 'unicode'> to <type 'str'>

"""
        self.writer.writerow([s for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
    
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
            
def removeSpecialKey(str):
    """Remove special characters in a string"""
    for x in range(len(str)):
        if str[x] == "<br>":
            str = str.replace("<br>", r"")
    for x in range(len(str)):
        if str[x] == "<p>":
            str = str.replace("<p>", r"")
    for x in range(len(str)):
        if str[x] == "u\xc2\xb65":
            str = str.replace("u\xc2\xb65", r" ")
    return str

#Addition by Ty    

#def writeComponent(self, list):
#
#        self.writer.writeomponent(list)
#        for i in range(len(list)):
#            if isinstance(list[i],str):
#                data = list[i].decode("utf-8")
#                self.writer.write(data)
#            else:
#                data = list[i]
#        # Fetch UTF-8 output from the queue ...
#        data = self.queue.getvalue()
#        data = data.decode("utf-8")
#         # because row input is already unicode utf-8
#        # Fetch UTF-8 output from the queue ...
#        data = self.queue.getvalue()
#       
#        # ... and reencode it into the target encoding
##        data = self.encoder.encode(data,"utf-8")
#        # write to the target stream
#        self.stream.write(data)
#        # empty queue
#        self.queue.truncate(0)            
#            
