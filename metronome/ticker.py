import numpy as np
import sounddevice as sd
import time
import wavio
import tkinter as tk
import sys


def tick(tempo, notes_per_measure=4):
    
    primary_tone = wavio.read('metronome.wav')
    sample_rate = primary_tone.rate

    tick = primary_tone.data

    other_tone = wavio.read('tock.wav')
    
    tock = other_tone.data

    tick_step = 60 / (tempo*2)

    ticking = True

    note = 1

    while ticking:

        if note == 1:
            sound = tock

        else:
            sound = tick

        sd.play(sound, sample_rate)
        time.sleep(tick_step)
        sd.stop()
        if note < notes_per_measure:
            note += 1


        else:
            note = 1
        print(note)


if __name__ == "__main__":
    
    if len(sys.argv) == 2:

        tick(int(sys.argv[1]))

    else:
        tick(int(sys.argv[1]), int(sys.argv[2]))

