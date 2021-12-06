from sys import path

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton

from .button import Button

path.append(".lib/modules/")
from modules.screens.qss.qss_elements import QSSPadding
from modules.screens.themes.button_theme_builder import StandardIconButtonThemeBuilder


class IconButton(Button):
    def render(
        self,
        icon: QIcon,
        size: QSize,
        padding: QSSPadding,
        parent=None,
    ) -> QPushButton:
        button = QPushButton(parent)
        button.setIcon(icon)
        button.setIconSize(size - padding.getWidth(size))
        button.setFixedSize(size)
        return button

    def getThemeBuilder(self):
        return StandardIconButtonThemeBuilder()
