# -*- coding: utf-8 -*-

import threading
import logging
import json
import datetime

class ReadingThread(threading.Thread):
    input_handler = None
    stop_reading = False
    db = None
    logger = None

    def __init__(self, input_handler, db):
        threading.Thread.__init__(self)

        self.setName("Helmet data reader")
        self.input_handler = input_handler
        self.db = db

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    # TODO: Test persisting process
    def run(self):
        if (not self.input_handler):
            raise Exception("Input handler not defined!")

        if (not self.db):
            raise Exception("Mongo db not defined!")

        self.logger.info("Starting thread: " + self.getName())
        while not self.stop_reading:
            data = ""

            try:
                data = self.input_handler.readline()
                print data
            except Exception, e:
                raise Exception("Reading procces raise an exception:\n" + str(e))

            # Si no se leyó nada, continuar.
            if (not data):
                continue

            dataJson = []
            try:
                dataJson = json.loads(data)
            except Exception, e:
                self.logger.warning("Unable to load data as a json object: {}".format(data))
                continue

            try:
                dataJson['readed_at'] = datetime.datetime.now()
                self.db.helmet_data.insert_one(dataJson)
            except Exception, e:
                raise Exception("Persisting helmet data raise an exception:\n" + str(e))
            
            

        self.logger.info("Exiting thread: " + self.getName())

    def stopReading(self):
        self.stop_reading = True

    def getStopReading(self):
        return self.stop_reading
