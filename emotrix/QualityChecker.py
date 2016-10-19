import random
import math

def average(data):
    return sum(data) * 1.0 / len(data)

def variance(data):
    avg = average(data)
    var = map(lambda x: (x - avg)**2, data)

    return average(var)

def standard_deviation(data):
    return math.sqrt(variance(data))

def get_deviation_standard_range(n, m, min_value, max_value):
    deviations = []
    for i in range (0, m):
        data = []
        for i in range (0, n):
            val1 = random.randint(0, 15)
            val2 = random.randint(0, 255)
            data.append(get_value_from_chars(val1, val2))
        deviations.append(standard_deviation(data))

    return min(deviations), max(deviations)

def get_value_from_chars(char1, char2):
    binVal1 = "{0:b}".format(char1)
    binVal2 = "{0:b}".format(char2)
    binVal1 = binVal1.rjust(8, '0')
    binVal2 = binVal2.rjust(8, '0')

    return int(binVal1 + binVal2, 2)

# print get_deviation_standard_range(100, 100, 0, 4096)
