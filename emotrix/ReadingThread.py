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

    def run(self):
        if (not self.input_handler):
            raise Exception("Input handler not defined!")

        if (not self.db):
            raise Exception("Mongo db not defined!")

        self.logger.info("Starting thread: " + self.getName())
        while not self.stop_reading:
            data = ""

            # Lectura desde el puerto serial
            try:
                data = self.input_handler.readline()
                if (not data):
                    continue
            except Exception, e:
                raise Exception("Reading procces raise an exception.\n" + str(e))

            # Parseo de la data recibida
            try:
                data = self.__processData(data)
                if (not data):
                    continue
            except Exception, e:
                raise Exception("Parsing procces raise an exception. \n" + str(e))

            # Creación del objeto json con la data
            try:
                dataJson = json.loads(json.dumps(data))
            except Exception, e:
                self.logger.warning("Unable to load data as a json object.\n" + str(e))
                continue

            # Persistencia de la data en la BD
            try:
                dataJson['readed_at'] = datetime.datetime.now()
                self.db.helmet_data.insert_one(dataJson)
            except Exception, e:
                raise Exception("Persisting helmet data raise an exception.\n" + str(e))
            
            

        self.logger.info("Exiting thread: " + self.getName())

    def stopReading(self):
        self.stop_reading = True

    def getStopReading(self):
        return self.stop_reading

    def __processData(self, data):
        data = data.strip()
        data = data[1:-1]

        processedData = {}
        cont = 1;
        go = True
        while go:
            try:
                sX = data[0 : data.index(",\"s{}\":".format(cont))]
            except Exception, e:
                sX = data
                go = False

            sX = sX[5 : len(sX)]
            if (sX == 'null'):
                self.logger.warning('Invalid char received: {}'.format(sX))
            else :
                char =  sX[1:-1].decode('unicode-escape')
                if (len(char) == 1):
                    processedData['s{}'.format(cont)] = ord(char)
                else:
                    self.logger.warning('Invalid char received: {}'.format(char))

            if (go):
                data = data[data.index(",\"s{}\":".format(cont)) + 1 : len(data)]
                cont += 1
        return processedData
