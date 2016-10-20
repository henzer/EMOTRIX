# -*- coding: utf-8 -*-

import threading
import logging
import json
import time


class BraceletThreadReader(threading.Thread):
    input_handler = None
    input_buffer = None
    stop_reading = False
    persist_data = False
    db = None
    logger = None

    def __init__(self, input_handler, input_buffer, db, persist_data):
        threading.Thread.__init__(self)

        self.setName("Bracelet data reader")
        self.input_handler = input_handler
        self.input_buffer = input_buffer
        self.persist_data = persist_data
        self.db = db

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
                while (data != "{\"bpm\":"):
                    data += self.input_handler.read(1)
                    if ((len(data) > 0) and (data[0] != "{")):
                        data = ""

                # Complete a sample
                while (data[-1] != "}"):
                    data += self.input_handler.read(1)

            except Exception, e:
                raise Exception(
                    "Reading procces raise an exception.\n" + str(e)
                )

            received_count += 1

            # Load data into a JSON object
            try:
                dataJson = json.loads(data)
            except Exception, e:
                self.logger.warning(
                    "Unable to load data as a json object.\n" + str(e)
                )
                ignored_count += 1

                continue

            # Validate checksum
            checksum = dataJson.pop("chksum")
            if (not self.__assertChecksum(dataJson, checksum)):
                self.logger(
                    "Invalid data. Checksum doesn't match: " + str(dataJson)
                )
                ignored_count += 1

                continue

            # Assume that all were taken at the same time.
            timestamp = str(time.time())
            # Take only seconds
            timestamp = timestamp[0: timestamp.index(".")]
            dataJson["readed_at"] = timestamp

            # Sent data to buffer
            self.input_buffer.insert(dataJson)

            if (not self.persist_data):
                continue

            # Persisting data on DB
            try:
                self.db.bracelet_data.insert_one(dataJson)
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

    def __assertChecksum(self, data, checksum):
        suma = 0
        for key in data:
            suma += int(data[key])

        if (checksum == suma):
            return True

        return False
