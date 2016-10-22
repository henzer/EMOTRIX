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
        return self.buffer[len(self.buffer) - 1]

    def getAndEmptyBuffer(self):
        data = self.buffer
        self.buffer = []

        return data
