import os
import sys
import time
import cmd
import numpy as np
import simpleaudio as sa
import wave
import wavio


SOUNDS = os.listdir('samples')


class TempoLab(cmd.Cmd):

    def __init__(self):

        super().__init__()
        self.patterns = {}
        self.samples = {}
        self.sample_names = {}
        self.tempo = 120
        self.framerate = 44100
        self.nticks = 8
        self.configure_engine()
        self.current_sound = SOUNDS[0]



    def do_load_sample(self, sound, fname):

        try:

            samples_path = os.path.join('samples', sound)
            sample_path = os.path.join(samples_path, fname.strip())

        except Exception as e:
            print(str(e))
            print("Usage:\n====\n$ load_sample [sound] [filename]")

        with wave.open(sample_path, 'rb') as wav:
            self.framerate = wav.getframerate()
            self.nchannels = wav.getnchannels()
            self.sampwidth = wav.getsampwidth()

            sample = np.frombuffer(wav.readframes(wav.getnframes()), dtype=np.int16)

        self.samples[sound] = sample
        self.sample_names[sound] = fname.strip()

    def configure_engine(self):
        for s in SOUNDS:
            self.patterns[s] = np.zeros((8))
            self.samples[s] = None
        self.tick_duration = 60 / self.tempo
        self.tick_nsamples = self.tick_duration * self.framerate
        self.pattern_duration = self.tick_duration * 8
        self.loop_markers = np.arange(0, self.tick_nsamples * 8, self.tick_nsamples)
        self.playing = False
        self.loops = []

    def do_info(self, line):
        print("INFO\n=======\n")
        print(f'{len(self.loops)} Loops Created')
        print(f'''Tempo: {self.tempo} BPM\nFramerate: {self.framerate}''')


        for s in SOUNDS:
            wavname = self.sample_names.get(s)

            if wavname is not None:
                print(f'{s}: "{wavname}"')

            else:
                print(f'{s}: Not Set')

