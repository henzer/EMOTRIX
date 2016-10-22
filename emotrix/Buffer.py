import time


class Buffer:
    def __init__(self, buffer_size):
        self.buffer = []
        self.buffer_time = []
        self.buffer_size = buffer_size

    def insert(self, value):
        self.buffer.append(value)
        self.insertTimeStamp()
        if (len(self.buffer) > self.buffer_size):
            self.buffer.pop(0)
            self.buffer_size.pop(0)

    def getAll(self):
        return self.buffer

    def getLast(self):
        return self.buffer[len(self.buffer) - 1]

    def getAndEmptyBuffer(self):
        data = self.buffer
        self.buffer = []

        return data

    def insertTimeStamp(self):
        timestamp = str(time.time())
        seconds = timestamp[0: timestamp.index(".")]
        self.buffer_time.append(seconds)
