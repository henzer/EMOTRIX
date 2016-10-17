from Casco import Casco
import sys
import time
import json
import datetime

puerto = 'COM3'
casco = Casco()
print "Conectando a puerto {}.".format(puerto)
try:
    casco.connect(puerto, 9600)
except Exception, e:
    print e
    sys.exit(0)

print "Is conected? " + str(casco.isConnected())
print "----------------"
casco.startReading()
time.sleep(3)
casco.stopReading()
casco.closePort()
print "----------------"
print "Is conected? " + str(casco.isConnected())

"""
#casco.startDatabase()
#db = casco.getDatabase()
#print db.toString

data = '{'
data += '   "data": {"s1":65,"s2":63,"s3":60,"s4":77},'
data += '   "status": {"s1":1,"s2":1,"s3":2,"s4":3},'
data += '   "checksum": 4526'
data += '}'

dataJson = json.loads(data)
dataJson['readed_at'] = datetime.datetime.now()

print dataJson
"""
