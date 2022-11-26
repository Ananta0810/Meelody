from typing import Self, Optional

from PyQt5.QtCore import QObject, QSize
from PyQt5.QtWidgets import QPushButton, QWidget

from modules.helpers.types.Decorators import override
from modules.widgets.AppIcon import AppIcon
from modules.models.view.Padding import Padding
from modules.models.view.builder.BackgroundThemeBuilder import BackgroundThemeBuilder
from modules.models.view.builder.IconButtonStyle import IconButtonStyle
from modules.statics.view.Material import Cursors
from modules.views.ViewComponent import ViewComponent


class IconButton(QPushButton, ViewComponent):
    __is_dark_mode: bool = False
    __light_mode_icon: AppIcon
    __dark_mode_icon: AppIcon
    __light_mode_background: str
    __dark_mode_background: str

    def __init__(self, parent: Optional["QWidget"] = None):
        super().__init__(parent)

    def set_light_mode_icon(self, icon: AppIcon) -> None:
        self.__light_mode_icon = icon

    def set_dark_mode_icon(self, icon: AppIcon) -> None:
        self.__dark_mode_icon = icon

    def set_light_mode_background(self, style: str) -> None:
        self.__light_mode_background = style

    def set_dark_mode_background(self, style: str) -> None:
        self.__dark_mode_background = style

    @override
    def apply_light_mode(self) -> Self:
        self.__is_dark_mode = False
        self.__change_icon_based_on_state()
        return self

    @override
    def apply_dark_mode(self) -> Self:
        self.__is_dark_mode = True
        self.__change_icon_based_on_state()
        return self

    def __change_icon_based_on_state(self):
        if self.__is_dark_mode:
            background: str = self.__dark_mode_background or self.__light_mode_background
            self.setStyleSheet(background)
            self.setIcon((self.__dark_mode_icon or self.__light_mode_icon))
        else:
            self.setStyleSheet(self.__light_mode_background)
            self.setIcon(self.__light_mode_icon)

    @staticmethod
    def build(
        size: QSize,
        padding: Padding,
        style: IconButtonStyle,
        parent: QObject = None,
    ) -> Self:
        button = IconButton(parent)
        button.setIcon(style.light_mode_icon)
        button.setIconSize(size - padding.get_width(size))
        button.setFixedSize(size)
        button.setCursor(Cursors.HAND)

        button.set_light_mode_icon(style.light_mode_icon)
        button.set_dark_mode_icon(style.dark_mode_icon)
        button.set_light_mode_background(BackgroundThemeBuilder.build(BackgroundThemeBuilder.BUTTON, size.width(), style.light_mode_background))
        button.set_dark_mode_background(BackgroundThemeBuilder.build(BackgroundThemeBuilder.BUTTON, size.width(), style.dark_mode_background))
        return button
