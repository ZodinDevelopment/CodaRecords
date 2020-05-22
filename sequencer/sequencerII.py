import os
import sys
import time
import numpy as np
import sounddevice as sd
import wavio
from PyQt5.QtWidgets import QMainWindow, QPushButton, QCheckBox, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QApplication
from PyQt5.QtCore import Qt



class SequencerApp(QMainWindow):

    def __init__(self):
        super().__init__()

        self.init_sounds()
        self.initUI()


    def initUI(self):
        self.measure = 8
        self.tempo = 120
        num_sounds = 16
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        self.boxes = []
        for i in range(num_sounds):

            checkboxes = [QCheckBox(f'{b}', self) for b in range(0,self.measure - 1)]

            hbox = QHBoxLayout()
            hbox.addStretch(1)
            for box in checkboxes:
                hbox.addWidget(box)


            self.boxes.append(hbox)

        for box in self.boxes:
            vbox.addLayout(box)

        self.setLayout(vbox)
        self.setGeometry(800, 600, 300, 150)

        self.show()


    def init_sounds(self):

        files = os.listdir('808')

        sounds = []

        for f in files:

            data = wavio.read(os.path.join('808', f))

            sounds.append(data)
o
        self.sounds = sounds


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = SequencerApp()
    sys.exit(app.exec_())



