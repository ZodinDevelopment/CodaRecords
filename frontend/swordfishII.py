import numpy as np
import simpleaudio as sa
import tkinter as tk


def play_it(event):
    sound = key_notes.get(event.char)
    play_obj = sa.play_buffer(sound, 2, 2, sample_rate)


def stop_it():
    sa.stop_all()


def do_it(place_holder=0):
    def saw_wave(f, detune=0.0):
        y = -2 / np.pi * np.arctan(np.tan(np.pi / 2 - (x * np.pi / (1 / f * 2 * np.pi + ramp0 * np.sin(((f + detune) * 0.5) * x + (np.sin(((f + detune) * fm) * x) * 0.5))))))
        return y

    fm = 0.25
    freq5 = float(scale_freq5.get())
    duration = float(scale_duration.get())
    freq1 = float(scale_f1.get())
    ramp_amount = float(scale_ramp.get())
    roll_amount = int(scale_roll.get())

    x = np.linspace(0, 2 * np.pi * duration, int(duration * sample_rate))
    ramp0 = np.logspace(1, 0, np.size(x), base=10) * ramp_amount

    notes = []
    for i in range(-5, 10):
        factor = (2**(i / 12.0))
        waveform_mod = saw_wave(freq1 * factor)
        waveform = saw_wave(freq1 * factor)
        waveform_detune = saw_wave(freq1 * factor, freq5)

        waveform = ((waveform + waveform_detune) *
                    (waveform_mod / 2 + 0.5)) * 0.1

        waveform[-fade_amount:] *= fade
        waveform = np.int16(waveform * 32767)
        waveform2 = np.roll(waveform, roll_amount, axis=None)
        waveform3 = np.vstack((waveform2, waveform)).T
        notes.append(waveform3.copy(order='C'))

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
master.title("No")

for i in keys:
    binders(f'{i}')

master.bind("<ButtonRelease-1>", do_it)

duration_label = tk.Label(master, text="Duration")
freq5_label = tk.Label(master, text="Detune")
f1_label = tk.Label(master, text="Octave")
ramp_label = tk.Label(master, text="Ramp")
roll_label = tk.Label(master, text="Delay")

scale_duration = tk.Scale(master, from_=0.2, to=5.0, resolution=0.2, orient=tk.HORIZONTAL, length=200)
scale_freq5 = tk.Scale(master, from_=0.0, to=13.0, resolution=0.2, orient=tk.HORIZONTAL, length=200)
scale_f1 = tk.Scale(master, from_=220, to=660, resolution=220, orient=tk.HORIZONTAL, length=50)
scale_ramp = tk.Scale(master, from_=0.0, to=2.0, resolution=0.01, orient=tk.HORIZONTAL, length=200)
scale_roll = tk.Scale(master, from_=0, to=4000, resolution=50, orient=tk.HORIZONTAL, length=200)

stop_it_button = tk.Button(master, text="Stop", command=stop_it)
scale_duration.set(1.0)
scale_freq5.set(5.0)
scale_f1.set(440)
scale_ramp.set(0.5)

duration_label.grid(row=0, column=0)
freq5_label.grid(row=1, column=0)
f1_label.grid(row=2, column=0)
ramp_label.grid(row=3, column=0)
roll_label.grid(row=4, column=0)

scale_duration.grid(row=0, column=1)
scale_freq5.grid(row=1, column=1)
scale_f1.grid(row=2, column=1, sticky='w')
scale_ramp.grid(row=3, column=1)
scale_roll.grid(row=4, column=1)
stop_it_button.grid(row=0, column=2)

key_notes = do_it()
master.mainloop()


