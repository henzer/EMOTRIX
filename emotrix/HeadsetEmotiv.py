# -*- coding: utf-8 -*-
# **********************************************************************************************************************
# Archivo:      HeadsetEmotiv.py
# Proposito:
# Autor:        Henzer Garcia   12538
# **********************************************************************************************************************
from TimeBuffer import TimeBuffer
from emokit.emotiv import Emotiv
from threading import Thread
import threading

import gevent

class HeadsetEmotiv():

    def __init__(self, time):
        self.f3 = TimeBuffer(time)
        self.f4 = TimeBuffer(time)
        self.af3 = TimeBuffer(time)
        self.af4 = TimeBuffer(time)

        self.reader = ThreadReaderEmotiv({
            'F3': self.f3,
            'F4': self.f4,
            'AF3': self.af3,
            'AF4': self.af4
        })

    def start(self):
        self.reader.start()



class ThreadReaderEmotiv(Thread):
    def __init__(self, input):
        threading.Thread.__init__(self)
        self.headset = Emotiv()
        self.f3 = input['F3']
        self.f4 = input['F4']
        self.af3 = input['AF3']
        self.af4 = input['AF4']

    def run(self):
        self.headset = Emotiv()
        gevent.spawn(self.headset.setup)
        gevent.sleep(0)
        print("Serial Number: %s" % self.headset.serial_number)
        while True:
            packet = self.headset.dequeue()
            self.f3.insert(packet.sensors['F3']['value'])
            self.f4.insert(packet.sensors['F4']['value'])
            self.af3.insert(packet.sensors['AF3']['value'])
            self.af4.insert(packet.sensors['AF4']['value'])
            gevent.sleep(0)
