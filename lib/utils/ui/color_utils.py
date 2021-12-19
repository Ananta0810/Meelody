from sys import path

path.append(".lib/modules/")
from modules.screens.qss.qss_elements import Color
from PyQt5.QtGui import QColor


class ColorUtils:
    @staticmethod
    def getQColorFromColor(color: Color) -> QColor:
        return QColor(color.red, color.green, color.blue, color.alpha * 255)
