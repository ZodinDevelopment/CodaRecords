import numpy as np
from scipy.io.wavfile import write
import sounddevice as sd
import time
import pickle
import os
from PyQt5 import QtWidgets
import mantaUI


class MantaApp(QtWidgets.QMainWindow, mantaUI.Ui_MainWindow):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)


        # hook stuff up under here

    def play(self, save=False):
        """Gets values and selections from gui then plays or saves"""

        #!!!
        # Here implement play button state changes and updates

        def tremolo():
            trem_adder = 1.0 - self.trem_amount_value
            return np.sin(self.x * self.trem_speed) * self.trem_amount_value + trem_adder

        def ramp_2_osc():
            return self.ramp_2 * np.sin(self.fm * self.x)

        def lfo_osc_wave(lfo_shape):
            return lfo_shape() * np.sin(self.fm * self.x)

        def ramp_3_fm2():
            return self.ramp_3 * np.sin(self.fm2 * self.x)

        def sine_wave(mod):
            y = np.sin(self.x * self.freq + mod)
            return y

        def triangle(mod):
            y = 2 / np.pi * np.arcsin(np.sin(self.freq * self.x + mod))
            return y

        def noise(ramp):
            y = np.random.normal(0, 0.4, len(self.x))
            y = np.clip(y, a_min=-1.0, a_max=1.0) * (self.ramp * 0.1)
            return y

        def lfo():
            return (np.sin(self.x * self.speed)) * self.lfo_amount

        def lfo_pluss():
            y = np.sin(self.x * self.speed) * 2 + 1
            yy = np.clip(y, 0.0, 1) * self.lfo_amount

            return yy


        self.freq = float(self.scale_freq.value())
        self.fm = float(self.scale_fm.value())
        self.fm2 = float(self.scale_fm2.value())
        self.speed = float(self.scale_speed.value())
        self.duration = float(self.scale_duration.value())
        self.lfo_amount = float(self.scale_lfo_amount.value())
        self.ramp_amount = float(self.scale_ramp_amount.value())
        self.trem_speed = float(self.scale_trem_speed.value())
        self.vol = float(self.scale_vol.value())
        self.trem_amount_value = float(self.scale_trem_amount_value.value())
        self.ramp3_divizor = float(self.scale_ramp3_divizor.value())
        self.roller = int(self.scale_roller.value())
        self.fade_size = 5000 + int(self.duration * self.sample_rate * float(self.scale_fade.value()))
        self.noise_shape = float(self.scale_noise_shape.value())

        total_samples = int(self.duration * self.sample_rate)
        self.x = np.linspace(0, self.duration * 2 * np.pi, int(self.duration * self.sample_rate))

        self.choose = self.lfo_int.value()
