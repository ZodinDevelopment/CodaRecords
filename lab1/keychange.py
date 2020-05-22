import numpy as np
import sounddevice as sd
import time


def sine_wave(f):
    y = np.sin(f*x)
    return y


def change_note(frequency, steps):
    f = frequency * (2**(steps / 12.0))
    return f


freq = 220.0
wave_data = sine_wave(change_note(freq, 2))


