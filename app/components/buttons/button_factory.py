from typing import final

from PyQt5.QtCore import QSize, QObject

from app.common.statics.qt import Cursors
from app.common.statics.styles import Paddings
from app.helpers.stylesheets import Padding
from .icons_button import MultiStatesIconButton, IconButton, ToggleIconButton


@final
class ButtonFactory:

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
