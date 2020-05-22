import sys
import numpy as np
import sounddevice as sd
import time


sample_rate = 44100

if len(sys.argv) >= 3:
    duration = float(sys.argv[1])
    frequency = float(sys.argv[2])
    fm = float(sys.argv[3])


else:
    duration = 6.0
    frequency = 880.0
    fm = 73.3333


ramp0 = np.logspace(0, 1, int(duration * sample_rate))

X = np.linspace(0, 2 * duration * np.pi, int(duration * sample_rate))


wave_data = np.sin(frequency * x + ramp0 * np.sin(fm * x))

wave_data = wave_data * 0.2

input("Press enter to play the wave >>> ")
sd.play(wave_data, sample_rate)
time.sleep(duration)
sd.stop()


print("Playback Complete. Goodbye")
