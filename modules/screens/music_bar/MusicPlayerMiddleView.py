from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout, QWidget

from modules.helpers.types.Decorators import override
from modules.helpers.types.Strings import Strings
from modules.models.view.builder.FontBuilder import FontBuilder
from modules.models.view.builder.SliderStyle import SliderStyle
from modules.models.view.builder.TextStyle import TextStyle
from modules.statics.view.Material import ColorBoxes
from modules.screens.AbstractScreen import BaseView
from modules.widgets.HorizontalSlider import HorizontalSlider
from modules.widgets.LabelWithDefaultText import LabelWithDefaultText


class MusicPlayerMiddleView(QHBoxLayout, BaseView):
    __label_playing_time: LabelWithDefaultText
    __slider_time: HorizontalSlider
    __label_total_time: LabelWithDefaultText

    def __init__(self, parent: Optional["QWidget"] = None) -> None:
        super(MusicPlayerMiddleView, self).__init__(parent)
        self._total_time: int = 0
        self.__init_ui()

    def __init_ui(self) -> None:
        font: QFont = FontBuilder.build(size=9)

        self.__label_playing_time = LabelWithDefaultText.build(
            width=60,
            font=font,
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
        )
        self.__label_playing_time.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.__slider_time = HorizontalSlider.build(
            height=12,
            light_mode_style=SliderStyle(
                handler_color=ColorBoxes.PRIMARY,
                track_active_color=ColorBoxes.PRIMARY,
            ),
            dark_mode_style=SliderStyle(
                handler_color=ColorBoxes.PRIMARY,
                track_active_color=ColorBoxes.PRIMARY,
            ),
        )
        self.__slider_time.setFixedWidth(250)
        self.__slider_time.setMaximum(100)
        self.__slider_time.setProperty("value", 0)
        self.__slider_time.setPageStep(0)

        self.__label_total_time = LabelWithDefaultText.build(
            width=60,
            font=font,
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
        )
        self.__label_total_time.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.addWidget(self.__label_playing_time)
        self.addWidget(self.__slider_time)
        self.addWidget(self.__label_total_time)

    @override
    def apply_light_mode(self) -> None:
        self.__label_playing_time.apply_light_mode()
        self.__slider_time.apply_light_mode()
        self.__label_total_time.apply_light_mode()

    @override
    def apply_dark_mode(self) -> None:
        self.__label_playing_time.apply_dark_mode()
        self.__slider_time.apply_dark_mode()
        self.__label_total_time.apply_dark_mode()

    def set_playing_time(self, time: float) -> None:
        self.__label_playing_time.setText(Strings.float_to_clock_time(time))

    def set_total_time(self, time: float) -> None:
        self._total_time = time
        self.__label_total_time.setText(Strings.float_to_clock_time(time))