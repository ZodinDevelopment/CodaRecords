import numpy as np
import sounddevice as sd
import time
import tkinter as tk


def play():
    play_button.config(text="Wait", state="disabled")
    play_button.update()


    def tremolo():
        trem_adder = 1.0 - trem_amount_value
        return np.sin(x * trem_speed) * trem_amount_value + trem_adder


    def ramp_2_osc():
        return ramp_2 * np.sin(fm * x)


    def lfo_osc_wave(lfo_shape):
        return lfo_shape() * np.sin(fm * x)

    def ramp_3_fm2():
        return ramp_3 * np.sin(fm2 * x)

    def sine_wave(mod):
        y = np.sin(x * freq + mod)
        return y

    def triangle(mod):
        y = 2 / np.pi * np.arcsin(np.sin(freq * x + mod))
        return y

    def noise(ramp):
        y = np.random.normal(0, 0.4, len(x))
        y = np.clip(y, a_min=-1.0, a_max=1.0) * (ramp * 0.1)

        return y


    def lfo():
        return (np.sin(x * speed)) * lfo_amount

    def lfo_pluss():
        y = np.sin(x * speed) * 2 + 1
        yy = np.clip(y, 0.0, 1) * lfo_amount
        return yy

    freq = float(scale_freq.get())
    fm = float(scale_fm.get())
    fm2 = float(scale_fm2.get())
    speed = float(scale_speed.get())
    duration = float(scale_duration.get())
    lfo_amount = float(scale_lfo_amount.get())
    ramp_amount = float(scale_ramp_amount.get())
    trem_speed = float(scale_trem_speed.get())
    vol = float(scale_vol.get())
    trem_amount_value = float(scale_trem_amount.get())
    ramp3_divizor = float(scale_ramp3_size.get())
    roller = int(scale_roll.get())
    fade_size = 5000 + int(duration * sample_rate * float(scale_fade.get()))
    noise_shape = float(scale_noise_shape.get())
    device_arg = device_num.get()

    total_samples = int(duration * sample_rate)

    x = np.linspace(0, duration * 2 * np.pi, total_samples)

    choose = lfo_int.get()
    choose_trem = trem_bool.get()
    choose_fm2 = fm2_bool.get()
    choose_noise = noise_int.get()
    choose_wave = wave_bool.get()

    ramp_3 = np.ones(len(x))
    ramp_3_ramp = np.logspace(1, 0, int(duration * sample_rate // ramp3_divizor))

    ramp_0 = np.logspace(noise_shape, 1, total_samples, base=5)
    ramp_1 = np.logspace(1, noise_shape, total_samples, base=5)
    ramp_2 = np.logspace(0, 1, total_samples) * ramp_amount
    ramp_3[: len(ramp_3_ramp)] = ramp_3_ramp
    fade_ramp = np.linspace(1, 0, fade_size if fade_size < 120000 else 120000)
    
    # 
    if choose_wave is True:
        if choose_fm2 is False:
            if choose is 0:
                waveform = r

