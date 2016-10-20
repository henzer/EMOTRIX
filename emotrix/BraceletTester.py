from Bracelet import Bracelet
import time
import sys

puerto = 'COM4'
bracelet = Bracelet()
print "Conectando a puerto {}.".format(puerto)
try:
    bracelet.connect(puerto, 9600)
except Exception, e:
    print e
    sys.exit(0)

print "Is conected? " + str(bracelet.isConnected())
print "----------------"
bracelet.startReading(persist_data=True)
time.sleep(3)
bracelet.stopReading()
bracelet.closePort()
print "----------------"
print "Is conected? " + str(bracelet.isConnected())
# print bracelet.getStatus()
