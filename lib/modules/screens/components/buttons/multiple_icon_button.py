from sys import path

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton

from .button import Button

path.append("./lib")
from modules.screens.qss.qss_elements import QSSPadding
from modules.screens.themes.button_theme_builder import StandardIconButtonThemeBuilder
from widgets.multiple_icon_button import QMultipleIconButton


class MultiIconButton(Button):
    def render(
        self,
        icons: list[QIcon],
        size: QSize,
        padding: QSSPadding = None,
        parent=None,
    ) -> QPushButton:
        button = QMultipleIconButton(parent)
        button.setIconList(icons)
        button.setCurrentIcon(0)
        if padding is not None:
            button.setIconSize(size - padding.getWidth(size))
        button.setFixedSize(size)
        return button

    def getThemeBuilder(self):
        return StandardIconButtonThemeBuilder()
