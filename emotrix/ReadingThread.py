

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

            # Reading from serial port
            try:
                data = self.input_handler.readline()
                if (not data):
                    continue
            except Exception, e:
                raise Exception("Reading procces raise an exception.\n" + str(e))

            # Data parsing
            try:
                data = self.__processData(data)
                if (not data):
                    continue
            except Exception, e:
                raise Exception("Parsing procces raise an exception. \n" + str(e))

            # Load data in a JSON object
            try:
                dataJson = json.loads(json.dumps(data))
            except Exception, e:
                self.logger.warning("Unable to load data as a json object.\n" + str(e))
                continue

            # Persisting data on DB
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
        """
        This method parses a sample of helmet data.
        A valid sample should look like this:
            {"s1":"KT","s2":"HJ","s3":"LS"}
        
        TODO: Change this line
            char =  sX.decode('unicode-escape')
        """
        self.logger.info('Parsing sample: ' + data)
        # If data were {"s1":"KT","s2":"HJ","s3":"LS"},
        # comments represent first iteration in while loop.
        data = data.strip()

        # data = "s1":"KT","s2":"HJ","s3":"LS"
        data = data[1:-1]

        processedData = {}
        # Look for s2
        cont = 2;
        go = True
        while go:
            try:
                # sX = "s1":"KT"
                sX = data[0 : data.index(",\"s{}\":".format(cont))]
            except Exception, e:
                sX = data
                go = False

            # sX = "KT"
            sX = sX[5 : len(sX)]
            if (sX == 'null'):
                self.logger.warning('Null char received: {}'.format(sX))
            else :
                # sX = KT
                sX = sX[1:-1]
                try:
                    char =  sX.decode('unicode-escape')
                except Exception, e:
                    raise Exception('Unable to decode character ' . sX)
                if (len(char) == 2):
                    processedData['s{}'.format(cont - 1)] = {'char1': ord(char[0]), 'char2': ord(char[1])}
                else:
                    self.logger.warning('Invalid char received: {}'.format(char))

            if (go):
                # data = "s2":"HJ","s3":"LS"
                data = data[data.index(",\"s{}\":".format(cont)) + 1 : len(data)]
                cont += 1

        return processedData
