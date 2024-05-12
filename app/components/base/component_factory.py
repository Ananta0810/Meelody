from typing import final

from PyQt5.QtCore import QSize, QObject
from PyQt5.QtGui import QFont

from app.components.base.buttons import IconButton, ToggleIconButton, MultiStatesIconButton
from app.helpers.stylesheets import Padding, Paddings
from app.resource.qt import Cursors


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
    def createIconButton(size: QSize, padding: Padding = Paddings.DEFAULT, parent: QObject = None) -> IconButton:
        button = IconButton(parent)
        button.setCursor(Cursors.pointer)

        button.setIconSize(size - padding.getWidth(size))
        button.setFixedSize(size)

        return button

    @staticmethod
    def createToggleButton(size: QSize, padding: Padding = Paddings.DEFAULT, parent: QObject = None) -> ToggleIconButton:
        button = ToggleIconButton(parent)
        button.setCursor(Cursors.pointer)

        button.setIconSize(size - padding.getWidth(size))
        button.setFixedSize(size)

        return button

    @staticmethod
    def createMultiStatesButton(size: QSize, padding: Padding = Paddings.DEFAULT, parent: QObject = None) -> MultiStatesIconButton:
        button = MultiStatesIconButton(parent)
        button.setCursor(Cursors.pointer)

        button.setIconSize(size - padding.getWidth(size))
        button.setFixedSize(size)

        return button
