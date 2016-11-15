# -*- coding: utf-8 -*-

HEADSET_NUMBER_OF_SENSORS = 4
HEADSET_EEG_MAX_VALUE = 4095
BRACELET_BPM_MAX_VALUE = 255
BRACELET_EMG_MAX_VALUE = 65535

HEADSET_MIN_BUFFER_SIZE = 70
BRACELET_MIN_BUFFER_SIZE = 300

HEADSET_CENTER = 2048
BRACELET_CENTER = 32768

"""
These amplitudes can be improved by performing actual tests and analyzing
the behavior of the signals.
"""
HEADSET_NO_SIGNAL_MAX_AMPLITUDE = 10
HEADSET_GOOD_SIGNAL_MAX_AMPLITUDE = 4095

BRACELET_NO_SIGNAL_MAX_AMPLITUDE = 10
BRACELET_GOOD_SIGNAL_MAX_AMPLITUDE = 65535
BRACELET_BPM_NO_SIGNAL_MAX_AMPLITUDE = 10

"""
Actually, constants related with minimum and maximum standard deviation,
are calculated when program start using helpers.get_std_range() method.
However, for best results, these values must be calculated by performing
real tests and using helpers.get_std_range() method too.

The values you see here represents nothing.
"""
HEADSET_GOOD_SIGNAL_MIN_VAR = 900
HEADSET_GOOD_SIGNAL_MAX_VAR = 1500

BRACELET_GOOD_SIGNAL_MIN_VAR = 15000
BRACELET_GOOD_SIGNAL_MAX_VAR = 22000

# Bounds for heart rate
MAX_HEART_RATE = 200
MIN_HEART_RATE = 75

# Seconds back for buffer
HEADSET_TIME_WINDOW_SIZE = 1
BRACELET_TIME_WINDOW_SIZE = 1
