from sys import path

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton

path.append("./lib")
from modules.screens.components.view_item import ViewItem
from modules.screens.qss.qss_elements import Padding
from modules.screens.themes.theme_builders import ButtonThemeBuilder
from widgets.multiple_icon_button import QMultipleIconButton
from widgets.toggle_icon_button import QToggleButton


class IconButton(ViewItem):
    def render(
        self,
        icon: QIcon,
        size: QSize,
        padding: Padding,
        parent=None,
    ) -> QPushButton:
        button = QPushButton(parent)
        button.setIcon(icon)
        button.setIconSize(size - padding.getWidth(size))
        button.setFixedSize(size)
        return button

    def getThemeBuilder(self):
        return ButtonThemeBuilder()


class ToggleIconButton(ViewItem):
    def render(
        self,
        size: QSize,
        icon: QIcon,
        checkedIcon: QIcon,
        padding: Padding,
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
        return ButtonThemeBuilder()


class MultiIconButton(ViewItem):
    def render(
        self,
        icons: list[QIcon],
        size: QSize,
        padding: Padding = None,
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
        return ButtonThemeBuilder()
