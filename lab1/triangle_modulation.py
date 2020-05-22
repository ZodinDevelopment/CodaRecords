import numpy as np
import sounddevice as sd
import time
import matplotlib.pyplot as plt
plt.style.use('dark_background')


def sin_wave():
    return np.sin(fm0 * x)


def wave_data():
    return 2 / np.pi * np.arcsin(
        np.sin(frequency0 * x + ramp0 * sin_wave())) * 0.2


sample_rate = 44100
duration = 8.0
frequency0 = 440
fm0 = 100

x = np.linspace(0, 2 * duration * np.pi, int(duration * sample_rate))
ramp0 = np.logspace(0, 1, int(duration * sample_rate)) * 7

result = wave_data()

input("Press enter to play resulting wave >> ")

sd.play(result, sample_rate)
time.sleep(duration)
sd.stop()

fig, (ax0, ax1) = plt.subplots(nrows=2)

ax0.plot(result[:500], linewidth=2.0)
ax1.plot(result[:10000], linewidth=2.0)
plt.show()


