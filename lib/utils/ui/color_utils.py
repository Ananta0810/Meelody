from sys import path

from PyQt5.QtGui import QColor

path.append(".")
from lib.modules.models.color import Color


class ColorUtils:
    @staticmethod
    def getQColorFromColor(color: Color) -> QColor:
        return QColor(color.red, color.green, color.blue, color.alpha * 255)
