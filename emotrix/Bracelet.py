# -*- coding: utf-8 -*-

import serial
import logging
from pymongo import MongoClient
from InputDeviceInterface import InputDeviceInterface
from BraceletThreadReader import BraceletThreadReader
from Buffer import Buffer
import helpers
import constants


class Bracelet(InputDeviceInterface):
    db = None
    port = None
    baudrate = 0
    is_reading = False
    device_reader = None
    device_handler = None
    device_buffer = None
    logger = None

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.device_buffer = Buffer(constants.BRACELET_BUFFER_SIZE)

        # Set bounds for good signal deviation standard.
        self.__set_signal_quality_std_ranges()

        # Can raise an pymongo.errors.ServerSelectionTimeoutError
        self.__start_database()

    def connect(self, port, baudrate):
        try:
            self.logger.info("Connecting to port \'{}\'...".format(port))
            self.device_handler = serial.Serial(port, baudrate, timeout=1)
            self.logger.info(
                "Connection to port \'{}\' established.".format(port)
            )
            self.port = port
            self.baudrate = baudrate
        except Exception, e:
            raise e

    def isConnected(self):
        return self.device_handler.isOpen()

    def closePort(self):
        # Si no esta conectado, no puede cerrar.
        if (not self.isConnected()):
            self.logger.info("Device is not conected.")
            return False

        # Si todavia esta leyendo, no puede cerrar.
        if (self.is_reading):
            self.logger.info("Can't close port because is still reading.")
            return False

        self.logger.info("Closing port " + str(self.port) + "...")
        self.device_handler.close()
        self.logger.info("Port " + str(self.port) + " closed successfully.")

        return True

    def startReading(self, persist_data=False):
        if (not self.isConnected()):
            raise Exception("Device is not conected.")

        if (persist_data and not self.db):
            raise Exception("Mongo db not initialized.")

        if (not self.device_buffer):
            raise Exception("Buffer not initialized.")

        self.device_reader = BraceletThreadReader(
            self.device_handler,
            self.device_buffer,
            self.db,
            persist_data
        )

        self.device_reader.start()
        self.is_reading = True

    def stopReading(self):
        self.device_reader.stopReading()
        self.device_reader.join()
        self.is_reading = False

    def getStatus(self):
        currentData = self.device_buffer.getAll()

        # If the buffer is not full, the signal is bad.
        if (len(currentData) != constants.BRACELET_BUFFER_SIZE):
            self.logger.info(
                "Not enough data to calculate the signal quality."
            )

            return {"bpm": 0, "emg": 0}

        emgData = []
        bpmData = []
        for sample in currentData:
            emgData.append(sample["emg"])
            bpmData.append(sample["bpm"])

        status = {}

        # No signal
        if (self.__is_no_signal(emgData)):
            status["emg"] = 0
        # Good signal
        elif (self.__is_good_signal(emgData)):
            status["emg"] = 3
        # Bad signal
        else:
            status["emg"] = 1

        # Average heart rate
        status["bpm"] = 1 if self.__is_heart_rate_valid(bpmData) else 0

        return status

    def __start_database(self):
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

    def __set_signal_quality_std_ranges(self):
        # Good sinal
        deviation_standard_info = helpers.get_std_range(
            constants.BRACELET_BUFFER_SIZE,
            1000,
            constants.BRACELET_GOOD_SIGNAL_MAX_AMPLITUDE
        )
        constants.BRACELET_GOOD_SIGNAL_MIN_STD = deviation_standard_info[0]
        constants.BRACELET_GOOD_SIGNAL_MAX_STD = deviation_standard_info[1]

    def __is_no_signal(self, samples):
        min_value = constants.BRACELET_CENTER - (
            constants.BRACELET_NO_SIGNAL_MAX_AMPLITUDE / 2
        )

        max_value = constants.BRACELET_CENTER + (
            constants.BRACELET_NO_SIGNAL_MAX_AMPLITUDE / 2
        )

        if ((min(samples) >= min_value) and (max(samples) <= max_value)):
            return True

        return False

    def __is_good_signal(self, samples):
        data_std = helpers.standard_deviation(samples)

        if (
            (data_std >= constants.BRACELET_GOOD_SIGNAL_MIN_STD) and
            (data_std <= constants.BRACELET_GOOD_SIGNAL_MAX_STD)
        ):
            return True

        return False

    def __is_heart_rate_valid(self, samples):
        average = helpers.average(samples)

        if (constants.MIN_HEART_RATE <= average <= constants.MAX_HEART_RATE):
            return True

        return False
