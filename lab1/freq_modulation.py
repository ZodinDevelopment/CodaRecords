import numpy as np
import sounddevice as sd
import time
import sys
import matplotlib.pyplot as plt
plt.style.use('dark_background')



sample_rate = 44100
if len(sys.argv) >= 2:
    duration = float(sys.argv[1])
    frequency = float(sys.argv[2])
    fm = float(sys.argv[3])
    factor = 2.0

else:
    duration = 6
    frequency = 440
    fm = 439.0
    factor = 2.0


x = np.linspace(0, duration * 2 * np.pi, int(duration * sample_rate))
wave_data = np.sin(frequency * x + (np.sin(fm * x) * factor))
wave_data = wave_data * 0.2


sd.play(wave_data, sample_rate)
time.sleep(duration)
sd.stop()


fig, ax = plt.subplots()
ax.plot(wave_data, linewidth=2)
plt.xlabel("Sample Number")
plt.ylabel("Amplitude")
plt.show()




print("Script finished.")
