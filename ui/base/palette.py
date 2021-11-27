from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Palette:
    def __init__(self):
        self.PRIMARY = QPalette()
        self.PRIMARY.setColor(QPalette.Text, Qt.blue)
