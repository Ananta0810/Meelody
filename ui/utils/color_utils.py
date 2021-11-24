from sys import path

path.append(".")
from models.color import Color
from PyQt5.QtGui import QColor, QIcon, QPainter


class ColorUtils:
    @staticmethod
    def getQColorFromColor(color: Color) -> QColor:
        return QColor(color.red, color.green, color.blue, color.alpha * 255)
