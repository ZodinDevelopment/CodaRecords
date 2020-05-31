import os
import sys
import time
import wave
import numpy as np
import simpleaudio as sa
import tkinter as tk


LARGE = ('Verdana', 12)
SOUNDS = ['claps', 'closed', 'cymbals', 'fx', 'kicks', 'open', 'toms', 'snares']


class ViperEel(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side='top', fill='both', expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MainPage, PatternPage, ConfigPage):
            frame = F(container, self)

            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        self.patterns = {}
        self.samples = {}
        self.configure()
        '''
        for s in SOUNDS:
            self.patterns[s] = np.zeros((8))
            self.samples[s] = None
            '''
        '''
        self.tempo = 120
        self.framerate = 44100
        self.nticks = 8
        self.tick_duration = 60 / self.tempo
        self.tick_nsamples = self.tick_duration * self.framerate
        self.pattern_duration = self.tick_duration * 8
        #self.framerate = 44100
        self.loop_array = np.arange(0, self.tick_nsamples * 8, self.tick_nsamples)
        self.playing = False
        for s in SOUNDS:
            self.patterns[s] = np.zeros((8))
            self.samples[s] = None
        '''
        self.current_sound = SOUNDS[0]
        self.show_frame(MainPage)

    def load_sample(self, sound, fname):
        samples_path = os.path.join('samples', sound)
        sample_path = os.path.join(samples_path, fname)

        with wave.open(sample_path, 'rb') as wav:
            self.framerate = wav.getframerate()
            self.nchannels = wav.getnchannels()
            self.sampwidth = wav.getsampwidth()

            sample = np.frombuffer(wav.readframes(self.framerate), dtype=np.int16)

        return sample

    def bind_looper_keys(self):
        for i in range(1, 8):
            self.bind(f'<KeyPress-{i}>', self.toggle_tick)

        self.bind('<KeyPress- >', self.toggle_playback)

    def show_frame(self, cont):
        frame = self.frames[cont]

        frame.tkraise()

    def toggle_tick(self, event):
        try:
            index = int(event.char)

        except ValueError:
            print(f'Key {event.char} press')
            index = None

        if index is not None:
            if index >= 1 and index <= 8:
                pattern = self.patterns.get(self.current_sound)
                if pattern[index] == 0:
                    pattern[index] = 1
                    print(f'Position {index} activated for sound {self.current_sound}')

                else:
                    pattern[index] = 0
                    print(f'Position {index} deactivated for sound {self.current_sound}')
                
                self.patterns[self.current_sound] = pattern
                self.toggle_playback()
                #print(f"Position {index} toggled 


    def toggle_playback(self):
        if self.playing:
            sa.stop_all()

        else:
            loop = self.render_loop(self, self.current_sound)
            self.playing = True
            play_obj = sa.play_buffer(loop, self.nchannels, self.sampwidth, self.framerate)
            while self.playing:
                if not play_obj.is_playing():
                    play_obj = sa.play_buffer(loop, self.nchannels, self.sampwidth, self.framerate)
                else:
                    continue

    def render_final(self):
        pass

    def render_loop(self, sound):
        pass

    def sample_selection(self, sound):
        pass

    def change_sound(self, sound):
        pass

    def configure(self):
        pass


class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='ViperEelI', font=LARGE)
        label.pack(pady=10, padx=10)
        

        for s in SOUNDS:
            slabel = tk.Label(self, text=s, font=LARGE)
            slabel.pack(pady=3, padx=3)
            button = tk.Button(self, text='Select Sample', command=lambda: controller.sample_selection(s))
            button.pack()

            button2 = tk.Button(self, text='Activate', command=lambda: controller.change_sound(s))
            
            button2.pack()
        buttonConfig = tk.Button(self, text='Configure', command=lambda: controller.show_frame(ConfigurePage))
        buttonConfig.pack()
        buttonPlay = tk.Button(self, text='Play', command=lambda: controller.toggle_playback())
        buttonPlay.pack()
        buttonFinish = tk.Button(self, text='Render', command=lambda: controller.render_final())
        buttonFinish.pack()


class ConfigPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Configure", font=LARGE)
        label.pack(pady=10, padx=10)

        tempo_val = tk.IntVar()

        spinner = tk.Spinbox(self, from_=80, to=220, textvariable=tempo_val)

        label2 = tk.Label(self, text='Tempo')
        spinner.pack()
        label2.pack(pady=10, padx=10)

        buttonSave = tk.Button(self, text='Confirm', command=lambda: controller.configure())
        buttonSave.pack()

        buttonCancel = tk.Button(Self, text='Cancel', command=lambda: controller.show_frame(MainPage))
        buttonCancel.pack()


class PatternPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        

        label = tk.Label(self, text='In Dev', font=LARGE)
        label.pack(pady=10,padx=10)

        button = tk.Button(self, text="Return", command=lambda: controller.show_frame(MainPage))
        button.pack()



if __name__ == "__main__":
    app = ViperEel()
    app.mainloop()

