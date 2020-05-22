import pyaudio
import numpy as np
import wave 
import time 


DURATION = 6
RATE = 44100
WIDTH = 2
CHANNELS = 2


def generate_tone():
    
    x = np.linspace(0, 2 * DURATION * np.pi, int(DURATION * RATE))

    frequency = 440.0

    wav = np.sin(frequency * x)

    wav *= 0.3

    return wav

wav = generate_tone()
def callback(in_data, frame_count, time_info, status):
    data = in_data[:frame_count]
    wav = in_data[frame_count:]
    wf.writeframes(data)
    return (data, pyaudio.paContinue)

p = pyaudio.PyAudio()
#wav = generate_tone()
wf = wave.open('output.wav', 'wb')
wf.setnchannels(2)
wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
wf.setframerate(44100)

#p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(2), channels=2, rate=44100, output=True, stream_callback=callback)

stream.start_stream()
frames = []
while stream.is_active():
    time.sleep(0.1)

stream.stop_stream()
stream.close()
p.terminate()
wf.close()
#wf = wave.open('output.wav', 'wb')
#wf.setnchannels(2)
#wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
#wf.setframerate(44100)
#wf.writeframes(b''.join(frames))
#wf.close()
