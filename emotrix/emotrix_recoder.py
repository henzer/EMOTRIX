# -*- coding: utf-8 -*-
# **********************************************************************************************************************
# Archivo:      emotrix_recorder.py
# Proposito:    Este archivo es el encargado de leer la data directamente desde el EMOTIV, y guardarla en un archivo csv
#               para luego hacer un preprocesamiento de ella.
# Autor:        Henzer Garcia   12538
# **********************************************************************************************************************

import platform
import csv
import time
from emokit.emotiv import Emotiv
import gevent


class EmotrixRecoder(object):

    #El metodo init define algunos parametros por defecto, para almacenar las lecturas del EMOTIV
    def __init__(self):
        self.sequence = ['happy', 'neutral', 'sad', 'happy', 'neutral', 'sad', 'happy', 'neutral', 'sad', 'happy', 'neutral', 'sad','happy', 'neutral', 'sad','happy', 'neutral', 'sad','happy', 'neutral', 'sad']
        self.time_block = 7
        self.num_blocks = len(self.sequence)
        self.filename = 'data.csv'

    #Metodo para iniciar la grabacion de las lecturas de las señales EEG.
    def start(self, sequence=None, time_block=7, filename='data.csv'):
        self.time_block = time_block
        self.filename = filename
        #Se define el objeto EMOTIV, utilizando la libreria EMOKIT
        headset = Emotiv()
        gevent.spawn(headset.setup)
        gevent.sleep(0)
        print("Serial Number: %s" % headset.serial_number)

        if sequence is not None:
            self.sequence = sequence
            self.num_blocks = len(self.sequence)
        i = 0
        cont_block = 0
        cont_seconds = 0
        temp_t = 0
        tag = self.sequence[0]

        #Se define el escritor de las lecturas en el archivo CSV
        writer = csv.writer(open(self.filename, 'w'), delimiter='\t', quotechar='"')
        try:
            t0 = time.time()
            while True:
                t = int(time.time()-t0)
                #t = int(time.time())
                if temp_t != t:
                    cont_seconds += 1

                if cont_seconds > self.time_block:
                    cont_seconds = 0
                    cont_block += 1
                    if cont_block == self.num_blocks:
                        headset.close()
                        break
                    else:
                        tag = self.sequence[cont_block]

                # Se obtiene el paquete de datos, utilizando EMOKIT
                packet = headset.dequeue()

                # Se construye la informacion a guardar
                row = [str(t),
                       "F3:" + str(packet.sensors['F3']['quality']) + "," + str(packet.sensors['F3']['value']),
                       "F4:" + str(packet.sensors['F4']['quality']) + "," + str(packet.sensors['F4']['value']),
                       "AF3:" + str(packet.sensors['AF3']['quality']) + "," + str(packet.sensors['AF3']['value']),
                       "AF4:" + str(packet.sensors['AF4']['quality']) + "," + str(packet.sensors['AF4']['value']),
                       tag]
                # Se exporta a csv
                writer.writerow(row)
                print row
                temp_t = t
                gevent.sleep(0)
        except KeyboardInterrupt:
            headset.close()
        finally:
            headset.close()
        i += 1


#Se inicia el proceso de la grabacion, se define la secuencia y el tiempo de cada estimulo.
er = EmotrixRecoder()
er.start(['NOPE','RELAX', 'RELAX', 'RELAX', 'RELAX',
          'HAPPY', 'NEUTRAL', 'SAD', 'NEUTRAL',
          'HAPPY', 'NEUTRAL', 'SAD', 'NEUTRAL',
          'HAPPY', 'NEUTRAL', 'SAD', 'NEUTRAL',
          'HAPPY', 'NEUTRAL', 'SAD', 'NEUTRAL',
          'HAPPY', 'NEUTRAL', 'SAD', 'NEUTRAL',
          'HAPPY', 'NEUTRAL', 'SAD', 'NEUTRAL',
          'HAPPY', 'NEUTRAL', 'SAD', 'NEUTRAL',
          'HAPPY', 'NEUTRAL', 'SAD', 'NEUTRAL',
          'HAPPY', 'NEUTRAL', 'SAD', 'NEUTRAL',
          'HAPPY', 'NEUTRAL', 'SAD', 'NEUTRAL',
          ], 4, 'user21.csv')
