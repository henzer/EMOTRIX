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
        current_timestamp = time.time()
        self.timestamps.append(current_timestamp)
        self.dataBuffer.append(value)
        if (self.timestamps[0] < (current_timestamp - self.seconds_back)):
            self.dataBuffer.pop(0)
            self.timestamps.pop(0)

    def getAll(self):
        return self.dataBuffer

    def getLast(self):
        return self.dataBuffer[len(self.dataBuffer) - 1]

    def dataBetAndEmptyBuffer(self):
        data = self.dataBuffer

        self.dataBuffer = []
        self.timestamps = []

        return data
