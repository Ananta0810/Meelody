from typing import Self

from PyQt5.QtCore import QObject, QSize
from PyQt5.QtWidgets import QPushButton

from modules.models.view.AppIcon import AppIcon
from modules.models.view.Padding import Padding
from modules.models.view.builder.BackgroundThemeBuilder import BackgroundThemeBuilder
from modules.models.view.builder.IconButtonStyle import IconButtonStyle
from modules.statics.view.Apps import Cursors


class IconButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_dark_mode = False
        self.light_mode_icon: AppIcon = None
        self.dark_mode_icon: AppIcon = None
        self.light_mode_background: str = ''
        self.dark_mode_background: str = ''

    def apply_dark_mode(self) -> Self:
        self.is_dark_mode = True
        self.__change_icon_based_on_state()
        return self

    def apply_light_mode(self) -> Self:
        self.is_dark_mode = False
        self.__change_icon_based_on_state()
        return self

    def __change_icon_based_on_state(self):
        if self.is_dark_mode:
            background: str = self.dark_mode_background or self.light_mode_background
            self.setStyleSheet(background)
            self.setIcon((self.dark_mode_icon or self.light_mode_icon))
        else:
            self.setStyleSheet(self.light_mode_background)
            self.setIcon(self.light_mode_icon)

    @staticmethod
    def build(
        size: QSize,
        padding: Padding,
        style: IconButtonStyle,
        parent: QObject = None,
    ) -> Self:
        button = IconButton(parent)
        button.light_mode_icon = style.light_mode_icon
        button.dark_mode_icon = style.dark_mode_icon
        button.setIcon(style.light_mode_icon)
        button.setIconSize(size - padding.get_width(size))
        button.setFixedSize(size)
        button.setCursor(Cursors.HAND)

        button.light_mode_background = BackgroundThemeBuilder.build(BackgroundThemeBuilder.BUTTON, size.width(), style.light_mode_background)
        button.dark_mode_background = BackgroundThemeBuilder.build(BackgroundThemeBuilder.BUTTON, size.width(), style.dark_mode_background)
        return button
