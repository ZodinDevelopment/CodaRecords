import numpy as np
import sounddevice as sd
import time
import matplotlib.pyplot as plt
plt.style.use('dark_background')


def sine(f):
    y = np.sin(f * x) * 0.2
    return y


def triangle():
    y = 2 / np.pi * np.arcsin(np.sin(freq3 * x + ramp1 * sine(
            freq2))) * 0.2
    return y


def triangle2():
    y = 2 / np.pi * np.arcsin(np.sin(freq4 * x)) * 0.2
    return y


def triangle_mod():
    y = 2 / np.pi * np.arcsin(np.sin(frequency * x + ramp0 * np.sin(
        freq1 * x))) * 0.2
    return y


def lfo():
    y = np.sin(lfo_f * x)
    y = (y * lfo_amount / 2 + (1 - lfo_amount / 2))
    return y



sample_rate = 44100
duration = 20.0
frequency = 440.0
freq1 = 400.0
freq2 = 622.2540
freq3 = 1864.655
freq4 = 932.3275
freq5 = 300.0
freq6 = 82.40689
lfo_f = 10.0
lfo_amount = 0.1

x = np.linspace(0, 2 * duration * np.pi, int(duration * sample_rate))

ramp0 = np.logspace(0, 1, int(duration * sample_rate)) * 4
ramp1 = np.logspace(1, 0, int(duration * sample_rate)) * 5

wave_data = ((triangle_mod() + sine(freq5) + triangle() + triangle2()
    + sine(freq6) + sine(55.0)) * lfo()) * 0.2


input("Press enter to play the result >>> ")
sd.play(wave_data, sample_rate)
time.sleep(duration)
sd.stop()


fig, (ax0, ax1) = plt.subplots(nrows=2)

ax0.plot(wave_data[:500], linewidth=2.0)
ax1.plot(wave_data[:7500], linewidth=2.0)

plt.show()
