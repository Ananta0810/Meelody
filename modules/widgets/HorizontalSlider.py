from typing import Self, Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider, QWidget

from modules.helpers.types.Decorators import override
from modules.models.view.builder.HorizontalSliderThemeBuilder import HorizontalSliderThemeBuilder
from modules.models.view.builder.SliderStyle import SliderStyle
from modules.views.ViewComponent import ViewComponent


class HorizontalSlider(QSlider, ViewComponent):
    __light_mode_style: str
    __dark_mode_style: str

    def __init__(self, parent: Optional["QWidget"] = None):
        QSlider.__init__(self, parent)

    def set_light_mode_style(self, style: str) -> None:
        self.__light_mode_style = style

    def set_dark_mode_style(self, style: str) -> None:
        self.__dark_mode_style = style

    @override
    def apply_light_mode(self):
        self.setStyleSheet(self.__light_mode_style)

    @override
    def apply_dark_mode(self):
        self.setStyleSheet(self.__dark_mode_style)

    @staticmethod
    def build(
        light_mode_style: SliderStyle,
        dark_mode_style: SliderStyle,
        height: int,
        parent: Optional["QWidget"] = None,
    ) -> Self:
        slider: HorizontalSlider = HorizontalSlider(parent)
        slider.setOrientation(Qt.Horizontal)
        slider.setMaximumHeight(height)
        slider.set_light_mode_style(HorizontalSliderThemeBuilder.build(style=light_mode_style, item_size=height))
        slider.set_dark_mode_style(HorizontalSliderThemeBuilder.build(style=dark_mode_style, item_size=height))
        return slider
