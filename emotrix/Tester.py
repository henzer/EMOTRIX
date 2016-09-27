from Casco import Casco
import sys
import time
import json

"""
casco = Casco()

try:
    casco.connect('COM3', 9600)
except Exception, e:
    print e
    sys.exit(0)

print casco.isConnected()
print "----------------"
casco.startReading()
time.sleep(5)
casco.stopReading()
casco.closePort()
print "----------------"
print casco.isConnected()

#casco.startDatabase()
#db = casco.getDatabase()
#print db.toString
"""

data = '{'
data += '   "data": {"s1":65,"s2":63,"s3":60,"s4":77},'
data += '   "status": {"s1":1,"s2":1,"s3":2,"s4":3},'
data += '   "checksum": 4526,'
data += '   "readed_at": "2015-12-01"'
data += '}'

dataJson = json.loads(data)
print dataJson
