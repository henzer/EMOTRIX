# -*- coding: utf-8 -*-
# **********************************************************************************************************************
# Archivo:      RawData.py
# Proposito:    Esta es la clase que obtiene la informacion en bruto, a partir de un archivo de texto.
#               Contiene todas las funciones para leer el archivo, dividir la data y hacer algunas transformaciones.
# Autor:        Henzer Garcia   12538
# **********************************************************************************************************************
import csv
import numpy as np
from BlockData import BlockData

class RawData(object):

    #En la funcion init, se lee el archivo/archivos pasados como parametros y see informacion en arreglos de python.
    def __init__(self, file_data="prueba", several_files=False, total=20):

        #Se definen los arreglos donde se almacenara la informacion
        self.file_name = file_data
        self.time = np.array([])
        self.f3 = np.array([])
        self.f4 = np.array([])
        self.af3 = np.array([])
        self.af4 = np.array([])
        self.tag = np.array([])
        self.blocks = []

        #Proceso para leer varios archivos al mismo tiempo.
        if several_files:
            for i in range(1, total+1):
                try:
                    file_name = file_data + str(i) + '.csv'
                    file_to_read = open(file_name, "rb")
                    self.read_file(file_to_read, ignore_tags=["NOPE", "RELAX", ""])
                    file_to_read.close()
                except:
                    file_to_read.close()
                    print 'No encontrado: ' + file_data + str(i) + '.csv'
        else:
            file_to_read = open(file_data, "rb")
            self.read_file(file_to_read, ignore_tags=["NOPE", "RELAX"])
            file_to_read.close()

    #Funcion especifica que lee el archivo de texto y luego la almacena en arreglos de python.
    def read_file(self, file_to_read, ignore_tags=[]):
        reader = csv.reader(file_to_read, delimiter='\t', quotechar='"')
        time, f3, f4, af3, af4, tag = [], [], [], [], [], []
        for row in reader:
            if len(row) == 6:
                if row[5] in ignore_tags:
                    continue
                f3_value = int(row[1].split(':')[1].split(',')[1])
                f3_quality = int(row[1].split(':')[1].split(',')[0])
                f4_value = int(row[2].split(':')[1].split(',')[1])
                f4_quality = int(row[2].split(':')[1].split(',')[0])
                af3_value = int(row[3].split(':')[1].split(',')[1])
                af3_quality = int(row[3].split(':')[1].split(',')[0])
                af4_value = int(row[4].split(':')[1].split(',')[1])
                af4_quality = int(row[4].split(':')[1].split(',')[0])
                #Filtro
                if min(f3_quality, f4_quality, af3_quality, af4_quality) >= 10:
                    time.append(int(row[0]))
                    f3.append(f3_value)
                    f4.append(f4_value)
                    af3.append(af3_value)
                    af4.append(af4_value)
                    tag.append(row[5])

        #Los arreglos se transforman a arreglos de numpy, para que sea mas eficiente.
        self.time = np.append(self.time, np.array(time))
        self.tag = np.append(self.tag, np.array(tag))
        self.f3 = np.append(self.f3, np.array(f3))
        self.f4 = np.append(self.f4, np.array(f4))
        self.af3 = np.append(self.af3, np.array(af3))
        self.af4 = np.append(self.af4, np.array(af4))


    #Fundion que divide la data en segmentos.
    def get_divided_data(self):
        f3, f4, af3, af4, time, tag = [], [], [], [], [], []
        before = self.tag[0]
        lower_limit = 0
        i = 0
        for t in np.append(self.tag, 'fin'):
            if t != before:
                previous_second = self.time[lower_limit]
                for second in self.time[lower_limit:i]:
                    if second != previous_second:
                        break
                    lower_limit += 1
                f3.append(self.f3[lower_limit:i])
                f4.append(self.f4[lower_limit:i])
                af3.append(self.af3[lower_limit:i])
                af4.append(self.af4[lower_limit:i])
                time.append(self.time[lower_limit:i])
                tag.append(self.tag[lower_limit:i])
                lower_limit = i
                before = t
            i += 1
        # print time
        return time, tag, f3, f4, af3, af4

    #Metodo para obtener los datos en bloques de 1 segundo.
    def get_blocks_data(self):
        self.blocks = []
        before = self.tag[0]
        lower_limit_i = 0
        i = 0
        size = 256
        overlap = 20
        for t in np.append(self.tag, 'fin'):
            if t != before:
                previous_second = self.time[lower_limit_i]
                for j in range(lower_limit_i, i-128, overlap):
                    #Se descarta el primer segundo de cada bloque
                    if j != lower_limit_i:
                        block = BlockData(tag=before, time=self.time[j], f3=self.f3[j:j+size], f4=self.f4[j:j+size], af3=self.af3[j:j+size], af4=self.af4[j:j+size])
                        self.blocks.append(block)
                lower_limit_i = i
                before = t
            i += 1
        return self.blocks

    #Metodo get para el arreglo F3
    def get_f3(self):
        return self.f3

    # Metodo get para el arreglo F4
    def get_f4(self):
        return self.f4
