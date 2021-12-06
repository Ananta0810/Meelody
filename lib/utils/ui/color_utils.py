from sys import path

from PyQt5.QtGui import QColor

path.append(".lib/modules/")
from modules.screens.qss.qss_elements import Color


class ColorUtils:
    @staticmethod
    def getQColorFromColor(color: Color) -> QColor:
        return QColor(color.red, color.green, color.blue, color.alpha * 255)
