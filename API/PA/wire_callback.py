import pyaudio
import time


WIDTH = 2
CHANNELS = 2
RATE = 44100

p = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    return (in_data, pyaudio.paContinue)

input("Press Return to initialize wire stream >> ")

stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                stream_callback=callback)

stream.start_stream()
print("Stream Activated")

while stream.is_active():
    time.sleep(0.1)

print("Stream closed, terminating the engine.")
stream.stop_stream()
stream.close()

p.terminate()
