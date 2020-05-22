import numpy as np
import simpleaudio as sa
import tkinter as tk


def play_it(event):
    sound = key_notes.get(event.char)
    play_obj = sa.play_buffer(sound, 2, 2, sample_rate)


def stop_it():
    sa.stop_all()


def do_it(place_holder=0):

    def triangle(f, detune=0.0):
        y = 2 / np.pi * np.arcsin(np.sin((f + detune) * x + ramp0 *
            (2 / np.pi * np.arcsin(np.sin(f + detune) * 0.5) * x +
                (np.sin(((f + detune) * fm) * x) * 0.5))))

        return y


    fm = 0.25
    freq5 = float(scale_freq5.get())
    duration = float(scale_duration.get())
    freq1 = float(scale_f1.get())
    ramp_amount = float(scale_rampe.get())
    roll_amount = int(scale_roll.get())

    x = np.linspace(0, 2 * np.pi * duration, int(duration * sample_rate))
    ramp0 = np.logspace(1, 0, np.size(x), base=10) * ramp_amount

    notes = []

    for i in range(-5, 10):
        factor = (2**(i / 12.0))
        waveform_mod = triangle(freq1 * factor)
        waveform = triangle(freq1 * factor)
        waveform_detune = triangle(freq1 * factor, freq5)

        waveform = ((waveform + waveform_detune) * (waveform_mod / 2 + 0.5)) * 1

        waveform[-fade_amount:] *= fade
        waveform = np.int16(waveform * 32767)
        waveform2 = np.roll(waveform, roll_amount, axis=None)
        waveform3 = np.vstack((waveform2, waveform)).T
        notes.append(waveform3.copy(order="C"))

    global key_notes
    key_notes = dict(zip(keys, notes))
    return key_notes


def binders(la):
    master.bind(f"<{la}>", play_it)

keys = ['a', 's', 'e', 'd', 'r', 'f', 't',
        'g', 'h', 'u', 'j', 'i', 'k', 'l', 'p']


sample_rate = 44100
fade_amount = 8000
fade = np.linspace(1, 0, fade_amount)
master = tk.Tk()
master.geometry('800x600')
master.configure(padx=20, pady=20)
master.title('No')


for i in keys:

    binders(f'{i}')


master.bind("<ButtonRelease-1>", do_it)
duration_label = tk.Label(master, text="Duration")
freq5_label = tk.Scale(master, from_=0.0, to=13.0, resolution=0.2, orient=tk.HORIZONTAL, length=200)

scale_f1 = tk.Scale(master, from_=110, to=660, resolution=110, orient=tk.HORIZONTAL, length=50)
scale
