import numpy as np
import sounddevice as sd
import time
import matplotlib.pyplot as plt
import scipy.io.wavfile as wf
plt.style.use('dark_background')
import sys


if len(sys.argv) >= 3:
    frequency = float(sys.argv[1])
    duration = float(sys.argv[2])

else:
    duration = 3.0
    frequency = 440.0

print(f"Generated Sine Wave of {duration} seconds at {frequency} Hz")
input("Press enter to listen to resulting wave >> ")



sample_rate = 44100

x = np.linspace(0, 2 * duration * np.pi, int(duration * sample_rate))
sinewave_data = np.sin(frequency * x + np.ain)

sinewave_data = sinewave_data * 0.3

sd.play(sinewave_data, sample_rate)
time.sleep(duration)
sd.stop()


plot_data = sinewave_data[:500]

input("Press enter to plot the resulting waveform >> ")

fig, ax = plt.subplots()
ax.plot(plot_data, linewidth=3)
plt.xlabel('Sample Number')
plt.ylabel("Amplitude")
plt.show()

outfile = str(input("Enter a filename to save the WAV data to >> "))
write_data = np.int16(sinewave_data * 32767)
wf.write(outfile,sample_rate, write_data)



