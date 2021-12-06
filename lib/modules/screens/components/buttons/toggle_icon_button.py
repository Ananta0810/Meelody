from sys import path

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton

from .button import Button

path.append("./lib")
from modules.screens.qss.qss_elements import QSSPadding
from modules.screens.themes.button_theme_builder import ToggleIconButtonThemeBuilder
from widgets.toggle_icon_button import QToggleButton


class ToggleIconButton(Button):
    def render(
        self,
        size: QSize,
        icon: QIcon,
        checkedIcon: QIcon,
        padding: QSSPadding,
        parent=None,
    ) -> QPushButton:
        button = QToggleButton(parent)
        button.setIcon(icon)
        button.setNormalIcon(icon)
        button.setCheckedIcon(checkedIcon)
        button.setCheckable(True)
        button.setIconSize(size - padding.getWidth(size))
        button.setFixedSize(size)
        return button

    def getThemeBuilder(self):
        return ToggleIconButtonThemeBuilder()
