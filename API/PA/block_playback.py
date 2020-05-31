import pyaudio
import wave
import sys


CHUNK = 1024

if len(sys.argv) < 2:
    print("Usage: {} filename.wav".format(sys.argv[0]))
    sys.exit(-1)

print("Reading raw bytes from wave file at '{}'".format(sys.argv[1]))

wf = wave.open(sys.argv[1], 'rb')

print("Initializing PyAudio")
p = pyaudio.PyAudio()

input("Press Return to open an output stream and play back the audio array >> ")

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

print("Writing frames from audio array to output stream...")
data = wf.readframes(CHUNK)

while data != '':
    stream.write(data)
    data = wf.readframes(CHUNK)
    if len(data) <= 0:
        break

input("Finished, press Return to close the stream and terminate the audio engine >> ")
stream.stop_stream()
stream.close()
p.terminate()


    
