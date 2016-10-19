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
    data = []
    deviations = []
    for i in range (0, m):
        for i in range (0, n):
            val = random.randint(min_value, max_value)
            data.append(val)
        deviations.append(standard_deviation(data))

    return min(deviations), max(deviations)

print get_deviation_standard_range(100, 100, 0, 4096)
