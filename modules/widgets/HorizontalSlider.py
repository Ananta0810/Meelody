from typing import Self, Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider, QWidget

from modules.helpers.types.Decorators import override
from modules.models.view.builder.HorizontalSliderThemeBuilder import HorizontalSliderThemeBuilder
from modules.models.view.builder.SliderStyle import SliderStyle
from modules.views.ViewComponent import ViewComponent


class HorizontalSlider(QSlider, ViewComponent):

    def __init__(self, parent: Optional["QWidget"] = None):
        QSlider.__init__(self, parent)
        self.light_mode_style: str = ''
        self.dark_mode_style: str = ''

    @override
    def apply_light_mode(self):
        self.setStyleSheet(self.light_mode_style)

    @override
    def apply_dark_mode(self):
        self.setStyleSheet(self.dark_mode_style)

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
        slider.light_mode_style = HorizontalSliderThemeBuilder.build(style=light_mode_style, item_size=height)
        slider.dark_mode_style = HorizontalSliderThemeBuilder.build(style=dark_mode_style, item_size=height)
        return slider
