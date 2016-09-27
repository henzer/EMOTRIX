"""
import serial

device_handler = serial.Serial('COM5', 9600, timeout=1)
count = 0
while True:
    print device_handler.readline()
    count += 1
    if (count == 5):
        break

device_handler.close()
"""

from bluetooth import *

print "performing inquiry..."
nearby_devices = discover_devices(lookup_names = True)
print "found %d devices:" % len(nearby_devices)

for name, addr in nearby_devices:
     print "\t%s - %s" % (addr, name)
