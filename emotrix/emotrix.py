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
from sklearn import svm
from sklearn.model_selection import cross_val_score
from random import shuffle
from sklearn import preprocessing

#Definicion de la clase.
class Emotrix():

    #Definicion del metodo init
    def __init__(self):
        self.clf = svm.SVC()

    #Metodo utilizado para obtener un bloque/segmento especifico, segun la etiqueta enviada como parametro.
    def get_block(self, blocks, tag):
        for block in blocks:
            if block.tag == tag:
                return block
    #Metodo utilizado para obtener las graficas de la data, para un usuario especifico.
    def graph(self, file_data="user1.csv"):
        raw = RawData(file_data)
        blocks = raw.get_blocks_data()
        sad_block = self.get_block(blocks, tag='SAD')
        happy_block = self.get_block(blocks, tag='HAPPY')
        neutral_block = self.get_block(blocks, tag='NEUTRAL')

        #Preparando lo necesario para mostrar la grafica.
        plt.figure(1, figsize=(20, 10))
        plt.title(u"Señal EEG")
        plt.subplot(411)
        plt.plot(sad_block.f3, 'r')
        plt.plot(happy_block.f3, 'b')
        plt.plot(neutral_block.f3, 'k')
        plt.ylabel("F3")
        plt.subplot(412)
        plt.plot(sad_block.f4, 'r')
        plt.plot(happy_block.f4, 'b')
        plt.plot(neutral_block.f4, 'k')
        plt.ylabel("F4")
        plt.subplot(413)
        plt.plot(sad_block.af3, 'r')
        plt.plot(happy_block.af3, 'b')
        plt.plot(neutral_block.af3, 'k')
        plt.ylabel("AF3")
        plt.subplot(414)
        plt.plot(sad_block.af4, 'r')
        plt.plot(happy_block.af4, 'b')
        plt.plot(neutral_block.af4, 'k')
        plt.ylabel("AF4")
        #Se guarda la grafica como imagen.
        plt.savefig('../../imagenes/sad_EEG.png')
        plt.show()

    #Funcion que define la transformacion que se aplicara a la data, puede ser PSD o no.
    def transf(self, signal):
        #return signal
        return np.abs(signal)**2

    #Funcion para entrenar el algoritmo, recibe como parametro el prefijo del archivo que contiene la data de entrenamiento.
    def training(self, file_data="user"):
        raw = RawData(file_data)
        blocks = raw.get_blocks_data()
        block = self.get_block(blocks, 'SAD')
        block_happy = self.get_block(blocks, 'HAPPY')
        block_neutral = self.get_block(blocks, 'NEUTRAL')

        #Definicion de los parametros para la aplicacion de la tranformada wavelet
        level = 4
        wavelet = 'db4'
        sensors = [raw.f3, raw.f4, raw.af3, raw.af4]

        for i in range(4):
            n = len(sensors[i])
            #Aplicacion de la transformada wavelet.
            cA4, cD4, cD3, cD2, cD1 = pywt.wavedec(sensors[i], wavelet=wavelet, level=level)

            #Extraccion de las 5 bandas de frecuencia.
            delta = pywt.upcoef('a', cA4, wavelet=wavelet, level=level, take=n)
            theta = pywt.upcoef('d', cD4, wavelet=wavelet, level=level, take=n)
            alpha = pywt.upcoef('d', cD3, wavelet=wavelet, level=3, take=n)
            beta = pywt.upcoef('d', cD2, wavelet=wavelet, level=2, take=n)
            gamma = pywt.upcoef('d', cD1, wavelet=wavelet, level=1, take=n)

            #Despligue de la grafica luego de la aplicacion de la transformada
            plt.figure(i, figsize=(20, 10))
            plt.subplot(511)
            plt.plot(self.transf(delta))
            plt.ylabel("delta")
            plt.subplot(512)
            plt.plot(self.transf(theta))
            plt.ylabel("theta")
            plt.subplot(513)
            plt.plot(self.transf(alpha))
            plt.ylabel("alpha")
            plt.subplot(514)
            plt.plot(self.transf(beta))
            plt.ylabel("beta")
            plt.subplot(515)
            plt.plot(self.transf(gamma))
            plt.ylabel("gamma")
            plt.savefig('../../imagenes/F'+str(i+1)+'ANEXOS_'+user+'.png')
        plt.show()

    #Funcion definida para realizar pruebas, durante el entrenamiento.
    def getAccuracy(self, file_data="user"):
        #Se leen los archivos con toda la data.
        raw = RawData(file_data, several_files=True)
        #Se obtiene la data, devidida por segmentos.
        blocks = raw.get_blocks_data()
        shuffle(blocks)
        c = [0, 0, 0]
        for block in blocks:
            if block.tag == 'HAPPY':
                c[0] += 1
            if block.tag == 'SAD':
                c[1] += 1
            if block.tag == 'NEUTRAL':
                c[2] += 1
        #Se imprime el numero de muestras
        print '################ NUMERO DE MUESTRAS ###############'
        print str(c[0]) + ' HAPPY'
        print str(c[1]) + ' SAD'
        print str(c[2]) + ' NEUTRAL'

        #Se aplica una sanitizacion de los datos, antes de implementar SVM
        result = self.feature_extraction(blocks)
        X = result['features']
        y = result['tags']
        scaler = preprocessing.StandardScaler().fit(X)
        normalize = preprocessing.Normalizer().fit(X)
        X = scaler.transform(X)
        X = normalize.transform(X)

        #Se realizar CROSS VALIDATION utilizando una variación de parametros.
        for c in np.arange(0.001, 1, 0.5):
            print "################   C=" + str(c) + "   #########################"
            self.clf = svm.SVC(kernel='linear', C=c)
            scores = cross_val_score(self.clf, X, y, cv=5, verbose=1)
            print ("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
        for c in np.arange(1, 100, 10):
            print "################   C=" + str(c) + "   #########################"
            self.clf = svm.SVC(kernel='linear', C=c)
            scores = cross_val_score(self.clf, X, y, cv=5, verbose=1)
            print ("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
        for c in np.arange(200, 2000, 200):
            print "################   C=" + str(c) + "   #########################"
            self.clf = svm.SVC(kernel='linear', C=c)
            scores = cross_val_score(self.clf, X, y, cv=5, verbose=1)
            print ("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

    #Funcion definida para la extraccion de caracteristicas de las señales EEG.
    def feature_extraction(self, blocks):
        print 'Feature extraction'
        result = {
            "features": [],
            "tags": []
        }
        i = 0
        n = len(blocks)
        level = 4
        wavelet = 'db4'
        for block in blocks:
            feature = []
            electrodes = [block.f3, block.f4, block.af3, block.af4]
            for electrode in electrodes:
                #Se obtienen las caracteristicas en el dominio del tiempo, media y desviacion estandar.
                feature.append(np.mean(electrode))
                feature.append(np.std(electrode))

                size = len(electrode)
                #Se aplica la transformada wavelet, para la separacion de las bandas de frecuencia.
                wavelet_result = pywt.wavedec(electrode, wavelet='db4', level=level)
                alpha = pywt.upcoef('d', wavelet_result[2], wavelet='db4', level=3, take=size)
                beta = pywt.upcoef('d', wavelet_result[3], wavelet='db4', level=2, take=size)
                gamma = pywt.upcoef('d', wavelet_result[4], wavelet='db4', level=1, take=size)

                #Se obtienen las caracteristicas en el dominio de la frecuencia, media y desviacion estandar.
                #ALPHA
                feature.append(np.mean(self.transf(alpha)))
                feature.append(np.std(self.transf(alpha)))
                #BETA
                feature.append(np.mean(self.transf(beta)))
                feature.append(np.std(self.transf(beta)))
                #GAMMA
                feature.append(np.mean(self.transf(gamma)))
                feature.append(np.std(self.transf(gamma)))

            result['features'].append(feature)
            result['tags'].append(block.tag)
        return result

    #Devuelve un listado de las emociones que el SDK de EMOTRIX puede determinar.
    def get_available_emotions(self):
        pass

    #Obtiene la version del SDK de EMOTRIX.
    def get_version(self):
        pass

    #Obtiene la informacion en bruto de las señales EEG
    def get_raw_data(self):
        pass

    #Determina la emocion predominante en el sujeto.
    def get_current_emotion(self):
        pass

    #Obtiene una lista con las emociones actuales del sujeto.
    def get_current_emotions(self):
        pass

    #Obtiene la informacion proporcionada por la pulsera.
    def get_hand_position(self):
        pass

    #Obtiene el ritmo cardiaco del sujeto
    def get_heart_beats(self):
        pass

    #Obtiene una lista con los electrodos que utiliza EMOTRIX.
    def get_electrodes(self):
        pass


e = Emotrix()
#e.pruebas(file_data='user')
e.training(file_data='user20.csv', user="user20")
#e.graph()