import os
import numpy as np
import pyaudio
import wave
import time


CHUNK = 1024
SAMPLE_RATE = 48000
CHANNELS = 1
FORMAT = pyaudio.paInt16


def play_wav_track(file_path):
    wf = wave.open(file_path, 'rb'_)
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=SAMPLE_RATE,
                    output=True)
    
    data = wf.readframes(CHUNK)

    while data != '':
        stream.write(data)
        data = wf.readframes(CHUNK)
        if len(data) <= 0:
            break

    stream.stop_stream()
    stream.close()
    p.terminate()

    print("Playback Complete.")


def capture(duration, outfile):
    if duration.split(' ')[1].lower() == "s":
        duration = float(duration.split(' ')[0])

    elif duration.split(' ')[1].lower() == "m":
        duration = float(duration.split(' ')[0]) * 60

    else:
        print("Error invalid argument for duration! ex. '10 s' or '1 m'")
    
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=SAMPLE_RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    for i in range(0, int(SAMPLE_RATE / CHUNKS * duration)):
        data = stream.read(CHUNK)
        frames.append(data)


    stream.stop_stream()
    stream.close()
    p.terminate()


    wf = wave.open(outfile, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.getsample
