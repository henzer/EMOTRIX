# -*- coding: utf-8 -*-

import serial
import logging
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
    logger = None

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Can raise an pymongo.errors.ServerSelectionTimeoutError
        self.__startDatabase()

    def connect(self, port, baudrate):
        try:
            self.device_handler = serial.Serial(port, baudrate, timeout=1)
            self.port = port
            self.baudrate = baudrate
        except Exception, e:
            raise e

    def isConnected(self):
        return self.device_handler.isOpen()

    def getStatus(self):
        pass

    def closePort(self):
        # Si no esta conectado, no puede cerrar.
        if (not self.isConnected()):
            self.logger.info("Device is not conected!")
            return False

        # Si todavia esta leyendo, no puede cerrar.
        if (self.is_reading):
            self.logger.info("Can't close port because is still reading!")
            return False

        self.logger.info("Closing port " + str(self.port) + "...")
        self.device_handler.close()
        self.logger.info("Port " + str(self.port) + " closed successfully!")

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
            raise Exception("Device is not conected!")

        if (not self.db):
            raise Exception("Mongo db not initialized!")

        self.reading_thread = ReadingThread(self.device_handler, self.db)
        self.reading_thread.start()
        self.is_reading = True

    def stopReading(self):
        self.reading_thread.stopReading()
        self.reading_thread.join()
        self.is_reading = False

    def __startDatabase(self):
        self.logger.info("Starting mongo client...")

        try:
            client = MongoClient("localhost", serverSelectionTimeoutMS=1)
            # Force connection on this request. This will raise an
            # exception if can't establish connection with server.
            client.server_info()

            self.db = client.emotrix_db
        except Exception, e:
            raise Exception("Unable to connect to MongoDB server. \n" + str(e))

        self.logger.info("MongoDB server connection established.")

    def __getDatabase(self):
        return self.db
