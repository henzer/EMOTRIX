import serial

device_handler = serial.Serial('COM6', 9600, timeout=1)
count = 0
while (count < 5):
    print device_handler.readline()
    count += 1

device_handler.close()
