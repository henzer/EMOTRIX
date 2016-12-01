# -*- coding: utf-8 -*-

"""
Object representation for Headset device.
"""

import serial
import logging
from pymongo import MongoClient
from InputDeviceInterface import InputDeviceInterface
from HeadsetThreadReader import HeadsetThreadReader
from TimeBuffer import TimeBuffer
import helpers
import constants


class Headset(InputDeviceInterface):
    db = None
    port = None
    baudrate = 0
    is_reading = False
    device_reader = None
    device_handler = None
    device_buffer = None
    logger = None

    def __init__(self, logging_level=logging.ERROR):
        """
        Creates an insance of Headset class and initializes the mandatory
        variables required by the reading process. Optionally, can receive
        the level for logging. This could be useful for debugging process.
        """
        logging.basicConfig(level=logging_level)
        self.logger = logging.getLogger(__name__)

        self.device_buffer = TimeBuffer(constants.HEADSET_TIME_WINDOW_SIZE)

        # Set bounds for good signal deviation standard.
        self.__set_signal_quality_variance_range()

    def connect(self, port, baudrate):
        """
        Attempts to establish a connection to the port received, with
        a baud rate of baudrate.
        Check PySerial's docs for possible values for baudrate.
        """
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
        """
        Check if headset device is connected.
        """
        return self.device_handler.isOpen()

    def startReading(self, persist_data=False):
        """
        Starts the serial port reading. If device isn't connected, throws
        and exception.
        *persist_data*: boolean to set if data must be stored en mongodb.
        """
        if (not self.isConnected()):
            raise Exception("Device is not conected.")

        if (not self.device_buffer):
            raise Exception("Buffer not initialized.")

        if (persist_data):
            # Can raise an pymongo.errors.ServerSelectionTimeoutError
            self.__start_database()

        self.device_reader = HeadsetThreadReader(
            self.device_handler,
            self.device_buffer,
            self.db,
            persist_data
        )

        self.device_reader.start()
        self.is_reading = True

    def stopReading(self):
        """
        Stops current reading process.
        Warning: this method doesn't close the port.
        """
        if (not self.is_reading):
            self.logger.info('Headset is not reading.')

            return

        self.device_reader.stopReading()
        self.device_reader.join()
        self.is_reading = False

    def getStatus(self):
        """
        Gets the quality of signal of each sensor. It returns a python
        dictionary like this: {"s1": 0, "s2": 3, ...}
        Possible values for each sensor are:
            - 0: No signal
            - 1: Bad signal
            - 3: Good signal
        """
        currentData = self.device_buffer.getAll()

        # If the buffer is not full, the signal is bad.
        if (len(currentData) < constants.HEADSET_MIN_BUFFER_SIZE):
            status = {}
            for i in range(0, constants.HEADSET_NUMBER_OF_SENSORS):
                status["s" + str(i + 1)] = 0

            self.logger.info(
                "Not enough data to check signal quality. {} found.".format(
                    len(currentData)
                )
            )

            return status

        sensorsData = [[] for i in range(constants.HEADSET_NUMBER_OF_SENSORS)]
        for sample in currentData:
            sample.pop('readed_at')
            index = 0
            for sensor in sample:
                sensorsData[index].append(sample[sensor])
                index += 1

        status = {}
        for i in range(0, constants.HEADSET_NUMBER_OF_SENSORS):
            # No signal
            if (self.__is_no_signal(sensorsData[i])):
                status["s" + str(i + 1)] = 0
            # Good signal
            elif (self.__is_good_signal(sensorsData[i])):
                status["s" + str(i + 1)] = 3
            # Bad signal
            else:
                status["s" + str(i + 1)] = 1

        self.logger.info(
            "Status calculated on {} samples.".format(len(currentData))
        )

        return status

    def getCurrentData(self):
        """
        Retrieve data acquired in the last second.
        """
        return self.device_buffer.getAll()

    def closePort(self):
        """
        Close current connection. If device isn't connected or program
        is still reading, it does nothing.
        """
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

    def __set_signal_quality_variance_range(self):
        # Good sinal
        variance_info = helpers.get_variance_range(
            constants.HEADSET_MIN_BUFFER_SIZE,
            1000,
            constants.HEADSET_GOOD_SIGNAL_MAX_AMPLITUDE
        )
        constants.HEADSET_GOOD_SIGNAL_MIN_VAR = variance_info[0]
        constants.HEADSET_GOOD_SIGNAL_MAX_VAR = variance_info[1]

    def __is_no_signal(self, samples):
        min_value = constants.HEADSET_CENTER - (
            constants.HEADSET_NO_SIGNAL_MAX_AMPLITUDE / 2
        )

        max_value = constants.HEADSET_CENTER + (
            constants.HEADSET_NO_SIGNAL_MAX_AMPLITUDE / 2
        )

        if ((min(samples) >= min_value) and (max(samples) <= max_value)):
            return True

        return False

    def __is_good_signal(self, samples):
        data_variance = helpers.variance(samples)

        if (
            (data_variance >= constants.HEADSET_GOOD_SIGNAL_MIN_VAR) and
            (data_variance <= constants.HEADSET_GOOD_SIGNAL_MAX_VAR)
        ):
            return True

        return False
