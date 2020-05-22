import numpy as np
import sounddevice as sd
import tkinter as tk


def play_it(event):
    sound = key_notes.get(event.char)
    sd.play(sound, sample_rate)


def stop_it():
    sd.stop()


def do_it(place_holder=None):
    def sine_wave(f, detune=0.0):
        y = np.sin((f + detune) * x + ramp0 *
                np.sin(((f + detune) * 0.5) * x))
        return y

    freq1 = 440.0
    shift_amount = 800
    detune_freq = float(scale_detune.get())
    duration = float(scale_duration.get())

    x = np.linspace(0, 2 * np.pi * duration, int(duration * sample_rate))
    ramp0 = np.logspace(1, 0, np.size(x), base=5)

    notes = []
    for i in range(-9, 6):
        waveform_mod = sine_wave(freq1 * (
            2**(i / 12.0)), detune_freq)
        waveform1 = sine_wave(
                freq1 * (2**(i / 12.0)))

        waveform1 = (waveform1 * (waveform_mod / 2 + 0.5)) * 0.5
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
master.geometry('800x600')
master.configure(padx=20, pady=20)

for k in keys:
    master.bind(f"<{k}>", play_it)
master.bind("<ButtonRelease-1>", do_it)

duration_label = tk.Label(master, text="Duration")
detune_label = tk.Label(master, text="Detune")

scale_duration = tk.Scale(master, from_=0.2, to=5.0, resolution=0.2, orient=tk.HORIZONTAL, length=200)
scale_detune = tk.Scale(master, from_=0.0, to=13, resolution=0.2, orient=tk.HORIZONTAL, length=200)
stop_button = tk.Button(master, text="Stop", command=stop_it)

scale_duration.set(1.0)

duration_label.grid(row=0, column=0)
detune_label.grid(row=1, column=0)
scale_duration.grid(row=0, column=1)
scale_detune.grid(row=1, column=1)
stop_button.grid(row=3, column=0, padx=50)

key_notes = do_it()
master.mainloop()

