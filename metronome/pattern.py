import os
import sys
import time
import numpy as np
import sounddevice as sd
import wavio


def main(tempo, pattern):

    wav = wavio.read('metronome.wav')
    sample_rate = wav.rate
    
    beat_duration = 60 / tempo 
    quarter_note = int(sample_rate * beat_duration)

    pattern = pattern.split('.')
    audio = wav.data
    audio = audio[:quarter_note]

    x = np.linspace(0, 2 * beat_duration * np.pi, int(beat_duration * sample_rate))
    notes = []
    for p in pattern:
        if p == '0':
            n = np.zeros_like(audio)
            n = n.astype(np.int16)

        elif p == '1':
        
            n = audio.astype(np.int16)

        notes.append(n)

    measure = np.concatenate([n for n in notes])

    sd.play(measure, sample_rate)

if __name__ == "__main__":
    tempo = int(sys.argv[1])
    pattern = sys.argv[2]

    main(tempo, pattern)

