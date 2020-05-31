import os
import numpy as np
import simpleaudio as sa
import wave
import tkinter as tk


LARGE = ('Verdana', 12)
SOUNDS = ['claps', 'closed', 'cymbals', 'fx', 'kicks', 'open', 'toms', 'snares']



class SeaTurtle(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side='top', fill='both', expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (PlayPage, ConfigurePage):
            frame = F(container, self)

            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.sounds = []
        self.keysA = [' ', 'f', 'v', 'g', 'r', 'w', 's', 'd']
        self.keysB = ['b', 'j', 'n', 'h', 'u', 'i', 'k', 'm']

        for s in SOUNDS:
            self.sounds.append(self.load_sample(s))

        self.padA = self.init_sounds(self.keysA)
        self.padB = self.init_sounds(self.keysB)

        self.bind_sounds()
        self.show_frame(PlayPage)

    def load_sample(self, sound, index=0):
        samples_path = os.path.join('samples', sound)
        samples = os.listdir(samples_path)

        with wave.open(os.path.join(samples_path, samples[index]), 'r') as wav:
            self.framerate = wav.getframerate()
            self.nchannels = wav.getnchannels()
            self.sampwidth = wav.getsampwidth()

            sample = np.frombuffer(wav.readframes(self.framerate), dtype=np.int16)

        return sample

    def init_sounds(self, keyset):
        key_sounds = dict(zip(keyset, self.sounds))
        return key_sounds

    def bind_sounds(self):
        for k in self.keysA:
            self.bind(f'<KeyPress-{k}>', self.play_it)

        for k in self.keysB:
            self.bind(f'<KeyPress-{k}>', self.play_it)

    def show_frame(self, cont):
        frame = self.frames[cont]

        frame.tkraise()

    def play_it(self, event):
        if event.char in self.keysA:
            sound = self.padA.get(event.char)

        elif event.char in self.keysB:
            sound = self.padB.get(event.char)

        else:
            sound = 0

        play_obj = sa.play_buffer(sound, self.nchannels, self.sampwidth, self.framerate)

    def stop_it(self):
        sa.stop_all()

    def set_samples(self, sound, selections, pad='both'):
        sound_index = SOUNDS.index(sound)
        spin = selections[sound_index]
        index = int(spin.get())
        self.sounds[sound_index] = self.load_sample(sound, index=index)


        if pad == 'a':
            self.padA = self.init_sounds(self.keysA)

        elif pad == 'b':
            self.padB = self.init_sounds(self.keysB)

        elif pad == 'both':
            self.padA = self.init_sounds(self.keysA)
            self.padB = self.init_sounds(self.keysB)

        self.bind_sounds()
        self.show_frame(PlayPage)

    def mix_samples(self, selections):
        for i in range(len(SOUNDS)):
            sound = SOUNDS[i]
            spin = selections[i]
            index = float(spin.get())
            index = 1 / index
            self.sounds[i] = self.sounds[i] * index

            self.bind_sounds()
            self.show_frame(PlayPage)



class PlayPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="SeaTurtleIV", font=LARGE)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Configure", command=lambda: controller.show_frame(ConfigurePage))
        button1.pack()

        button2 = tk.Button(self, text='Mixer', command=lambda: controller.show_frame(MixerPage))
        button2.pack()


class MixerPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        mainlabel = tk.Label(self, text='Adjust Levels', font=LARGE)
        mainlabel.pack(pady=10, padx=10)
        selections = []
        for s in SOUNDS:
            val = tk.IntVar()

            spinner = tk.Scale(self, from_=0.0, to=100.0, resolution=1.0, orient=tk.VERTICAL, length=200)

            label = tk.Label(self, text=s, font=LARGE)
            label.pack(pady=10, padx=10)
            spinner.pack()
            selections.append(spinner)

        buttonMix = tk.Button(self, text='Confirm', command=lambda: controller.mix_samples(selections))
        buttonMix.pack()


class ConfigurePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        mainlabel = tk.Label(self, text='Configure Kit', font=LARGE)
        mainlabel.pack(pady=10, padx=10)
        selections = []
        for s in SOUNDS:
            samples_path = os.path.join('samples', s)
            n_options = len(os.listdir(samples_path))
            val = tk.IntVar()

            spinner = tk.Spinbox(self, from_=0, to=n_options-1, textvariable=val)

            label = tk.Label(self, text=s, font=LARGE)
            label.pack(pady=10, padx=10)
            spinner.pack()
            selections.append(spinner)
            b = tk.Button(self, text=s, command=lambda: controller.set_samples(s, selections, pad='both'))
            b.pack()

        buttonCancel = tk.Button(self, text='Cancel', command=lambda: controller.show_frame(PlayPage))
        buttonCancel.pack()


if __name__ == "__main__":
    app = SeaTurtle()
    app.mainloop()
