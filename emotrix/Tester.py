# -*- coding: utf-8 -*-

from Headset import Headset
from Bracelet import Bracelet
import time

headsetPort = 'COM3'
braceletPort = 'COM4'

headset = Headset()
bracelet = Bracelet()

try:
    headset.connect(headsetPort, 9600)
except Exception, e:
    raise e

try:
    bracelet.connect(braceletPort, 9600)
except Exception, e:
    headset.closePort()
    raise e

print "Headset: Is conected? " + str(headset.isConnected())
print "Bracelet: Is conected? " + str(bracelet.isConnected())
print "------------------------------------------------"
headset.startReading(persist_data=False)
bracelet.startReading(persist_data=False)

time.sleep(10)
headset.stopReading()
bracelet.stopReading()

headset.closePort()
bracelet.closePort()

print "------------------------------------------------"
print "Headset: Is conected? " + str(headset.isConnected())
print "Bracelet: Is conected? " + str(bracelet.isConnected())

print headset.getStatus()
print bracelet.getStatus()
