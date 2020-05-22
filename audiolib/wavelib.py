import numpy as np
import sounddevice as sd
import wavio
import wave
import time

from audiolib.arrays import wavespace, phasespace



def sinewave(f, x):
    return np.sin(f * x)


def triangle(f, x):
    return 2 / np.pi * np.arcsin(np.sin(f * x))


def sawtooth(f, x):
    return -2 / np.pi * np.arctan(np.tan(np.pi / 2 - (x * np.pi / (1 / f * 2 * np.pi))))


def square(f, x):
    a = np.sin(f * x) / 2 + 0.5
    d = np.round(a) - 0.5
    return d



WAVES = {
        'sine': sinewave,
        'triangle': triangle,
        'sawtooth': sawtooth,
        'square': square
}



def sine_modulation(frequency, duration, fm, level=0.3, sample_rate=48000, carrier='sine'):

    x = wavespace(duration, sample_rate)

    ramp = phasespace(duration, sample_rate)

    phase_function = WAVES.get(carrier)
    mod = phase_function(fm, x)

    return np.sin(frequency * x + ramp * mod) * level


def triangle_modulation(frequency, duation, fm, level=0.3, sample_rate=48000, carrier='sine'):

    x = wavespace(duration, sample_rate)

    ramp = phasespace(duration, sample_rate)

    phase_function = WAVES.get(carrier)
    mod = phase_function(fm, x)

    return 2 / np.pi * np.arcsin(np.sin(frequency * x + ramp * mod)) * level

def sawtooth_modulation(frequency, duration, fm, level=0.3, sample_rate=48000, carrier='sine'):

    x = wavespace(duration, sample_rate)

    ramp = phasespace(duration, sample_rate)

    phase_function = WAVES.get(carrier)
    mod = phase_function(fm, x)

    return -2 / np.pi * np.arctan(np.tan(np.pi / 2 - (x * np.pi / (1 * frequency * 2 * np.pi + ramp * mod)))) * level



def square_modulation(frequency, duration, fm, level=0.3, sample_rate=48000, carrier='sine'):
    x = wavespace(duration, sample_rate)

    ramp = phasespace(duration, sample_rate)

    phase_function = WAVES.get(carrier)
    mod = phase_function(fm, x)

    a = np.sin(frequency * x + ramp * mod) / 2 + 0.5
    d = np.round(a) - 0.5

    return d * level


def play(wave, duration, sample_rate):

    sd.play(wave, sample_rate)
    time.sleep(duration)
    sd.stop()



