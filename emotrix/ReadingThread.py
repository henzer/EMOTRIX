import threading

class ReadingThread(threading.Thread):
    input_handler = None
    stop_reading = False

    def __init__(self, threadID, input_handler):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.input_handler = input_handler

    def run(self):
        print "Starting reading thread " + str(self.threadID)
        while not self.stop_reading:
            if (not self.input_handler):
                print "Input handler not defined!"
                return

            try:
                print self.input_handler.readline()
            except Exception, e:
                print "Reading procces raise an exception:"
                print str(e)
                self.stop_reading = True

        print "Exiting reading thread " + str(self.threadID)

    def stopReading(self):
        self.stop_reading = True

    def getStopReading(self):
        return self.stop_reading