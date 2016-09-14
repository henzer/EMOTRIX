from Casco import Casco
import sys
import time

casco = Casco()
"""
try:
    casco.connect('COM3', 9600)
except Exception, e:
    print e
    sys.exit(0)
"""
print casco.isConnected()
print "----------------"
#casco.startReading()
#time.sleep(5)
#casco.stopReading()
#casco.closePort()
print "----------------"
print casco.isConnected()

casco.startDatabase()
db = casco.getDatabase()
print db.toString
