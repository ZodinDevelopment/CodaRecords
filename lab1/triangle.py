import sys
import numpy as np
import sounddevice as sd
import time
import matplotlib.pyplot as plt
plt.style.use('dark_background')


sample_rate = 44100
if len(sys.argv) >= 2:
    duration = float(sys.argv[1])

else:
    duration = 2.0

if len(sys.argv) >= 3:
    frequency = float(sys.argv[2])

else:
    frequency = 440.0


x = np.linspace(0, 2 * np.pi * duration, int(sample_rate * duration))
wave_data = 2 / np.pi * np.arcsin(np.sin(frequency * x)) * 0.5

input("Press enter to play the triangle wave >> ")
sd.play(wave_data, sample_rate)
time.sleep(duration)
sd.stop()

fig, ax = plt.subplots()
ax.plot(wave_data[:400], linewidth=3.0)
plt.title("Triangle")
plt.xlabel("Sample Number")
plt.ylabel("Amplitude")
plt.show()


