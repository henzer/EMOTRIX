# -*- coding: utf-8 -*-

import math
import random


def average(data):
    return sum(data) * 1.0 / len(data)


def variance(data):
    avg = average(data)
    var = map(lambda x: (x - avg)**2, data)

    return average(var)


def standard_deviation(data):
    return math.sqrt(variance(data))


def get_std_range(n, m, amplt):
    """
    Gets an approximation of the bounds for the standard deviation
    of a data set whose amplitude is amplt.

    The algorithm generates n random values betwen 0 and amplt. Over
    this n random values, calculates the standard deviation. Then,
    it repeats this process m times and finally, gets the minimun
    and maximum calculated standard deviation.
    """
    deviations = []
    for i in range(0, m):
        data = []
        for i in range(0, n):
            val = random.randint(0, amplt)
            data.append(val)
        deviations.append(standard_deviation(data))

    return min(deviations), max(deviations)
