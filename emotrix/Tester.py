from Headset import Headset
import time
import sys

puerto = 'COM3'
casco = Headset()
print "Conectando a puerto {}.".format(puerto)
try:
    casco.connect(puerto, 9600)
except Exception, e:
    print e
    sys.exit(0)

print "Is conected? " + str(casco.isConnected())
print "----------------"
casco.startReading(persist_data=False)
time.sleep(10)
casco.stopReading()
casco.closePort()
print "----------------"
print "Is conected? " + str(casco.isConnected())
print casco.getStatus()
