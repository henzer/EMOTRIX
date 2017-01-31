# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from RawData import RawData
from HeadsetEmotiv import HeadsetEmotiv
from emotrix import Emotrix
from BlockData import BlockData
from TimeBuffer import TimeBuffer
from Bracelet import Bracelet
import logging
import time

import Tkinter

class Main(object):
    def __init__(self):
        #Creacion del objeto HeadsetEmotiv
        time = 5

        self.buffer_emotion = TimeBuffer(time)
        self.e = Emotrix()
        self.e.training2()

        print "Iniciando la lectura desde Emotiv"
        self.he = HeadsetEmotiv(time)
        self.he.start()



        self.root = Tkinter.Tk()
        self.root.title('EMOTRIX')
        self.boton1 = Tkinter.Button(self.root, text="EMOTRIX", command=self.show_emotrix, width=50, height=5)
        self.boton2 = Tkinter.Button(self.root, text="EMOTIV", command=self.show_emotiv, width=50, height=5)
        self.boton3 = Tkinter.Button(self.root, text="PULSERA", command=self.show_pulsera, width=50, height=5)
        self.boton4 = Tkinter.Button(self.root, text="DETECTAR", command=self.show_emotion, width=50, height=5)
        self.boton1.grid(row=1, column=1)
        self.boton2.grid(row=2, column=1)
        self.boton3.grid(row=3, column=1)
        self.boton4.grid(row=4, column=1)
        self.root.mainloop()

    def show_emotiv(self):
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(1, 1, 1)
        ani = animation.FuncAnimation(self.fig, self.animate, interval=10)
        plt.show()

    def show_emotrix(self):
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(1, 1, 1)
        ani = animation.FuncAnimation(self.fig, self.animate, interval=10)
        plt.show()

    def show_pulsera(self):
        print "Iniciando Matias"
        puerto = 'COM3'
        self.bracelet = Bracelet(logging.INFO)
        try:
            self.bracelet.connect(puerto, 115200)
        except Exception, e:
            raise e
        self.bracelet.startReading(persist_data=False)
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(1, 1, 1)
        ani = animation.FuncAnimation(self.fig, self.animate_pulsera, interval=10)
        plt.show()

    def show_emotion(self):
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(1, 1, 1)
        ani = animation.FuncAnimation(self.fig, self.animate_emotion, interval=10)
        plt.show()

    def animate_emotion(self, i):
        b = BlockData(f3=self.he.f3.getAll(), f4=self.he.f4.getAll(), af3=self.he.af3.getAll(), af4=self.he.af4.getAll())
        result = self.e.detect_emotion(b)
        print result
        if result[0]=='HAPPY':
            self.buffer_emotion.insert(-50)
        elif result[0]=='SAD':
            self.buffer_emotion.insert(50)
        else:
            self.buffer_emotion.insert(0)

        self.ax1.clear()
        self.ax1.set_title("Deteccion de emociones");
        self.ax1.set_xlabel('Tiempo');
        self.ax1.set_ylabel('Emociones');
        self.ax1.text(3,55,"Felicidad", fontsize=15)
        self.ax1.text(3, 0, "Neutral", fontsize=15)
        self.ax1.text(3, -60, "Tristeza", fontsize=15)
        self.ax1.set_ylim([-100, 100])
        self.ax1.plot(self.buffer_emotion.getAll(), marker="o")

    def animate(self, i):

        self.ax1.clear()
        self.ax1.set_title("Electrodos F3, F4, AF3, AF4");
        self.ax1.set_xlabel('Tiempo')
        self.ax1.set_ylabel('Amplitud')

        self.ax1.plot(self.he.f3.getAll(), "r")
        self.ax1.plot(self.he.f4.getAll(), "b")
        self.ax1.plot(self.he.af3.getAll(), "y")
        self.ax1.plot(self.he.af4.getAll(), "k")

    def animate_pulsera(self, i):
        self.ax1.clear()
        self.ax1.set_title("Brazalete");
        self.ax1.set_xlabel('Tiempo');
        self.ax1.set_ylabel('Amplitud');
        self.ax1.set_ylim([300, 800]);
        self.ax1.plot(self.bracelet.device_buffer.getAll(), "r")

    def stop(self):
        plt.close()



main = Main()
# main.show()

