import os
import sys
import time
import numpy as np
import sounddevice as sd
import simpleaudio as sa
import tkinter as tk
import wavio


def play_it(event):
    sound = key_sounds.get(event.char)
    #sound = key_sounds.get(event.keysym)
    play_obj = sa.play_buffer(sound, 1, 2, sample_rate)
    #print(event.keycode)
    #sd.play(sound, sample_rate)


def stop_it():
    #sd.stop()
    sa.stop_all()

def do_it(place_holder=None):
    ''''
    def load_wave(fname):

        wave = wavio.read(fname)

        return wave.dat
    '''


    # sounds = []
    # for wav in os.listdir('808/'):
        # wavfile = wavio.read(os.path.join('808', wav))

        # sound = wavfile.data

        # sample_rate = wavfile.rate

        # sounds.append(sound)

    sounds = [wavio.read(os.path.join('sampleset', wavfile)).data for wavfile in os.listdir('sampleset')]
    global key_sounds
    key_sounds = dict(zip(keys, sounds))
    return key_sounds



keys = ['a','s','d','f','g','h','j','k','l','z','x','c','b','n','m']
sample_rate = 22050
master = tk.Tk()
master.geometry('800x600')
master.configure(padx=20, pady=20)

for k in keys:
   master.bind(f"<KeyPress-{k}>", play_it)
master.bind("<ButtonRelease-1>", do_it)
#master.bind('<Key>', play_it)
stop_button = tk.Button(master, text="Stop", command=stop_it)

stop_button.grid(row=3, column=0, padx=50)

key_sounds = do_it()

master.mainloop()



