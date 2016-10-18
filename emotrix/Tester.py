from Casco import Casco
import sys
import time
import json
import datetime

puerto = 'COM3'
casco = Casco()
# casco.processData()
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
