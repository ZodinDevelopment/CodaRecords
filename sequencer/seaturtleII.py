import os
import tkinter as tk
import numpy as np
import simpleaudio as sa
import wave


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
        self.keysA = ['q','w','t','u','g','h','s','b']
        self.keysB = ['f','o','y','i',' ','j','k','n']
        #self.soundsetA = self.init_sounds(self.keysA)
        #self.soundsetB = self.init_sounds(self.keysB)


        for s in SOUNDS:
            self.sounds.append(self.load_sample(s))

        self.soundsetA = self.init_sounds(self.keysA)
        self.soundsetB = self.init_sounds(self.keysB)
        self.bind_sounds()
        self.show_frame(PlayPage)

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
            sound = self.soundsetA.get(event.char)

        elif event.char in self.keysB:
            sound = self.soundsetB.get(event.char)

        else:
            sound = None

        play_obj = sa.play_buffer(sound, self.nchannels, self.sampwidth, self.framerate)

    def stop_it(self):
        sa.stop_all()

    def init_sounds(self, keyset):

        key_sounds = dict(zip(keyset, self.sounds))
        return key_sounds

    def load_sample(self, sound, index=0):

        samples_path = os.path.join('samples', sound)
        samples = os.listdir(samples_path)

        with wave.open(os.path.join(samples_path, samples[index]), 'r') as wav:
            self.framerate = wav.getframerate()
            self.nchannels = wav.getnchannels()
            self.sampwidth = wav.getsampwidth()

            sample = np.frombuffer(wav.readframes(self.framerate), dtype=np.int16)
        return sample


    def set_samples(self, selections):
        self.sounds = []
        for i in range(len(SOUNDS)):
            sound = SOUNDS[i]
            spin = selections[i]
            index = int(spin.get())
            self.sounds.append(self.load_sample(sound, index=index))

        self.soundsetA = self.init_sounds(self.keysA)
        self.soundsetB = self.init_sounds(self.keysB)
        self.bind_sounds()
        self.show_frame(PlayPage)

class PlayPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Play Mode', font=LARGE)
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text='Configure', command=lambda: controller.show_frame(ConfigurePage))
        button.pack()



class ConfigurePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        mainlabel = tk.Label(self, text="Configuration", font=LARGE)
        mainlabel.pack(pady=10, padx=10)
        selections = []
        for s in SOUNDS:
            samples_path = os.path.join('samples', s)
            n_options = len(os.listdir(samples_path))
            val = tk.IntVar()


            spinner = tk.Spinbox(self, from_=0, to=n_options - 1, textvariable=val)

            label = tk.Label(self, text=s, font=LARGE)
            label.pack(pady=10, padx=10)
            spinner.pack()
            selections.append(spinner)

        button = tk.Button(self, text='Confirm', command=lambda: controller.set_samples(selections))
        button.pack()


if __name__ == "__main__":
    app = SeaTurtle()
    app.mainloop()
