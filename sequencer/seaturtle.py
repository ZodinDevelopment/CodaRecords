import os
import tkinter as tk
import numpy as np
import wavio
import simpleaudio as sa
import wave


LARGE = ('Verdana', 12)

SOUNDS = ['claps', 'closed', 'cymbals', 'fx', 'kicks', 'open', 'toms', 'snares']


class MainApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side='top', fill='both', expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (PlayPage, ConfigurePage, ViewPage):

            frame = F(container, self)


            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')




        """
        for f in os.listdir('sampleset'):
            orig = wave.open(os.path.join('sampleset', f), 'r')
            self.framerate = orig.getframerate()
            self.nchannels = orig.getnchannels()
            self.sampwidth = orig.getsampwidth()
            self.sounds.append(np.frombuffer(orig.readframes(44100), dtype=np.int16))

            orig.close()

        """
        self.library = {}
        for s in SOUNDS:
            samples_path = os.path.join('samples', s)
            samples = []
            for f in os.listdir(samples_path):
                wav = wave.open(os.path.join(samples_path, f), 'r')
                self.framerate = wav.getframerate()
                self.nchannels = wav.getnchannels()
                self.sampwidth = wav.getsampwidth()

                samples.append(np.frombuffer(wav.readframes(self.framerate), dtype=np.int16))

                wav.close()

            self.library[s] = samples

        self.sounds





        #self.keys = [['q', 'p'], ['w','o'], ['e','i'], ['r','u'], ['t','y'], ['f','j']]
        self.keysA = ['q','w','e','r','t','a','d','f']
        self.keysB = ['p', 'o', 'i', 'u', 'y', 'l','k']
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

        play_obj = sa.play_buffer(sound, 1, self.sampwidth, 44100)

    def stop_it(self):
        sa.stop_all()

    def configure(self):
        for key in self.keys:
            self.bind(f"<KeyPress-{key}>", None)
        self.keys = []
        with open('keys.txt', 'r') as f:
            keys = f.read()
            self.keys = keys.split('.')

        self.key_sounds = self.init_sounds()
        self.bind_sounds()
    def add_key(self, event):
        self.keys.append(event.char)
        print(f"Added {event.char}")


    def init_sounds(self, keyset):

        key_sounds = dict(zip(keyset, self.sounds))
        return key_sounds

    def cycle_sample(sound):



class PlayPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Play Mode", font=LARGE)
        label.pack(pady=10,padx=10)

        button = tk.Button(self, text='Configure', command=lambda: controller.show_frame(ConfigurePage))
        button.pack()



        button2 = tk.Button(self, text="Stop", command=lambda: controller.stop)
        button2.pack()


class ConfigurePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Configuration", font=LARGE)
        label.pack(pady=10, padx=10)

        buttons = [tk.Button(self, text=f"Cycle {s.capitalize()}", command=lambda: controller.cycle_sample(s))]
        for b in buttons:
            b.pack()

        button2 = tk.Button(self, text="Play Mode", command=lambda: controller.show_frame(PlayPage))
        button2.pack()


class ViewPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="View Waves", font=LARGE)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Play Mode", command=lambda: controller.show_frame(PlayPage))
        button1.pack()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

