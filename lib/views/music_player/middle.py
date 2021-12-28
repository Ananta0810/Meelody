from typing import Optional

from constants.ui.qss import ColorBoxes
from modules.screens.components.font_builder import FontBuilder
from modules.screens.components.labels import LabelWithDefaultText
from modules.screens.components.sliders import HorizontalSlider
from modules.screens.themes.theme_builders import (
    HorizontalSliderThemeBuilder, LabelThemBuilder)
from PyQt5.QtCore import QMetaObject, Qt
from PyQt5.QtWidgets import QHBoxLayout, QWidget
from utils.helpers.my_string import Stringify
from views.view import View


class MusicPlayerTimeSlider(QHBoxLayout, View):
    def __init__(self, parent: Optional["QWidget"] = None) -> None:
        super(MusicPlayerTimeSlider, self).__init__(parent)
        self.setupUi()

    def setupUi(self) -> None:
        font = FontBuilder().withSize(9).build()
        labelTheme = (
            LabelThemBuilder().addLightModeTextColor(ColorBoxes.GRAY).addDarkModeTextColor(ColorBoxes.WHITE).build()
        )

        self.playingTime = LabelWithDefaultText.render(font)
        self.playingTime.setFixedWidth(60)
        self.playingTime.setAlignment(Qt.AlignRight| Qt.AlignVCenter)
        self.addWidget(self.playingTime)
        self._addThemeForItem(self.playingTime, labelTheme)

        self.timeSlider = HorizontalSlider.render(height=12)
        self.timeSlider.setFixedSize(250, 12)
        self.timeSlider.setProperty("value", 0)
        self.addWidget(self.timeSlider)
        self._addThemeForItem(
            self.timeSlider,
            theme=HorizontalSliderThemeBuilder()
            .addLightHandleColor(ColorBoxes.PRIMARY)
            .addLightLineColor(ColorBoxes.HOVERABLE_PRIMARY_25)
            .addDarkLineColor(ColorBoxes.HOVERABLE_WHITE_25)
            .build(itemSize=self.timeSlider.height()),
        )
        self.totalTime = LabelWithDefaultText.render(font)
        self.totalTime.setFixedWidth(60)
        self.totalTime.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.addWidget(self.totalTime)
        self._addThemeForItem(self.totalTime, labelTheme)

        QMetaObject.connectSlotsByName(self)

    def displayPlayingTime(self, time: float) -> None:
        self.playingTime.setText(Stringify.floatToClockTime(time))

    def displayTotalTime(self, time: float) -> None:
        self.totalTime.setText(Stringify.floatToClockTime(time))

    def runTimeSlider(self, currentTime: float, totalTime: float) -> None:
        TIME_FIX_FOR_CASE_WHEN_DEVIDING_FOR_ZERO: float = 999999.0
        if totalTime == 0:
            totalTime = TIME_FIX_FOR_CASE_WHEN_DEVIDING_FOR_ZERO
        position = int(currentTime * 100 / totalTime)
        self.timeSlider.setSliderPosition(position)

    def getTimeSliderPosition(self) -> int:
        return self.timeSlider.sliderPosition()
