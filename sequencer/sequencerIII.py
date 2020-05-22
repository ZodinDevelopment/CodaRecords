import os
import sys
import time
import cmd
import numpy as np
import wavio
import sounddevice as sd


class Sequencer(cmd.Cmd):

    def __init__(self):
        super().__init__()
        self.tempo = 120
        files = os.listdir('808')
        self.sounds = []
        for f in files:
            fname = os.path.join('808', f)

            wave = wavio.read(fname)

            self.sounds.append(wave.data)

        self.tempo = 120
        self.sound_select = 0

        self.sequences = [[0 for i in range(8)] for sound in self.sounds]

        #for sound in self.sounds:
          #  self.sequence[self.sounds.index(sound)] = np.zeros((1,8))


    def do_play_sequence(self, sound):
        #sound_index = int(sound)
        beat_duration = 60 / self.tempo

        for index in self.sequences[self.sound_select]:
            if index == 0:
                continue
            else:

                sd.play(self.sounds[self.sound_select], 22050)
            ##print(self.sequence[sound_index].index(beat))
                print(index)
                time.sleep(beat_duration)

        sd.stop()


    def do_show_sequences(self, line):
        print(f'Current Sound: {self.sound_select}')
        for ind, s in enumerate(self.sequences):
            lin = ''
            for b in s:
                if b == 0:
                    lin += '-'

                else:
                    lin += '#'

            print(f'{ind}: {lin}')


    def do_set_sound(self, index):
        try:
            index = int(index)
        except:
            print("Invalid Selection")

        self.sound_select = index
        print(f"Drum {index} selected.")
    def do_set_tempo(self, tempo):
        try:
            tempo = int(tempo)
        except:
            print("Invalid Tempo")

        self.tempo = tempo

        print(f"Tempo adjusted to {tempo} BPM")

    def do_sequence(self, sequence):
        beats = sequence.split('.')
        if len(beats) == 8:
            beats = [int(b) for b in beats]
            self.sequences[self.sound_select] = beats

            print(f"New sequence for drum {self.sound_select}: {beats}")

        else:
            print("Invalid sequence, use format: '0.0.0.0.0.0.0.0")

    def do_EOF(self, line):

        return print

    def postloop(self):
        return



if __name__ == '__main__':
    s = Sequencer()

    s.cmdloop()

