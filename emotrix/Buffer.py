import threading
import time
import random


class Buffer:
    def __init__(self, buffer_size):
        self.buffer = []
        self.buffer_size = buffer_size
    def insert(self, value):
        self.buffer.append(value)
        if (len(self.buffer) > self.buffer_size):
            self.buffer.pop(0)
    def getAll(self):
        return self.buffer
    def getLast(self):
        return self.buffer[len(self.buffer)-1]

var = Buffer(2)
var.insert(1)
var.insert(2)
var.insert(3)
print var.getAll()
print var.getLast()


