from typing import final

from PyQt5.QtCore import QSize, QObject
from PyQt5.QtGui import QFont

from app.components.base.buttons import IconButton


@final
class Factory:
    @staticmethod
    def createFont(family: str = "Segoe UI", size: int = 9, italic: bool = False, bold: bool = False) -> QFont:
        font = QFont(family)
        font.setPointSize(size)
        font.setItalic(italic)
        font.setBold(bold)
        return font

    @staticmethod
    def createIconButton(size: QSize, parent: QObject = None) -> IconButton:
        button = IconButton(parent)
        # button.setIconSize(size - padding.getWidth(size))
        button.setFixedSize(size)

        return button
