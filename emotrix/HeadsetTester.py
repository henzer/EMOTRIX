# -*- coding: utf-8 -*-

from Headset import Headset
import logging
import time

puerto = 'COM3'
headset = Headset(logging.INFO)

try:
    headset.connect(puerto, 115200)
except Exception, e:
    raise e

print "Is conected? " + str(headset.isConnected())
print "-----------------------------------------"
headset.startReading(persist_data=True)
time.sleep(5)
headset.stopReading()
headset.closePort()
print "-----------------------------------------"
print "Is conected? " + str(headset.isConnected())
print headset.getStatus()
