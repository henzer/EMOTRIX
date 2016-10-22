from Headset import Headset
import logging
import time
import sys

puerto = 'COM3'
casco = Headset(logging.INFO)
print "Conectando a puerto {}.".format(puerto)
try:
    casco.connect(puerto, 115200)
except Exception, e:
    print e
    sys.exit(0)

print "Is conected? " + str(casco.isConnected())
print "----------------"
casco.startReading(persist_data=False)
time.sleep(5)
casco.stopReading()
casco.closePort()
print "----------------"
print "Is conected? " + str(casco.isConnected())
print casco.getStatus()
