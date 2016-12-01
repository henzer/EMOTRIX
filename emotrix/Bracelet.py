# -*- coding: utf-8 -*-

"""
Object representation for Bracelet device.
"""

import serial
import logging
from pymongo import MongoClient
from InputDeviceInterface import InputDeviceInterface
from BraceletThreadReader import BraceletThreadReader
from TimeBuffer import TimeBuffer
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

    def __init__(self, logging_level=logging.ERROR):
        """
        Creates an insance of Headset class and initializes the mandatory
        variables required by the reading process. Optionally, can receive
        the level for logging. This could be useful for debugging process.
        """
        logging.basicConfig(level=logging_level)
        self.logger = logging.getLogger(__name__)

        self.device_buffer = TimeBuffer(constants.BRACELET_TIME_WINDOW_SIZE)

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

        self.device_reader = BraceletThreadReader(
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
        self.device_reader.stopReading()
        self.device_reader.join()
        self.is_reading = False

    def getStatus(self):
        """
        Gets the quality of signal receiving from Bracelet device.
        The bracelet sends the value of the EMG signal and actual values
        for BPM (beats per minute).
        So this function returns a python dictionary like this:
            {"bpm": 3, "emg": 1}
        Possible values for "bmp" are:
            - 0: No signal
            - 1: Bad signal
            - 3: Good signal. The average of the readings taken at the last
            second is between the valid range of BMP.
        Possible values for "emg" are:
            - 0: No signal
            - 1: Bad signal
            - 3: Good signal
        """
        currentData = self.device_buffer.getAll()

        # If the buffer is not full, the signal is bad.
        if (len(currentData) < constants.BRACELET_MIN_BUFFER_SIZE):
            self.logger.info(
                "Not enough data to check signal quality. {} found.".format(
                    len(currentData)
                )
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
        if (
            helpers.average(bpmData) <= constants.BRACELET_BPM_NO_SIGNAL_MAX_AMPLITUDE
        ):
            status["bpm"] = 0
        elif (self.__is_heart_rate_valid(bpmData)):
            status["bpm"] = 3
        else:
            status["bpm"] = 1

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
            constants.BRACELET_MIN_BUFFER_SIZE,
            1000,
            constants.BRACELET_GOOD_SIGNAL_MAX_AMPLITUDE
        )
        constants.BRACELET_GOOD_SIGNAL_MIN_VAR = variance_info[0]
        constants.BRACELET_GOOD_SIGNAL_MAX_VAR = variance_info[1]

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
        data_variance = helpers.variance(samples)

        if (
            (data_variance >= constants.BRACELET_GOOD_SIGNAL_MIN_VAR) and
            (data_variance <= constants.BRACELET_GOOD_SIGNAL_MAX_VAR)
        ):
            return True

        return False

    def __is_heart_rate_valid(self, samples):
        average = helpers.average(samples)

        if (constants.MIN_HEART_RATE <= average <= constants.MAX_HEART_RATE):
            return True

        return False
