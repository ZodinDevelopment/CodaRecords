import numpy as np 
import sys
import time



def wavespace(duration, sample_rate=48000):

    return np.linspace(0, 2 * duration * np.pi, int(duration * sample_rate))


def phasespace(duration, sample_rate=48000, factor=1):
    return np.logspace(0, 1, int(duration * sample_rate)) * factor


