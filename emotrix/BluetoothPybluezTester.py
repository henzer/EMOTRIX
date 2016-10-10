"""
sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)
bd_addr = target_address
port = 0x1001

sock.connect((bd_addr,port))

sock.recv()

sock.close()
"""

import bluetooth
import sys
bd_addr = "20:15:03:19:27:02" #itade address

port = 1
sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))
print 'Connected'
sock.settimeout(1.0)
sock.send("x")
print 'Sent data'

data = sock.recv(1)
print 'received: %s'%data

sock.close()
