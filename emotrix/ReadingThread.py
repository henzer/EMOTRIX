import threading
import logging
import json
import datetime
import time

class ReadingThread(threading.Thread):
    NUMBER_OF_SENSORS = 4
    MAX_VALUE = 4095
    input_handler = None
    stop_reading = False
    persist_data = False
    db = None
    logger = None

    def __init__(self, input_handler, db, persist_data):
        threading.Thread.__init__(self)

        self.setName("Helmet data reader")
        self.input_handler = input_handler
        self.persist_data = persist_data
        self.db = db

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def run(self):
        if (not self.input_handler):
            raise Exception("Input handler not defined!")

        if (self.persist_data and not self.db):
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
                data = self.__parseData(data)
                if (not data):
                    continue
            except Exception, e:
                raise Exception("Parsing procces raise an exception. \n" + str(e))

            # Process data
            checksum = data.pop('checksum')
            data = self.__processValues(data)

            if (not data):
                continue

            # Persisting data on DB
            if (not self.persist_data):
                continue

            # Load data into a JSON object
            try:
                dataJson = json.loads(json.dumps(data))
            except Exception, e:
                self.logger.warning("Unable to load data as a json object.\n" + str(e))
                continue

            try:
                self.db.helmet_data.insert_one(dataJson)
            except Exception, e:
                raise Exception("Persisting helmet data raise an exception.\n" + str(e))

        self.logger.info("Exiting thread: " + self.getName())

    def stopReading(self):
        self.stop_reading = True

    def __parseData(self, data):
        """
        This method parses a sample of helmet data.
        A valid sample should look like this:
            {s1:KT,s2:HJ,s3:LS,s4:KL,cs:4253}
        
        TODO: Change this line
            char =  sX.decode('unicode-escape')
        """
        self.logger.info('Parsing sample: ' + data)
        # If data were {s1:KT,s2:HJ,s3:LS,s4:KL,cs:4253},
        # comments represent first iteration in while loop.
        data = data.strip()

        # (6 * NUMBER_OF_SENSORS) + 2 curly brackets - last coma
        if (len(data) < ((6 * self.NUMBER_OF_SENSORS) + 1)):
            self.logger.warning('Incomplete data received: ' + data)

            return {}

        # data = s1:KT,s2:HJ,s3:LS,s4:KL,cs:4253
        data = data[1:-1]

        try:
            # checksum = ,cs:4253
            checksum = data[data.index(",cs:") : len(data)]
            checksum = checksum[4 : len(checksum)]
        except Exception, e:
            raise Exception('Error while getting checksum value.\n' + str(e))

        # data = s1:KT,s2:HJ,s3:LS,s4:KL
        data = data[0:data.index(",cs:")]

        processedData = {}
        # Look for s2
        cont = 2;
        go = True
        while go:
            try:
                # sX = s1:KT
                sX = data[0 : data.index(",s{}:".format(cont))]
            except Exception, e:
                sX = data
                go = False

            # sX = KT
            sX = sX[3 : len(sX)]
            if (sX == 'null'):
                self.logger.warning('Null char received: {}'.format(sX))
            else :
                try:
                    char =  sX.decode('unicode-escape')
                except Exception, e:
                    raise Exception('Unable to decode character ' + sX)
                if (len(char) == 2):
                    processedData['s{}'.format(cont - 1)] = {'char1': ord(char[0]), 'char2': ord(char[1])}
                else:
                    self.logger.warning('Invalid char received: {}'.format(char))

            if (go):
                # data = s2:HJ,s3:LS,s4:KL,cs:4253
                data = data[data.index(",s{}:".format(cont)) + 1 : len(data)]
                cont += 1

        processedData['checksum'] = checksum

        return processedData

    def __processValues(self, data):
        processedValues = {}
        # Assume that all were taken at the same time.
        timestamp = str(time.time())
        for key in data:
            binVal1 = "{0:b}".format(data[key]['char1'])
            binVal2 = "{0:b}".format(data[key]['char2'])
            binVal1 = binVal1.rjust(8, '0')
            binVal2 = binVal2.rjust(8, '0')
            realValue = int(binVal1 + binVal2, 2)

            # if (realValue > self.MAX_VALUE):
            #     self.logger.warning('Too large value received. {}:{}'.format(key, data[key]))
            #     return {}

            # TODO: Implement process for quality
            processedValues[key] = {'value': realValue, 'quality': 15, 'readed_at': timestamp}

        return processedValues

    def __assertChecksum(self, data, checksum):
        suma = 0
        for key in data:
            suma += data[key]['char1'] + data[key]['char2']

        if (checksum == suma):
            return True

        return False