class TestLab(cmd.Cmd):

    def __init__(self):
        super().__init__()

        self.tempo = 120
        self.framerate = 44100

        self.samples = {}
        self.resolution = 1
        self.nticks = int(8 // self.resolution)
        self.configure_engine()
        self.loops = []
        self.composition = np.zeros((self.tick_nsamples * self.nticks), dtype=np.int16)

    def configure_engine(self):

        self.tick_duration = 60 / self.tempo
        self.tick_duration *= self.resolution

        self.tick_nsamples = int(self.tick_duration * self.framerate)
        self.tick_nsamples = int(self.resolution * self.tick_nsamples)

        self.pattern_nsamples = self.tick_nsamples * self.nticks
        self.pattern_duration = self.tick_duration * self.nticks
        self.loop_markers = np.arange(0, self.tick_nsamples * self.nticks, self.tick_nsamples)

        self.playing = False


    def do_showconfig(self, line):
        print("INFO\n======\n")
        print(f'{len(self.loops)} Loops')
        print(f'''
            Tempo: {self.tempo} BPM\nFramerate: {self.framerate}
        ''')

        for s in SOUNDS:
            if self.samples.get(s) is not None:
                print(f"{s}: Loaded")
            else:
                print(f"{s}: Not Set")

    def do_temposet(self, tempo):
        try:
            tempo = int(tempo)
        except:
            tempo = 120

        self.tempo = tempo

        print(f"Tempo set to {self.tempo}")
        print("Execute 'reload' to reconfigure client")

    def do_reload(self, line):
        self.configure_engine()
        print("Engine configuration reloaded")

    def do_configure(self, sound):
        if sound not in SOUNDS:
            for s in SOUNDS:
                print(s)
            print("Usage: 'configure [sound]'")


        samples_path = os.path.join('samples', sound)
        choices = os.listdir(samples_path)
        for ind, c in enumerate(choices):
            print(f"{ind}: {c}")


        selection = input("Select using the numerals >> ")
        try:
            selection = int(selection)
            fname = choices[selection]

        except:
            print("Invalid selection")
            #self.mainloop()
        sample_path = os.path.join(samples_path, fname)
        with wave.open(sample_path, 'rb') as wav:
            self.nchannels = wav.getnchannels()
            self.sampwidth = wav.getsampwidth()

            sample = np.frombuffer(wav.readframes(wav.getnframes()), dtype=np.int16)
            sample = sample[:self.tick_nsamples]
        self.samples[sound] = sample
        print(f"{sound} loaded with {fname}")


    def do_test(self, sound):
        sample = self.samples.get(sound)
        if sample is not None:
            play_obj = sa.play_buffer(sample, self.nchannels, self.sampwidth, self.framerate)

            time.sleep(2)
            sa.stop_all()
            print("Done")
        else:
            print("No sample loaded")

        #selection = inp
    def do_construct(self, sound):
        pattern = np.zeros((self.nticks))

        print("Enter pattern with format: '+.+..+..'")
        pattern_input = str(input("Enter pattern >> "))
        pattern_input = pattern_input.strip()
        beats = pattern_input
        if len(beats) != self.nticks:
            print(f"Need {self.nticks} ticks")
            self.mainloop()
        for ind, b in enumerate(beats):
            if b == '+':
                pattern[ind] = 1
            elif b == '.':
                pattern[ind] = 0
            else:
                print(f"{ind} tick invalid")
                continue
        self.loops.append(self.render_loop(sound, pattern))
        print("Loop constructed.")
        print(f"{len(self.loops)} loop")
        input()

    def do_unfo(self, loop_ind):

        last = self.loops.pop()
        del last

    def render_loop(self, sound, pattern):
        audio = np.zeros((self.pattern_nsamples), dtype=np.int16)
        sample = self.samples.get(sound)
        if sample is None:
            raise Exception("Error")
        sample_length = len(sample)
        sample = sample[:len(audio)]

        for ind, tick in enumerate(pattern):
            if tick == 1:
                tickpos = self.loop_markers[ind]
                audio[tickpos:sample_length + tickpos] += sample


            else:
                continue

        #audio *= 32767 / np.max(np.abs(audio))
        audio = audio.astype(np.int16)
        sa.play_buffer(audio, self.nchannels, self.sampwidth, self.framerate)
        time.sleep(self.pattern_duration)
        sa.stop_all()
        print("Loop Rendered")
        return audio

    def do_play_all(self,line):
        loops = []
        for loop in self.loops:
            full = [loop for i in range(8)]
            audio = loop
            for i in full:
                audio = np.concatenate((audio, i))
            loops.append(audio)
        plays = [sa.play_buffer(loop, self.nchannels, self.sampwidth, self.framerate) for loop in loops]
        #audio = np.zeros_like(fullplays[0])

        #audio = np.vstack((audio, a))

    def do_playloop(self, loop_ind='all'):
        if loop_ind == 'all':
            self.play_all()
        try:
            ind = int(loop_ind)
            loop = self.loops[ind]
            fullplay = [loop for i in range(8)]
            audio = loop
            for l in fullplay:
                audio = np.concatenate((audio, l))

            self.play_obj = sa.play_buffer(audio, self.nchannels, self.sampwidth, self.framerate)
            self.playing = True


        except:
            print("Oops")

        #while self.playing:
        #    if not self.play_obj.is_playing:
        #        self.play_obj.play()
         #       continue

    def do_stop(self, line):
        sa.stop_all()

    def do_resolution(self, res):
        try:
            res = float(res)
        except:
            pass
        self.resolution = res
        self.nticks = int(8 // self.resolution)
        print("use 'reload' to confirm")

    def do_compose(self, measures):
        audio = np.zeros((self.pattern_nsamples), dtype=np.int16)
        for loop in self.loops:
            audio += loop
        total = audio
        for i in range(int(measures)):
            if i > 1:
                total = np.concatenate((total, audio))

        self.composition = np.concatenate((self.composition, total))

    def do_save(self, fname):
        with wave.open(fname, 'wb') as wf:
            wf.setframerate(self.framerate)
            wf.setnchannels(self.nchannels)
            wf.setsampwidth(self.sampwidth)
            wf.writeframes(self.composition)
            print("saved")
    def do_EOF(self, line):
        print

    def postloop(self):
        return True



if __name__ == "__main__":
    app = TestLab()
    app.cmdloop()

