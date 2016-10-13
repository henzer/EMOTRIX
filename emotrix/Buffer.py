import threading
import time
import random


buffer = []
buffer_size = 100
class myThread (threading.Thread):
    def __init__(self, threadID, name, delay, writer):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.delay = delay
        self.writer = writer
    def run(self):
        #print "Starting " + self.name
        if (self.writer == True):
            execute(self.name, self.delay)

        if (self.writer == False and len(buffer) != 0):
            #time.sleep(self.delay)
            print "Buffer Readed " + str(buffer[len(buffer)-1])
        #print "Exiting " + self.name
        print 

def execute(threadName, delay):
    #print 
    #time.sleep(delay)
    buffer.append(random.randint(0,10))
    if (len(buffer) > buffer_size):
        buffer.pop(0)
    #print "Executing " + str(threadName) + " " + str(buffer)

i = 0
cont = 0
tiempo1 = time.clock()
while i < 300 :
    # Create new threads
    threadReader = myThread(i, "Reader Thread-"+str(i), 1, False)
    threadWriter = myThread(i, "Writer Thread-"+str(i), 4, True)
    

    # Start new Threads
    threadWriter.start()
    threadReader.start()
    #Wait to finish last thread
    threadWriter.join()
    threadReader.join()

    i +=1
    cont +=1

print "Exiting Main Thread"
print cont
print time.clock()-tiempo1
