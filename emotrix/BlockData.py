# -*- coding: utf-8 -*-
# **********************************************************************************************************************
# Archivo:      BlockData.py
# Proposito:    Esta es la clase que almacena cada uno de los segmentos de las señales EEG.
# Autor:        Henzer Garcia   12538
# **********************************************************************************************************************
class BlockData(object):
    def __init__(self, tag="", time=0, f3=[], f4=[], af3=[], af4=[]):
        self.tag = tag
        self.time = time
        self.f3 = f3
        self.f4 = f4
        self.af3 = af3
        self.af4 = af4
