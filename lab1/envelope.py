import numpy as np
import sounddevice as sd
import time


sample_rate = 44100
duration = 4.0
sustain_value = 0.3

x = np.linspace(0, 2 * duration * np.pi, int(duration*sample_rate))

attack_length = len(x) // 10
decay_length = len(x) // 2
sustain_length = len(x) - (attack_length + decay_length)

attack = np.linspace(0, 1, num=attack_length)
decay = np.linspace(1, sustain_value, num=decay_length)
sustain = np.ones(sustain_length) * sustain_value
ads = np.concatenate((attack, decay, sustain))

wave_data = np.sin(220 * x)

wave_data = wave_data * ads


sd.play(wave_data, sample_rate)
time.sleep(duration)
sd.stop()


