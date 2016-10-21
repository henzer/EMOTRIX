from Bracelet import Bracelet
import time
import sys

puerto = 'COM3'
bracelet = Bracelet()
print "Conectando a puerto {}.".format(puerto)
try:
    bracelet.connect(puerto, 9600)
except Exception, e:
    print e
    sys.exit(0)

print "Is conected? " + str(bracelet.isConnected())
print "----------------"
bracelet.startReading(persist_data=False)
time.sleep(10)
bracelet.stopReading()
bracelet.closePort()
print "----------------"
print "Is conected? " + str(bracelet.isConnected())
print bracelet.getStatus()
