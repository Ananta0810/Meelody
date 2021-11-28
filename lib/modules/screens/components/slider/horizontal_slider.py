from sys import path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider

from .slider import Slider

path.append(".")
from lib.modules.screens.background import Background
from lib.modules.screens.background_color import BackgroundColor


class HorizontalSlider(Slider):
    def __init__(
        self,
        lineSize: int = 2,
        lineColor: BackgroundColor = None,
        handleSize: float = 10,
        handleColor: BackgroundColor = None,
        background: Background = None,
    ):
        self.lineSize = lineSize
        self.lineColor = lineColor
        self.handleSize = handleSize
        self.handleColor = handleColor
        self.background = background

    def export(self, height: int, parent=None) -> QSlider:
        slider: QSlider = QSlider(parent)
        slider.setOrientation(Qt.Horizontal)
        slider.setFixedHeight(height)

        background = self.background
        lineSize = self.lineSize
        lineColor = self.lineColor
        handelSize = self.handleSize
        handleColor = self.handleColor

        lineRadius = lineSize // 2
        lineMargin = (height - lineSize) // 2
        handleMargin = (height - handelSize) // 2

        slider.setStyleSheet(
            "QSlider::groove{border:none}"  # This line is to make sure the style work properly
            + "QSlider{"
            + f"    background:{str(background.color.normal) if background is not None else None};"
            + f"    border:{str(background.border) if background is not None else None};"
            + f"    border-radius:{background.roundness if background is not None else None}px"
            + "}"
            + "QSlider::hover{"
            + "     border:none;"
            + f"    background:{str(background.color.hover) if background is not None else None};"
            + "}"
            + "QSlider::sub-page{"
            + "     border:none;"
            + f"    background:{str(handleColor.normal)};"
            + f"    border-radius:{lineRadius}px;"
            + f"    margin:{lineMargin}px 0px {lineMargin}px {handleMargin + 1}px"
            + "}"
            + "QSlider::add-page{"
            + "     border:none;"
            + f"    background:{lineColor.normal};"
            + f"    border-radius:{lineRadius}px;"
            + f"    margin:{lineMargin}px {handleMargin}px {lineMargin}px 0px"
            + "}"
            + "QSlider::handle{"
            + "    border:none;"
            + f"    background:{str(handleColor.normal)};"
            + f"    border-radius:{handelSize // 2}px;"
            + f"    width:{handelSize}px;"
            + f"    margin:{handleMargin}px {handleMargin + 1}px"
            + "}"
            + "QSlider::handle:hover{"
            + f"    background:{str(handleColor.hover) if handleColor.hover is not None else handleColor.normal};"
            + f"    width:{handelSize + 2}px;"
            + f"    border-radius:{handelSize // 2 + 1}px;"
            + f"    margin:{handleMargin - 1}px {handleMargin}px"
            + "}"
        )

        return slider
