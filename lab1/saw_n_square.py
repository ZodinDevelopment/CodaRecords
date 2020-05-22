import numpy as np
import sounddevice as sd
import time
import matplotlib.pyplot as plt
plt.style.use('dark_background')


def sawtooth():
    return -2 / np.pi * np.arctan(
        np.tan(np.pi / 2 - (x * np.pi / (1 / frequency0 * 2 * np.pi))))


def square():
    a = np.sin(frequency0 * x) / 2 + 0.5
    d = np.round(a) - 0.5
    return d


sample_rate = 44100
duration = 1.0
frequency0 = 440

x = np.linspace(0, 2 * duration * np.pi, int(duration * sample_rate))

saw_and_square = np.concatenate((sawtooth(), square())) * 0.3

input("Press enter to play both waves >> ")
sd.play(saw_and_square, sample_rate)
time.sleep(duration * 2)
sd.stop()


