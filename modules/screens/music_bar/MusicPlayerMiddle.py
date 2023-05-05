from typing import Optional, Callable

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QShortcut

from modules.helpers import Times
from modules.helpers.types.Decorators import override, connector
from modules.models.view.builder.FontBuilder import FontBuilder
from modules.models.view.builder.SliderStyle import SliderStyle
from modules.models.view.builder.TextStyle import TextStyle
from modules.screens.AbstractScreen import BaseView
from modules.statics.view.Material import ColorBoxes
from modules.widgets.Labels import LabelWithDefaultText
from modules.widgets.Sliders import HorizontalSlider


class MusicPlayerMiddle(QHBoxLayout, BaseView):
    __label_playing_time: LabelWithDefaultText
    __slider_time: HorizontalSlider
    __label_total_time: LabelWithDefaultText

    def __init__(self, parent: Optional["QWidget"] = None) -> None:
        super().__init__(parent)
        self.__total_time: int = 0
        self.__can_run_slider: bool = True
        self.__init_ui()
        self.__slider_time.sliderPressed.connect(lambda: self.__set_can_run_time_slider(False))
        self.__slider_time.sliderReleased.connect(lambda: self.__set_can_run_time_slider(True))
        self.assign_shortcuts()

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
    def assign_shortcuts(self) -> None:
        shortcut_0 = QShortcut(QKeySequence(Qt.Key_0), self.__slider_time)
        shortcut_0.activated.connect(lambda: self.__skip__to(0))

        shortcut_1 = QShortcut(QKeySequence(Qt.Key_1), self.__slider_time)
        shortcut_1.activated.connect(lambda: self.__skip__to(10))

        shortcut_2 = QShortcut(QKeySequence(Qt.Key_2), self.__slider_time)
        shortcut_2.activated.connect(lambda: self.__skip__to(20))

        shortcut_3 = QShortcut(QKeySequence(Qt.Key_3), self.__slider_time)
        shortcut_3.activated.connect(lambda: self.__skip__to(30))

        shortcut_4 = QShortcut(QKeySequence(Qt.Key_4), self.__slider_time)
        shortcut_4.activated.connect(lambda: self.__skip__to(40))

        shortcut_5 = QShortcut(QKeySequence(Qt.Key_5), self.__slider_time)
        shortcut_5.activated.connect(lambda: self.__skip__to(50))

        shortcut_6 = QShortcut(QKeySequence(Qt.Key_6), self.__slider_time)
        shortcut_6.activated.connect(lambda: self.__skip__to(60))

        shortcut_7 = QShortcut(QKeySequence(Qt.Key_7), self.__slider_time)
        shortcut_7.activated.connect(lambda: self.__skip__to(70))

        shortcut_8 = QShortcut(QKeySequence(Qt.Key_8), self.__slider_time)
        shortcut_8.activated.connect(lambda: self.__skip__to(80))

        shortcut_9 = QShortcut(QKeySequence(Qt.Key_9), self.__slider_time)
        shortcut_9.activated.connect(lambda: self.__skip__to(90))

    def __skip__to(self, pos: int) -> None:
        self.__slider_time.setValue(pos)
        self.__slider_time.sliderReleased.emit()

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

    @connector
    def set_onchange_playing_time(self, fn: Callable[[float], None]) -> None:
        self.__slider_time.sliderReleased.connect(
            lambda: fn(self.get_playing_time())
        )

    def set_playing_time(self, time: float) -> None:
        self.__label_playing_time.setText(Times.string_of(time))
        self.__run_time_slider(time)

    def set_total_time(self, time: float) -> None:
        self.__total_time = time
        self.__label_total_time.setText(Times.string_of(time))

    def get_playing_time(self) -> float:
        return self.__slider_time.sliderPosition() * self.__total_time / 100

    def __set_can_run_time_slider(self, enable: bool) -> None:
        self.__can_run_slider = enable

    def __run_time_slider(self, current_time: float) -> None:
        if not self.__can_run_slider:
            return
        position = 0 if self.__total_time == 0 else int(current_time * 100 / self.__total_time)
        self.__slider_time.setSliderPosition(position)
