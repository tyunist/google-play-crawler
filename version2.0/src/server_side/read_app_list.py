# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Ty"
__date__ ="$Nov 12, 2013 3:47:18 AM$"

if __name__ == "__main__":
    print "Hello World"
import csv, sys
#
#with open('import_app.csv', 'a+b') as f:
#    reader = csv.reader(f, delimiter=" ", quoting=csv.QUOTE_ALL)
#    try:
#        for row in reader:
#            print row
#    except csv.Error as e:
#        sys.exit('file %s, line %d: %s' % ('import_app.csv', reader.line_num, e))
#

def remove_quotes(s):
    return ' '.join(c for c in s if c not in ('"', "'"))
with open('androidappratings-current.csv', 'a+b') as f:
    reader = csv.reader(f)
    try:
        for row in reader:
            print remove_quotes(row).split(' ')[1].decode('utf8')
            print type(remove_quotes(row).split(' ')[1].decode('utf8'))
    except csv.Error as e:
        sys.exit('file %s, line %d: %s' % ('androidappratings-current.csv', reader.line_num, e))

