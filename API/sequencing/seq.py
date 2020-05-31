import threading 
import mido
import pygame
import glob
import numpy as np
import os
import sys
import subprocess


class Data():
    def __init__(self, *args, **kwargs):
        # stores point in sequence and BPN
        self.time = 120
        self.started = False
        self.tick = 31
        super().__init__(*args, **kwargs)


class Sequencer(threading.Thread):
    def __init__(self, event):
        threading.Thread.__init__(self)
        self.stopped = event
        threading.Thread.daemon = True

    def run(self):
        while not self.stopped.wait((60000/d.time) / 5000):
            if d.started == True:
                seqAdvance()
                # call a function


class ThreadedMidi(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.daemon = True
        self.start()
    def run(self):
        # get mido going
        ins = mido.get_input_names()
        print(ins)
        inport = mido.open_input(ins[0])
        for msg in inport:
            print(msg)
            if msg.type != "program_change":
                if msg.type == "note_on":
                    playSound(msg.note)
            else:
                toggleSeq()


# Functions
def playSound(note):
    # takes a note integer, plays note and assigns it to sequence
    global delCur;
    global OVRHT;
    tok = d.tick
    i = 0;
    makeNoise(note)
    if d.started == True:
        if delCur == False:
            if OVRHT == True:
                while i < 5:
                    if i < 4:
                        if seq[i][tok] == 0:
                            if re == True:
                                if d.tick % 2: 
                                    seq[i][tok - 1] = note
                                else:
                                    seq[i][tok] = note
                            else:
                                seq[i][d.tick] = note
                            break
                        if seq[i][d.tick] == note:
                            break
                    else:
                        # first in is the first out
                        seq[1][d.tick] = seq[0][d.tick]
                        seq[2][d.tick] = seq[1][d.tick]
                        seq[3][d.tick] = seq[2][d.tick]
                        seq[0][d.tick] = note
                    i += 1



def makeNoise(note):
    j = 0
    while j < len(noteList):
        if note == noteList[j]:
            cha[j].play(s[j])
            break
        j += 1


def toggleSeq():
    # turns sequence on and off
    if d.started == True:
        d.started = 0
        print(d.started)
    else:
        d.started = 1


def seqAdvance():
    # function cycles through the sequence
    if d.tick < seqSize - 1:
        d.tick += 1
    else:
        d.tick = 0
    if met == True:
        if d.tick == 0 or d.tick == 8 or d.tick == 16 or d.tick == 24:
            if d.tick == 0:
                pygame.mixer.Channel(8).set_volume(1)
                pygame.mixer.Channel(8).play(metro)
            else:
                pygame.mixer.Channel(8).set_volume(.4)
                pygame.mixer.Channel(8).play(metro)
    if seq[0][d.tick] != 0:
        makeNoise(seq[0][d.tick])
    if seq[1][d.tick] != 0:
        makeNoise(seq[1][d.tick])
    if seq[2][d.tick] != 0:
        makeNoise(seq[2][d.tick])
    if seq[3][d.tick] != 0:
        makeNoise(seq[3][d.tick])


def recall(sequenceNum, re):
    if re == True:
        print("recalled sequence: {}".format(str(sequenceNum)))
        seq[0] = sav[sequenceNum][0]
        seq[1] = sav[sequenceNum][1]
        seq[2] = sav[sequenceNum][2]
        seq[3] = sav[sequenceNum][3]
    else:
        print("saved sequence: {}".format(str(sequenceNum)))
        sav[sequenceNum][0] = seq[0].copy()
        sav[sequenceNum][1] = seq[1].copy()
        sav[sequenceNum][2] = seq[2].copy()
        sav[sequenceNum][3] = seq[3].copy()


def setWavs(pathnm):
    if re == True:
        pathnm += 9
    if pathnm <= foldNum:
        wavs = glob.glob(paths[pathnm - 1])
        print(f"Loaded Bank {paths[pathnm -1 ]}")
        wavs = sorted(wavs)
        for i in range(len(wavs)):
            if i > 15:
                break
            else:
                s[i] = pygame.mixer.Sound(wavs[i])



# Init pygame mixer
pygame.mixer.pre_init(22050, -16, 8, 512)
pygame.init()

swing = 0
setMidi = False
met = True
# get wavs from current folder 
chnWav = False
foldNum = 1 # change to number of subfolders
paths = [0] * foldNum
extension = '/*.wav'
iya = 0
for root, dirs, files in os.walk('.'):
    for dir in dirs:
        print(dir)
        paths[iya] = (dir + extension)
        iya += 1


wavs = glob.glob(paths[0])
wavs = sorted(wavs)
mets = glob.glob('*.wav')

# midi note numbers
noteList = [36, 38, 40, 41, 43, 45, 47, 48, 50, 52, 53, 55, 57, 59, 60, 62]
# SEQUENCER SIZE
seqSize = 32
#  sequences
delCur = False
stopper = False
OVRHT = False
seq = np.zeros(shape=(4,seqSize))
sav = np.zeros(shape=(7,4,seqSize))

# setup main variables
d = Data()

# setup sequencer class
stopFlag = threading.Event()
sequence = Sequencer(stopFlag)
sequence.start()
pygame.mixer.set_num_channels(9)

# setup arrays for channels and soundfiles
s = [0] * 16
cha = [0] * 16

metro = pygame.mixer.Sound(mets[0])

for i in range(len(wavs)):
    if i > 15:
        break
    else:
        print(str(i))
        if i > 7:
            cha[i] = pygame.mixer.Channel(i - 8)
        else:
            cha[i] = pygame.mixer.Channel(i)

        s[i] = pygame.mixer.Sound(wavs[i])


# start running midi
tm = ThreadedMidi(name='Play-Thread')
re = True
pygame.display.set_mode()
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP_PLUS:
                if chnWav == True:
                    d.time += 15
                else:
                    if re == False:
                        d.time += 1
                    else:
                        d.time += 5

            if event.key == pygame.K_KP_MINUS:
                if chnWav == True:
                    d.time -= 15
                else:
                    if re == False:
                        d.time -= 1
                    else:
                        d.time -= 5

            if event.key == pygame.K_KP_ENTER:
                toggleSeq()
                d.tick = 31
            if event.key == pygame.K_KP_MULTIPLY:
                chnWav = True

            if event.key == pygame.K_NUMLOCK:
                if chnWav == True:
                    subprocess.call('sudo shutdown -h now', shell=True)
                    pygame.quit()
                    sys.exit()

            if event.key == pygame.K_KP0:
                if re == False:
                    seq[0] = [0] * seqSize
                    seq[1] = [0] * seqSize
                    seq[2] = [0] * seqSize
                    seq[3] = [0] * seqSize
                else:
                    delCur = True

            if event.key == pygame.K_KP_PERIOD:
                re = False
            if event.key == pygame.K_KP8:
                if chnWav == True:
                    setWavs(8)
                else:
                    if met == True:
                        met = False
                    else:
                        met = True
            if event.key == pygame.K_KP9:
                if chnWav == True:
                    setWavs(9)
                else:
                    if OVRHT == True:
                        OVRHT = False
                    else:
                        OVRHT = True

            if event.key == pygame.K_KP1:
                if chnWav == True:
                    setWavs(1)
                else:
                    recall(1,re)

            if event.key == pygame.K_KP2:
                if chnWav == True:
                    setWavs(2)
                else:
                    recall(2,re)

            if event.key == pygame.K_KP3:
                if chnWav == True:
                    setWavs(3)
                else:
                    recall(3,re)

            if event.key == pygame.K_KP4:
                if chnWav == True:
                    setWavs(4)
                else:
                    recall(4,re)
            if event.key == pygame.K_KP5:
                if chnWav == True:
                    setWavs(5)
                else:
                    recall)56
