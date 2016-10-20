NUMBER_OF_SENSORS = 4
MAX_VALUE = 4095

BUFFER_SIZE = 100
BRACELET_BUFFER_SIZE = 100

"""
These amplitudes can be improved by performing actual tests and analyzing
the behavior of the signals.
"""
NO_SIGNAL_MAX_AMPLITUDE = 10
BAD_SIGNAL_MAX_AMPLITUDE = 58
GOOD_SIGNAL_MAX_AMPLITUDE = 4096

BRACELET_NO_SIGNAL_MAX_AMPLITUDE = 10
BRACELET_BAD_SIGNAL_MAX_AMPLITUDE = 500
BRACELET_GOOD_SIGNAL_MAX_AMPLITUDE = 65535

"""
Actually, constants related with minimum and maximum standard deviation,
are calculated when program start using helpers.get_std_range() method.
However, for best results, these values must be calculated by performing
real tests and using helpers.get_std_range() method too.

The values you see here represents nothing.
"""

NO_SIGNAL_MIN_STD = 2
NO_SIGNAL_MAX_STD = 4

BAD_SIGNAL_MIN_STD = 50
BAD_SIGNAL_MAX_STD = 300

GOOD_SIGNAL_MIN_STD = 900
GOOD_SIGNAL_MAX_STD = 1500

BRACELET_NO_SIGNAL_MIN_STD = 2
BRACELET_NO_SIGNAL_MAX_STD = 4

BRACELET_BAD_SIGNAL_MIN_STD = 115
BRACELET_BAD_SIGNAL_MAX_STD = 170

BRACELET_GOOD_SIGNAL_MIN_STD = 15000
BRACELET_GOOD_SIGNAL_MAX_STD = 22000

# Bounds for heart rate
MAX_HEART_RATE = 200
MIN_HEART_RATE = 150
