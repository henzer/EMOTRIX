import serial

device_handler = serial.Serial('COM6', 9600, timeout=1)
count = 0
while True:
    print device_handler.readline()
    count += 1
    if (count == 5):
        break

device_handler.close()
