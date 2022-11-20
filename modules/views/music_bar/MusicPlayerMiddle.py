from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout, QWidget

from modules.helpers.types.Strings import Strings
from modules.models.view.builder.FontBuilder import FontBuilder
from modules.models.view.builder.SliderStyle import SliderStyle
from modules.models.view.builder.TextStyle import TextStyle
from modules.statics.view.Material import ColorBoxes
from modules.widgets.HorizontalSlider import HorizontalSlider
from modules.widgets.LabelWithDefaultText import LabelWithDefaultText


class MusicPlayerMiddle(QHBoxLayout):
    label_playing_time: LabelWithDefaultText
    slider_time: HorizontalSlider
    label_total_time: LabelWithDefaultText

    def __init__(self, parent: Optional["QWidget"] = None) -> None:
        super(MusicPlayerMiddle, self).__init__(parent)
        self._total_time: int = 0
        self.setup_ui()

    def setup_ui(self) -> None:
        font: QFont = FontBuilder.build(size=9)

        self.label_playing_time = LabelWithDefaultText.build(
            width=128,
            font=font,
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
        )
        self.label_playing_time.setFixedWidth(60)
        self.label_playing_time.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.slider_time = HorizontalSlider.build(
            height=12,
            light_mode_style=SliderStyle(handler_color=ColorBoxes.PRIMARY, line_color=ColorBoxes.PRIMARY),
            dark_mode_style=SliderStyle(handler_color=ColorBoxes.PRIMARY, line_color=ColorBoxes.PRIMARY),
        )
        self.slider_time.setFixedWidth(250)
        self.slider_time.setMaximum(100)
        self.slider_time.setProperty("value", 0)
        self.slider_time.setPageStep(0)

        self.label_total_time = LabelWithDefaultText.build(
            width=128,
            font=font,
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
        )
        self.label_total_time.setFixedWidth(60)
        self.label_total_time.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.addWidget(self.label_playing_time)
        self.addWidget(self.slider_time)
        self.addWidget(self.label_total_time)

    def apply_light_mode(self) -> None:
        self.label_playing_time.apply_light_mode()
        self.slider_time.apply_light_mode()
        self.label_total_time.apply_light_mode()

    def apply_dark_mode(self) -> None:
        self.label_playing_time.apply_dark_mode()
        self.slider_time.apply_dark_mode()
        self.label_total_time.apply_dark_mode()

    def set_playing_time(self, time: float) -> None:
        self.label_playing_time.setText(Strings.float_to_clock_time(time))

    def set_total_time(self, time: float) -> None:
        self._total_time = time
        self.label_total_time.setText(Strings.float_to_clock_time(time))