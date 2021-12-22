from abc import ABC, abstractstaticmethod
from sys import path

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton

path.append("./lib")
from modules.screens.components.view_item import ViewItem
from modules.screens.qss.qss_elements import Padding
from modules.screens.themes.theme_builders import ButtonThemeBuilder
from widgets.multiple_icon_button import QMultipleIconButton
from widgets.standard_icon_button import QIconButton
from widgets.toggle_icon_button import QToggleButton


class ViewIconButton(ABC):
    @abstractstaticmethod
    def render():
        pass


class IconButton(ViewItem):
    def render(
        self,
        lightModeIcon: QIcon,
        size: QSize,
        padding: Padding,
        darkModeIcon: QIcon = None,
        parent=None,
    ) -> QPushButton:
        button = QIconButton(parent)
        button.setLightModeIcon(lightModeIcon)
        button.setDarkModeIcon(darkModeIcon)
        button.setIcon(lightModeIcon)
        button.setIconSize(size - padding.getWidth(size))
        button.setFixedSize(size)
        return button

    def getThemeBuilder(self):
        return ButtonThemeBuilder()


class ToggleIconButton(ViewItem):
    def render(
        self,
        size: QSize,
        lightModeIcon: QIcon,
        lightModeCheckedIcon: QIcon,
        padding: Padding,
        darkModeIcon: QIcon = None,
        darkModeCheckedIcon: QIcon = None,
        parent=None,
    ) -> QPushButton:
        button = QToggleButton(parent)
        button.setIcon(lightModeIcon)
        button.setLightModeNormalIcon(lightModeIcon)
        button.setLightModeCheckedIcon(lightModeCheckedIcon)
        button.setDarkModeNormalIcon(darkModeIcon)
        button.setDarkModeCheckedIcon(darkModeCheckedIcon)
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
