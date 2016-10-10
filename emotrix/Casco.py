import serial
import time
from pymongo import MongoClient
from InputDeviceInterface import InputDeviceInterface
from ReadingThread import ReadingThread

class Casco(InputDeviceInterface):

    device_handler = None
    db = None
    port = None
    baudrate = 0
    is_reading = False
    reading_thread = None

    def connect(self, port, baudrate):
        try:
            self.device_handler = serial.Serial(port, baudrate, timeout=1)
            self.port = port
            self.baudrate = baudrate

            self.startDatabase()
        except Exception, e:
            raise e

    def isConnected(self):
        return self.device_handler.isOpen()

    def getStatus(self):
        pass

    def closePort(self):
        # Si no esta conectado, no puede cerrar.
        if (not self.isConnected()):
            print "Device is not conected!"
            return False

        # Si todavia esta leyendo, no puede cerrar.
        if (self.is_reading):
            print "Can't close port because is still reading!"
            return False

        print "Closing port " + str(self.port) + "..."

        self.device_handler.close()

        print "Port " + str(self.port) + " closed successfully!"
        return True

    def setPort(self, port):
        self.port = port

    def getPort(self):
        return self.port;

    def setBaudRate(self, baudrate):
        self.baudrate = baudrate

    def getBaudRate(self):
        return self.baudrate

    def startReading(self):
        if (not self.isConnected()):
            print "Device is not conected!"
            return None

        if (not self.db):
            print "Mongo db not initialized!"
            return None            

        print "Start reading"
        self.reading_thread = ReadingThread(1, self.device_handler)
        self.reading_thread.start()
        self.is_reading = True

    def stopReading(self):
        self.reading_thread.stopReading()
        # Wait for a moment so that the thread ends.
        time.sleep(0.1)
        self.is_reading = False

    def __startDatabase(self):
        client = MongoClient()
        self.db = client.emotrix
        # print client.database_names()
        # print self.db.collection_names()

    def __getDatabase(self):
        return self.db
