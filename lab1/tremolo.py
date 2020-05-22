import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import time
import sys
plt.style.use('dark_background')


sample_rate = 44100

if len(sys.argv) >= 2:
    duration = float(sys.argv[1])

else:
    duration = 6.0

if len(sys.argv) >= 3:
    frequency = float(sys.argv[2])

else:
    frequency = 440.0



if len(sys.argv) >= 4:
    fm = float(sys.argv)

else:
    fm= 430.0


tremolo_frequency = 8.0
ramp_amount = 2.1
factor = 0.9


ramp0 = np.logspace(0, 1, int(duration * sample_rate)) * ramp_amount
x = np.linspace(0, 2 * np.pi * 2, int(duration * sample_rate))
x_lfo = np.linspace(0, duration * 2 * np.pi, int(duration * sample_rate))

tremolo_osc = np.sin(tremolo_frequency * x)
tremolo_osc = (tremolo_osc * factor / 2 + (1 - factor / 2))

print(np.max(tremolo_osc))
print(np.min(tremolo_osc))
wave_data = np.sin(frequency * x + ramp0 * np.sin(
    fm * x)) * tremolo_osc

wave_data = wave_data * 0.2

sd.play(wave_data, sample_rate)
time.sleep(duration)
sd.stop()

input("Press enter to plot the resulting wave >> ")

fig, (ax0, ax1) = plt.subplots(nrows=2)
ax0.plot(wave_data[:1000], linewidth=2)
ax1.plot(wave_data[:10000], linewidth=2)

plt.xlabel('Sample Number')
plt.ylabel('Amplitude')
plt.show()

