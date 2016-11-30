from abc import ABCMeta, abstractmethod


class InputDeviceInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def connect(self, port, baudrate):
        pass

    @abstractmethod
    def isConnected(self):
        pass

    @abstractmethod
    def startReading(self, persist_data=False):
        pass

    @abstractmethod
    def stopReading(self):
        pass

    @abstractmethod
    def getStatus(self):
        pass

    @abstractmethod
    def getCurrentData(self):
        pass

    @abstractmethod
    def closePort(self):
        pass