import os
import numpy as np
import simpleaudio as sa
import wave
import tkinter as tk


LARGE = ('Verdana', 12)
SOUNDS = ['claps', 'closed', 'cymbals', 'fx', 'kicks', 'open', 'toms', 'snares']



class SeaTurtle(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side='top', fill='both', expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (PlayPage, ConfigurePage, MixerPage):
            frame = F(container, self)

            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.sounds = []
        self.keysA = [' ', 'f', 'v', 'g', 'r', 'w', 's', 'd']
        self.keysB = ['b', 'j', 'n', 'h', 'u', 'i', 'k', 'm']

        for s in SOUNDS:
            self.sounds.append(self.load_sample(s))

        self.padA = self.init_sounds(self.keysA)
        self.padB = self.init_sounds(self.keysB)

        self.bind_sounds()
        self.show_frame(PlayPage)

    def load_sample(self, sound, index=0):
        samples_path = os.path.join('samples', sound)
        samples = os.listdir(samples_path)

        with wave.open(os.path.join(samples_path, samples[index]), 'r') as wav:
            self.framerate = wav.getframerate()
            self.nchannels = wav.getnchannels()
            self.sampwidth = wav.getsampwidth()

            sample = np.frombuffer(wav.readframes(self.framerate), dtype=np.int16)

        return sample

    def init_sounds(self, keyset):
        key_sounds = dict(zip(keyset, self.sounds))
        return key_sounds

    def bind_sounds(self):
        for k in self.keysA:
            self.bind(f'<KeyPress-{k}>', self.play_it)

        for k in self.keysB:
            self.bind(f'<KeyPress-{k}>', self.play_it)

    def show_frame(self, cont):
        frame = self.frames[cont]

        frame.tkraise()

    def play_it(self, event):
        if event.char in self.keysA:
            sound = self.padA.get(event.char)

        elif event.char in self.keysB:
            sound = self.padB.get(event.char)

        else:
            sound = 0

        play_obj = sa.play_buffer(sound, self.nchannels, self.sampwidth, self.framerate)

    def stop_it(self):
        sa.stop_all()

    def set_samples(self, sound, selections, pad='both'):
        sound_index = SOUNDS.index(sound)
        spin = selections[sound_index]
        index = int(spin.get())
        self.sounds[sound_index] = self.load_sample(sound, index=index)


        if pad == 'a':
            self.padA = self.init_sounds(self.keysA)

        elif pad == 'b':
            self.padB = self.init_sounds(self.keysB)

        elif pad == 'both':
            self.padA = self.init_sounds(self.keysA)
            self.padB = self.init_sounds(self.keysB)

        self.bind_sounds()
        self.show_frame(PlayPage)

    def mix_samples(self, selections):
        for i in range(len(SOUNDS)):
            sound = SOUNDS[i]
            spin = selections[i]
            index = float(spin.get())
            index = 1 / index
            self.sounds[i] = self.sounds[i] * index

        self.bind_sounds()
        self.show_frame(PlayPage)

class PlayPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="SeaTurtleIV", font=LARGE)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Configure", command=lambda: controller.show_frame(ConfigurePage))
        button1.pack()

        button2 = tk.Button(self, text='Mixer', command=lambda: controller.show_frame(MixerPage))
        button2.pack()


class MixerPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        mainlabel = tk.Label(self, text='Adjust Levels', font=LARGE)
        mainlabel.pack(pady=10, padx=10)
        selections = []
        for s in SOUNDS:
            val = tk.IntVar()

            spinner = tk.Scale(self, from_=1.0, to=100.0, resolution=1.0, orient=tk.HORIZONTAL, length=200)

            label = tk.Label(self, text=s, font=LARGE)
            label.pack(pady=5, padx=5)
            spinner.pack()
            selections.append(spinner)

        buttonMix = tk.Button(self, text='Confirm', command=lambda: controller.mix_samples(selections))
        buttonMix.pack()


class ConfigurePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        mainlabel = tk.Label(self, text='Configure Kit', font=LARGE)
        mainlabel.pack(pady=10, padx=10)
        selections = []
        for s in SOUNDS:
            samples_path = os.path.join('samples', s)
            n_options = len(os.listdir(samples_path))
            val = tk.IntVar()

            spinner = tk.Spinbox(self, from_=0, to=n_options-1, textvariable=val)

            label = tk.Label(self, text=s, font=LARGE)
            label.pack(pady=10, padx=10)
            spinner.pack()
            selections.append(spinner)
            b = tk.Button(self, text=s, command=lambda: controller.set_samples(s, selections, pad='both'))
            b.pack()

        buttonCancel = tk.Button(self, text='Cancel', command=lambda: controller.show_frame(PlayPage))
        buttonCancel.pack()


if __name__ == "__main__":
    app = SeaTurtle()
    app.mainloop()
