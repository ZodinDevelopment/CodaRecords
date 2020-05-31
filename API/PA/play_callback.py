import pyaudio
import wave
import time
import sys


if len(sys.argv) < 2:
    print("Usage:\n====\n{} filename.wav".format(sys.argv[0]))
    sys.exit(-1)

wf = wave.open(sys.argv[1], 'rb')

p = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    return (data, pyaudio.paContinue)

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                stream_callback=callback)

stream.start_stream()

while stream.is_active():
    time.sleep(0.1)

print("Done")
stream.stop_stream()
stream.close()
wf.close()

p.terminate()

