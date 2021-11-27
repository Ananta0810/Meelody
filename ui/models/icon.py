from sys import path

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon

path.append(".")
from models.color import Color


class Icon:
    def __init__(
        self,
        icon: QIcon,
        size: QSize,
        backgroundColor: Color,
        hoverBackgroundColor: Color,
    ):
        self.icon = icon
        self.size = size
        self.backgroundColor = backgroundColor
        self.hoverBackgroundColor = hoverBackgroundColor
