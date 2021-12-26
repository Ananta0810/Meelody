from modules.screens.components.view_item import ViewItem
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider


class HorizontalSlider(ViewItem):
    def render(
        height: int,
        parent=None,
    ) -> QSlider:
        slider: QSlider = QSlider(parent)
        slider.setOrientation(Qt.Horizontal)
        slider.setMaximumHeight(height)
        return slider
