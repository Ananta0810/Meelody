from typing import Optional

from constants.ui.theme_builders import SliderThemeBuilders, TextThemeBuilders
from modules.screens.components.font_builder import FontBuilder
from modules.screens.components.labels import LabelWithDefaultText
from modules.screens.components.sliders import HorizontalSlider
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QWidget
from utils.helpers.my_string import Stringify
from views.view import View


class MusicPlayerTimeSlider(QHBoxLayout, View):
    def __init__(self, parent: Optional["QWidget"] = None) -> None:
        super(MusicPlayerTimeSlider, self).__init__(parent)
        self._canRunSlider = True
        self._totalTime = 0
        self.setupUi()
        self.setupConnections()

    def setupUi(self) -> None:
        font = FontBuilder().withSize(9).build()
        labelTheme = TextThemeBuilders.DEFAULT.build()

        self.playingTime = LabelWithDefaultText.render(font)
        self.playingTime.setFixedWidth(60)
        self.playingTime.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.addWidget(self.playingTime)
        self._addThemeForItem(self.playingTime, labelTheme)

        self.timeSlider = HorizontalSlider.render(height=12)
        self.timeSlider.setFixedSize(250, 12)
        self.timeSlider.setMaximum(100)
        self.timeSlider.setProperty("value", 0)
        self.timeSlider.setPageStep(0)
        self.addWidget(self.timeSlider)
        self._addThemeForItem(
            self.timeSlider, theme=SliderThemeBuilders.PRIMARY.build(itemSize=self.timeSlider.height())
        )

        self.totalTime = LabelWithDefaultText.render(font)
        self.totalTime.setFixedWidth(60)
        self.totalTime.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.addWidget(self.totalTime)
        self._addThemeForItem(self.totalTime, labelTheme)

    def setupConnections(self):
        self.timeSlider.sliderPressed.connect(lambda: self.__setCanRunTimeSlider(False))
        self.timeSlider.sliderReleased.connect(lambda: self.__setCanRunTimeSlider(True))

    def setPlayingTime(self, time: float) -> None:
        self.playingTime.setText(Stringify.floatToClockTime(time))
        self.__runTimeSlider(time)

    def setTotalTime(self, time: float) -> None:
        self._totalTime = time
        self.totalTime.setText(Stringify.floatToClockTime(time))

    def getCurrentTime(self) -> float:
        return self.timeSlider.sliderPosition() * self._totalTime / 100

    def __runTimeSlider(self, currentTime: float) -> None:
        if not self._canRunSlider:
            return
        position = 0 if self._totalTime == 0 else int(currentTime * 100 / self._totalTime)
        self.timeSlider.setSliderPosition(position)

    def __setCanRunTimeSlider(self, canRun: bool) -> None:
        self._canRunSlider = canRun
