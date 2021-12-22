from sys import path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider

path.append("./lib")
from modules.screens.components.view_item import ViewItem
from modules.screens.themes.theme_builder import ThemeBuilder
from modules.screens.themes.theme_builders import HorizontalSliderThemeBuilder


class HorizontalSlider(ViewItem):
    def render(
        height: int,
        parent=None,
    ) -> QSlider:
        slider: QSlider = QSlider(parent)
        slider.setOrientation(Qt.Horizontal)
        slider.setMaximumHeight(height)
        return slider

    def getThemeBuilder() -> ThemeBuilder:
        return HorizontalSliderThemeBuilder()
