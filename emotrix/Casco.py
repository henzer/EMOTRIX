# -*- coding: utf-8 -*-

import serial
import logging
import random
from pymongo import MongoClient
from InputDeviceInterface import InputDeviceInterface
from ReadingThread import ReadingThread
from Buffer import Buffer
import helpers
import constants

class Casco(InputDeviceInterface):
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

        self.device_buffer = Buffer(constants.BUFFER_SIZE)

        # Set bounds for good signal deviation standard.
        self.__set_signal_quality_std_range()

        # Can raise an pymongo.errors.ServerSelectionTimeoutError
        self.__start_database()

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
        currentData = self.device_buffer.getAll()

        # If the buffer is not full, the signal is bad.
        if (len(currentData) != constants.BUFFER_SIZE):
            status = {}
            for i in range(0, constants.NUMBER_OF_SENSORS):
                status["s" + str(i + 1)] = 0

            self.logger.info(
                "Not enough data to calculate the signal quality."
            )

            return status

        sensorsData = [[] for i in range(constants.NUMBER_OF_SENSORS)]
        for sample in currentData:
            sample.pop('readed_at')
            index = 0
            for sensor in sample:
                sensorsData[index].append(sample[sensor]["value"])
                index += 1

        status = {}
        for i in range(0, constants.NUMBER_OF_SENSORS):
            sensor_data_std = helpers.standard_deviation(sensorsData[i])

            # No signal
            if (
                (sensor_data_std >= constants.NO_SIGNAL_MIN_STD) and
                (sensor_data_std <= constants.NO_SIGNAL_MAX_STD)
            ):
                status["s" + str(i + 1)] = 0
            # Bad signal
            elif (
                (sensor_data_std >= constants.BAD_SIGNAL_MIN_STD) and
                (sensor_data_std <= constants.BAD_SIGNAL_MAX_STD)
            ):
                status["s" + str(i + 1)] = 1
            # Good signal
            elif (
                (sensor_data_std >= constants.GOOD_SIGNAL_MIN_STD) and
                (sensor_data_std <= constants.GOOD_SIGNAL_MAX_STD)
            ):
                status["s" + str(i + 1)] = 3
            # Signal out of range
            else:
                status["s" + str(i + 1)] = -1

        return status

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

    def startReading(self, persist_data = False):
        if (not self.isConnected()):
            raise Exception("Device is not conected.")

        if (persist_data and not self.db):
            raise Exception("Mongo db not initialized.")

        if (not self.device_buffer):
            raise Exception("Buffer not initialized.")

        self.device_reader = ReadingThread(self.device_handler, self.device_buffer, self.db, persist_data)
        self.device_reader.start()
        self.is_reading = True

    def stopReading(self):
        self.device_reader.stopReading()
        self.device_reader.join()
        self.is_reading = False

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

    def __set_signal_quality_std_range(self):        
        # No signal
        deviation_standard_info = self.__get_std_range(
            constants.BUFFER_SIZE,
            1000,
            constants.NO_SIGNAL_MAX_AMPLITUDE
        )
        constants.NO_SIGNAL_MIN_STD = deviation_standard_info[0]
        constants.NO_SIGNAL_MAX_STD = deviation_standard_info[1]

        # Bad signal
        deviation_standard_info = self.__get_std_range(
            constants.BUFFER_SIZE,
            1000,
            constants.BAD_SIGNAL_MAX_AMPLITUDE
        )
        constants.BAD_SIGNAL_MIN_STD = deviation_standard_info[0]
        constants.BAD_SIGNAL_MAX_STD = deviation_standard_info[1]

        # Good sinal
        deviation_standard_info = self.__get_std_range(
            constants.BUFFER_SIZE,
            1000,
            constants.GOOD_SIGNAL_MAX_AMPLITUDE
        )
        constants.GOOD_SIGNAL_MIN_STD = deviation_standard_info[0]
        constants.GOOD_SIGNAL_MAX_STD = deviation_standard_info[1]

    def __get_std_range(self, n, m, amplt):
        """
        Gets an approximation of the bounds for the standard deviation
        of a data set whose amplitude is amplt.
        The algorithm generates n random values betwen 0 and amplt. Over
        this n random values, calculates the standard deviation. Then,
        it repeats this process m times and finally, gets the minimun
        and maximum calculated standard deviation.
        """
        deviations = []
        for i in range (0, m):
            data = []
            for i in range (0, n):
                val = random.randint(0, amplt)
                data.append(val)
            deviations.append(helpers.standard_deviation(data))

        return min(deviations), max(deviations)
