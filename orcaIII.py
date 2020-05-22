import numpy as np
import sounddevice as sd
import tkinter as tk

from audiolib.wavelib import *
from audiolib.arrays import *


MODULATORS = {
        'sine': sine_modulation,
        'triangle': triangle_modulation,
        'sawtooth': sawtooth_modulation,
        'square': square_modulation
}
BASES = [
    ("sine", 1),
    ('triangle', 2),
    ('sawtooth', 3),
    ('square', 4)
]


def play_it(event):
    sound = key_notes.get(event.char)
    sd.play(sound, sample_rate)


def stop_it():
    sd.stop()


def do_it(place_holder=None):
    def synthesize(frequency, duration, fm, level, sample_rate, base, carrier):

        modulator = MODULATORS.get(base)

        return modulator(frequency, duration, fm, level, sample_rate, carrier)



    freq = 440.0
    shift_amount = 800
    phase_factor = float(scale_phase.get())
    duration = float(scale_duration.get())
    level = float(scale_level.get())

    base = radio_base.get()
    carrier = radio_carrier.get()
    base = MODULATORS.get(base)
    

    notes = []
    for i in range(-9, 6):
        waveform1 = synthesize(frequency=freq * (2**(i / 12.0)), duration=duration, fm=phase_factor*freq, level=level, sample_rate=sample_rate, base=base, carrier=carrier)

        waveform2 = np.roll(waveform1, shift_amount)

        waveform2[:shift_amount] = 0
        waveform_stereo = np.vstack((waveform2, waveform1)).T

        notes.append(waveform_stereo)


    global key_notes
    key_notes = dict(zip(keys, notes))
    return key_notes


sample_rate = 44100
keys = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i',
        'o', 'p', 'a', 'd', 'f', 'h', 'j']
master = tk.Tk()
#master.geometry('800x600')
#master.configure(padx=20, pady=20)

for k in keys:
    master.bind(f"<{k}>", play_it)
master.bind("<ButtonRelease-1>", do_it)

duration_label = tk.Label(master, text="Duration")
phase_label = tk.Label(master, text="Modulation Factor")
level_label = tk.Label(master, text="Playback Level")

base_label = tk.Label(master, text="Wave Type I")
carrier_label = tk.Label(master, text="Wave Type II")

scale_duration = tk.Scale(master, from_=0.2, to=5.0, resolution=0.2, orient=tk.HORIZONTAL, length=200)
scale_phase = tk.Scale(master, from_=0.10, to=95.0, resolution=0.5, orient=tk.HORIZONTAL, length=200)
scale_level = tk.Scale(master, from_=0.1, to=0.95, resolution=0.05, orient=tk.HORIZONTAL, length=200)

radio_base = tk.IntVar()


radio_base.set(1)


for text, mode in BASES:
    b = tk.Radiobutton(master, text=text, variable=radio_base, value=mode)

    b.pack()


radio_carrier = tk.IntVar()

radio_carrier.set(1)

for text, mode in BASES:
    b = tk.Radiobutton(master, text=text, variable=radio_carrier, value=mode)

    b.pack()



stop_button = tk.Button(master, text="Stop", command=stop_it)
radio_base.set(1)
radio_carrier.set(1)
scale_duration.set(1.0)
scale_phase.set(0.50)
scale_level.set(0.3)

#duration_label.grid(row=0, column=0)
#phase_label.grid(row=1, column=0)
#level_label.grid(row=2, column=0)
#base_label.grid(row=3, column=0)
#carrier_label.grid(row=4, column=0)

#scale_duration.grid(row=0, column=1)
#scale_phase.grid(row=1, column=1)
#scale_level.grid(row=2, column=1)

#radio_base.grid(row=0, column=2)
#radio_carrier.grid(row=0, column=3)
scale_duration.pack()
scale_phase.pack()
scale_level.pack()
stop_button.pack()
#radio_base.pack()
#radio_carrier.pack()

#stop_button.grid(row=3, column=0, padx=50)

key_notes = do_it()

master.mainloop()


