from PyQt5.QtGui import QFont

from .qss_elements import QSSColor


class QSSFont:
    def __init__(self, font: QFont, color: QSSColor):
        self.font = font
        self.color = color
