# -*- coding: utf-8 -*-
# **********************************************************************************************************************
# Archivo:      emotrix.py
# Proposito:    Este archivo es el encargado de gestionar todas las llamadas al API, para trabajar con EMOTRIX
# Autor:        Henzer Garcia   12538
# **********************************************************************************************************************
from RawData import RawData
import numpy as np
import matplotlib.pyplot as plt
import pywt


class Emotrix():

    def __init__(self):
        pass

    def training(self, file_data="data.csv"):
        raw = RawData(file_data)
        x, F3, F4, AF3, AF4, tag = raw.get_divided_data()

        level = 4
        wavelet = 'db4'

        cA4, cD4, cD3, cD2, cD1 = pywt.wavedec(F3[1], 'db4', level=level)

        delta = pywt.upcoef('d', cA4, 'db4', level=level)
        theta = pywt.upcoef('d', cD4, 'db4', level=level)
        alpha = pywt.upcoef('d', cD3, 'db4', level=level)
        beta = pywt.upcoef('d', cD2, 'db4', level=level)
        gamma = pywt.upcoef('d', cD1, 'db4', level=level)

        print 'Tamanios'
        print len(F3)
        for f in F3:
            print len(f)
        print "************"

        print len(cA4)
        print len(cD4)
        print len(cD3)
        print len(cD2)
        print len(cD1)
        print "************"
        print len(delta)
        print len(theta)
        print len(alpha)
        print len(beta)
        print len(gamma)

        plt.figure(1)
        plt.subplot(511)
        plt.plot(delta)
        plt.ylabel("delta")
        plt.subplot(512)
        plt.plot(theta)
        plt.ylabel("theta")
        plt.subplot(513)
        plt.plot(alpha)
        plt.ylabel("alpha")
        plt.subplot(514)
        plt.plot(beta)
        plt.ylabel("beta")
        plt.subplot(515)
        plt.plot(gamma)
        plt.ylabel("gamma")
        plt.show()
        print 'hola'


    def get_emotion(self):
        pass

e = Emotrix()
e.training(file_data='henzer.csv')
