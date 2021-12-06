from sys import path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider

from .slider import Slider

path.append("./lib")
from modules.screens.qss.qss_elements import QSSBackground, ColorBox


class HorizontalSlider(Slider):
    def render(
        self,
        height: int,
        handleColor: ColorBox,
        lineColor: ColorBox,
        background: QSSBackground = None,
        handleSize: int = 10,
        lineSize: int = 2,
        parent=None,
    ) -> QSlider:
        slider: QSlider = QSlider(parent)
        slider.setOrientation(Qt.Horizontal)
        slider.setFixedHeight(height)

        lineRadius = lineSize // 2
        lineMargin = (height - lineSize) // 2
        handleMargin = (height - handleSize) // 2

        styleSheet = "QSlider::groove{border:none}"
        if background is not None:
            styleSheet += (
                "QSlider{"
                + f"    background-color:{background.colorStyleSheet()};"
                + f"    border:{background.borderStyleSheet()};"
                + f"    border-radius:{background.borderRadiusStyleSheet(height)}"
                + "}"
                + "QSlider::hover{"
                + f"     border:{background.borderStyleSheet(True)};"
                + f"    background:{background.colorStyleSheet(True)};"
                + "}"
            )
        styleSheet += (
            "QSlider::add-page{"
            + "     border:none;"
            + f"    background:{lineColor.toStylesheet()};"
            + f"    border-radius:{lineRadius}px;"
            + f"    margin:{lineMargin}px {handleMargin}px {lineMargin}px 0px"
            + "}"
            + "QSlider::sub-page{"
            + "     border:none;"
            + f"    background:{handleColor.toStylesheet()};"
            + f"    border-radius:{lineRadius}px;"
            + f"    margin:{lineMargin}px 0px {lineMargin}px {handleMargin + 1}px"
            + "}"
            + "QSlider::handle{"
            + "    border:none;"
            + f"    background:{handleColor.toStylesheet()};"
            + f"    border-radius:{handleSize // 2}px;"
            + f"    width:{handleSize}px;"
            + f"    margin:{handleMargin}px {handleMargin + 1}px"
            + "}"
            + "QSlider::handle:hover{"
            + f"    background:{handleColor.toStylesheet(True)};"
            + f"    width:{handleSize + 2}px;"
            + f"    border-radius:{handleSize // 2 + 1}px;"
            + f"    margin:{handleMargin - 1}px {handleMargin}px"
            + "}"
        )
        slider.setStyleSheet(styleSheet)
        return slider
