# -*- coding: utf-8 -*-

import threading
import logging
import json
import time
import constants


class HeadsetThreadReader(threading.Thread):
    input_handler = None
    input_buffer = None
    stop_reading = False
    persist_data = False
    sample_length = 0
    db = None
    logger = None

    def __init__(self, input_handler, input_buffer, db, persist_data):
        threading.Thread.__init__(self)

        self.setName("Headset data reader")
        self.input_handler = input_handler
        self.input_buffer = input_buffer
        self.persist_data = persist_data
        self.db = db
        # 4 electrodes => {s1:KT,s2:HJ,s3:LS,s4:KL,cs:RH}
        self.sample_length = 6 * (constants.HEADSET_NUMBER_OF_SENSORS + 1) + 1

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def run(self):
        if (not self.input_handler):
            raise Exception("Input handler not defined!")

        if (self.persist_data and not self.db):
            raise Exception("Mongo db not defined!")

        if (not self.input_buffer):
            raise Exception("Buffer not initialized.")

        received_count = 0
        ignored_count = 0
        self.logger.info("Starting thread: " + self.getName())
        while not self.stop_reading:
            # Reading from serial port
            try:
                data = ""
                # Look for start of a sample
                while (data != "{s1"):
                    data += self.input_handler.read(1)
                    if ((len(data) > 0) and (data[0] != "{")):
                        data = ""

                # Complete a sample
                data += self.input_handler.read(self.sample_length - 3)

            except Exception, e:
                raise Exception(
                    "Reading procces raise an exception.\n" + str(e)
                )

            received_count += 1
            # Data parsing
            try:
                data = self.__parseAndConvertCharsToInts(data)
                if (not data):
                    ignored_count += 1
                    continue
            except Exception, e:
                raise Exception(
                    "Parsing procces raise an exception. \n" + str(e)
                )

            # Process data
            try:
                data = self.__processValues(data)
                if (not data):
                    ignored_count += 1
                    continue
            except Exception, e:
                raise Exception(
                    "Getting real value process raise an exception.\n" + str(e)
                )

            # Validate checksum
            checksum = data.pop("cs")
            if (not self.__assertChecksum(data, checksum)):
                self.logger.warning(
                    "Invalid data. Checksum doesn't match: {}\n{}".format(
                        checksum,
                        str(data)
                    )
                )
                ignored_count += 1

                continue

            # Assume that all were taken at the same time.
            timestamp = str(time.time())
            # Take only seconds
            timestamp = timestamp[0: timestamp.index(".")]
            data["readed_at"] = timestamp

            # Sent data to buffer
            self.input_buffer.insert(data)

            if (not self.persist_data):
                continue

            # Load data into a JSON object
            try:
                dataJson = json.loads(json.dumps(data))
            except Exception, e:
                self.logger.warning(
                    "Unable to load data as a json object.\n" + str(e)
                )
                continue

            # Persisting data on DB
            try:
                self.db.headset_data.insert_one(dataJson)
            except Exception, e:
                raise Exception(
                    "Persisting data raise an exception.\n" + str(e)
                )

        self.logger.info("Exiting thread: " + self.getName())
        self.logger.info(
            "Samples received = {}, Samples ignored:{}".format(
                received_count,
                ignored_count
            )
        )

    def stopReading(self):
        self.stop_reading = True

    def __parseAndConvertCharsToInts(self, data):
        """
        This method parses a sample of helmet data.
        A valid sample should look like this:
            {s1:KT,s2:HJ,s3:LS,s4:KL,cs:RH}
        """
        data = data.strip()
        # self.logger.info("Parsing data: " + data)

        if (len(data) != self.sample_length):
            self.logger.warning(
                "Invalid length {}. Sample should have {} chars.".format(
                    len(data),
                    self.sample_length
                )
            )
            return {}

        if ((data[0] != "{") or (data[-1] != "}")):
            self.logger.warning("Missing curly braces: " + data)
            return {}

        try:
            index = 4
            dataObject = {}
            for i in range(0, constants.HEADSET_NUMBER_OF_SENSORS):
                dataObject["s" + str(i + 1)] = {
                    "char1": ord(data[index]),
                    "char2": ord(data[index + 1])
                }
                index += 6

            dataObject["cs"] = {
                "char1": ord(data[index]),
                "char2": ord(data[index + 1])
            }
        except Exception, e:
            self.logger.warning(
                "Unable to parse data: {}\n{}".format(data, str(e))
            )
            return {}

        return dataObject

    def __processValues(self, data):
        processedValues = {}

        for key in data:
            binVal1 = "{0:b}".format(data[key]["char1"])
            binVal2 = "{0:b}".format(data[key]["char2"])
            binVal1 = binVal1.rjust(8, "0")
            binVal2 = binVal2.rjust(8, "0")
            realValue = int(binVal1 + binVal2, 2)

            if ((key != 'cs') and (realValue > constants.HEADSET_EEG_MAX_VALUE)):
                self.logger.warning(
                    "Too large value received. {}:{}".format(
                        key,
                        data[key]
                    )
                )
                return {}

            processedValues[key] = realValue

        return processedValues

    def __assertChecksum(self, data, checksum):
        suma = 0
        for key in data:
            suma += int(data[key])

        if (checksum == suma):
            return True

        return False
