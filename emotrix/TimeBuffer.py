# -*- coding: utf-8 -*-

import time


class TimeBuffer:
    dataBuffer = None
    timestamps = None
    seconds_back = 0

    def __init__(self, seconds_back):
        self.dataBuffer = []
        self.timestamps = []
        self.seconds_back = seconds_back

    def insert(self, value):
        """
        Insert an element into buffer.
        """
        current_timestamp = time.time()
        self.timestamps.append(current_timestamp)
        self.dataBuffer.append(value)
        if (self.timestamps[0] < (current_timestamp - self.seconds_back)):
            self.dataBuffer.pop(0)
            self.timestamps.pop(0)

    def getAll(self):
        """
        Retrieve all data from buffer.
        """
        return self.dataBuffer

    def getLast(self):
        """
        Retrieve last element from buffer.
        """
        return self.dataBuffer[len(self.dataBuffer) - 1]

    def getLength(self):
        return len(self.dataBuffer)

    def getAllAndClearBuffer(self):
        """
        Retrieve all data and clear buffer.
        """
        data = self.dataBuffer

        self.dataBuffer = []
        self.timestamps = []

        return data
