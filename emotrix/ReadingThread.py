import threading

class ReadingThread(threading.Thread):
    input_handler = None
    stop_reading = False
    db = None

    def __init__(self, threadID, input_handler, db):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.input_handler = input_handler

    # TODO: Test persisting process
    def run(self):
        if (not self.input_handler):
            print "Input handler not defined!"
            return

        if (not self.db):
            print "Mongo db not defined!"
            return

        print "Starting reading thread " + str(self.threadID)
        while not self.stop_reading:
            data = ""

            try:
                data = self.input_handler.readline()
                print data
            except Exception, e:
                print "Reading procces raise an exception:"
                print str(e)
                return

            dataJson = []
            try:
                dataJson = json.loads(data)
            except Exception, e:
                print "Converting data to JSON format raise an exception:"
                print str(e)
                return

            try:
                dataJson['readed_at'] = datetime.datetime.now()
                self.db.helmet_data.insert_one(dataJson)
            except Exception, e:
                print "Persisting helmet data raise an exception:"
                print str(e)
                return
            
            

        print "Exiting reading thread " + str(self.threadID)

    def stopReading(self):
        self.stop_reading = True

    def getStopReading(self):
        return self.stop_reading
