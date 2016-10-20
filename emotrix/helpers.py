# -*- coding: utf-8 -*-

import math

def average(data):
    return sum(data) * 1.0 / len(data)

def variance(data):
    avg = average(data)
    var = map(lambda x: (x - avg)**2, data)

    return average(var)

def standard_deviation(data):
    return math.sqrt(variance(data))
