# -*- coding: utf-8 -*-

from Bracelet import Bracelet
import logging
import time

puerto = 'COM3'
bracelet = Bracelet(logging.INFO)

try:
    bracelet.connect(puerto, 115200)
except Exception, e:
    raise e

print "Is conected? " + str(bracelet.isConnected())
print "-----------------------------------------"
bracelet.startReading(persist_data=False)
time.sleep(5)
bracelet.stopReading()
bracelet.closePort()
print "-----------------------------------------"
print "Is conected? " + str(bracelet.isConnected())
print bracelet.getStatus()
