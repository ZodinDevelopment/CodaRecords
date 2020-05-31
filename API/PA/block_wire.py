import pyaudio
import sys


CHUNK = 1024
WIDTH = 2
CHANNELS = 2
RATE = 44100

if len(sys.argv) != 2:
    print("Usage\n=====\n{} [duration]".format(sys.argv[0]))
    sys.exit(-1)

DURATION = float(sys.argv[1])

print("Initializing audio engine")
p = pyaudio.PyAudio()
input("Press Return when ready >> ")
print("Opening a stream from input device to default output")
stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)


print("* recording")

for i in range(0, int(RATE / CHUNK * DURATION)):
    data = stream.read(CHUNK)
    stream.write(data, CHUNK)

print("* done")

stream.stop_stream()
stream.close()
p.terminate()
