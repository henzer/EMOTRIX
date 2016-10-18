from abc import ABCMeta, abstractmethod

class InputDeviceInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def connect(self, port, boundrate):
        pass

    @abstractmethod
    def isConnected(self):
        pass

    @abstractmethod
    def getStatus(self):
        pass

    @abstractmethod
    def closePort(self):
        pass

    @abstractmethod
    def startReading(self):
        pass

    @abstractmethod
    def stopReading(self):
        pass