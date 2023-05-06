import math
from typing import Optional, Callable

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QShortcut

from modules.helpers.types.Decorators import override, connector
from modules.models.AudioPlayer import AudioPlayer
from modules.models.view.Background import Background
from modules.models.view.Color import Color
from modules.models.view.builder.FontBuilder import FontBuilder
from modules.models.view.builder.IconButtonStyle import IconButtonStyle
from modules.models.view.builder.SliderStyle import SliderStyle
from modules.models.view.builder.TextStyle import TextStyle
from modules.screens.AbstractScreen import BaseView
from modules.statics.view.Material import Icons, Paddings, Colors, Backgrounds, ColorBoxes, Images
from modules.widgets import Dialogs
from modules.widgets.Buttons import ToggleIconButton, StatelessIconButton, IconButton, ActionButton
from modules.widgets.Cover import CoverProp, Cover
from modules.widgets.Icons import AppIcon
from modules.widgets.Labels import LabelWithDefaultText
from modules.widgets.Sliders import HorizontalSlider


class MusicPlayerRightSide(QHBoxLayout, BaseView):
    __btn_loop: ToggleIconButton
    __btn_shuffle: ToggleIconButton
    __btn_love: ToggleIconButton
    __btn_volume: StatelessIconButton

    __boxes_layout: QHBoxLayout
    __boxes: QWidget
    __slider_volume: HorizontalSlider
    __btn_timer: IconButton

    __onchange_timer: Callable[[int | None], bool] = None

    def __init__(self, parent: Optional["QWidget"] = None):
        super().__init__(parent)
        self.__init_ui()
        self.assign_shortcuts()

    def __init_ui(self) -> None:
        self.__btn_loop = self.__build_option_btn_with_icon(icon=Icons.LOOP)
        self.__btn_shuffle = self.__build_option_btn_with_icon(icon=Icons.SHUFFLE)
        self.__btn_love = self.__build_option_btn_with_icon(
            icon=Icons.LOVE,
            active_icon_color=Colors.DANGER,
            active_background=Backgrounds.CIRCLE_HIDDEN_DANGER_10,
        )
        self.__btn_love.set_change_state_on_pressed(False)

        self.__btn_volume = StatelessIconButton.build(
            size=Icons.LARGE,
            padding=Paddings.RELATIVE_50,
            children=[
                IconButtonStyle(
                    light_mode_icon=Icons.VOLUME_UP.with_color(Colors.PRIMARY),
                    light_mode_background=Backgrounds.CIRCLE_HIDDEN_PRIMARY_10,
                ),
                IconButtonStyle(
                    light_mode_icon=Icons.VOLUME_DOWN.with_color(Colors.PRIMARY),
                    light_mode_background=Backgrounds.CIRCLE_HIDDEN_PRIMARY_10,
                ),
                IconButtonStyle(
                    light_mode_icon=Icons.VOLUME_SILENT.with_color(Colors.PRIMARY),
                    light_mode_background=Backgrounds.CIRCLE_HIDDEN_PRIMARY_10,
                ),
            ],
        )
        self.__btn_volume.set_change_state_on_pressed(False)

        self.__boxes = QWidget()
        self.__boxes_layout = QHBoxLayout(self.__boxes)
        self.__boxes_layout.setContentsMargins(0, 0, 0, 0)

        self.__slider_volume = HorizontalSlider.build(
            height=48,
            light_mode_style=SliderStyle(
                handler_color=ColorBoxes.PRIMARY,
                track_active_color=ColorBoxes.PRIMARY,
                background=Backgrounds.ROUNDED_PRIMARY_10,
            ),
            dark_mode_style=SliderStyle(
                handler_color=ColorBoxes.PRIMARY,
                track_active_color=ColorBoxes.PRIMARY,
                background=Backgrounds.ROUNDED_WHITE_25,
            ),
        )
        self.__slider_volume.setSliderPosition(100)
        self.__boxes_layout.addWidget(self.__slider_volume)

        self.__btn_timer = IconButton.build(
            padding=Paddings.RELATIVE_50,
            size=Icons.LARGE,
            style=IconButtonStyle(
                light_mode_icon=Icons.TIMER.with_color(Colors.PRIMARY),
                light_mode_background=Backgrounds.CIRCLE_HIDDEN_PRIMARY_10
            )
        )

        self.__btn_timer.clicked.connect(self.__open_timer_dialog)
        self.__btn_volume.clicked.connect(
            lambda signal: self.__slider_volume.setVisible(not self.__slider_volume.isVisible()))

        self.addWidget(self.__btn_loop)
        self.addWidget(self.__btn_shuffle)
        self.addWidget(self.__btn_love)
        self.addWidget(self.__btn_volume)
        self.addWidget(self.__boxes, 1)
        self.addWidget(self.__btn_timer)

        self.__timer_dialog = TimerDialog()
        self.__timer_dialog.on_apply_change(lambda minutes: self.__onchange_timer(minutes))

    @override
    def assign_shortcuts(self) -> None:
        loop_shortcut = QShortcut(QKeySequence(Qt.Key_Q), self.__btn_loop)
        loop_shortcut.activated.connect(lambda: self.set_loop(not self.__btn_loop.is_active()))

        shuffle_shortcut = QShortcut(QKeySequence(Qt.Key_W), self.__btn_shuffle)
        shuffle_shortcut.activated.connect(lambda: self.set_shuffle(not self.__btn_shuffle.is_active()))

        love_shortcut = QShortcut(QKeySequence(Qt.Key_E), self.__btn_love)
        love_shortcut.activated.connect(self.__btn_love.click)

    @override
    def apply_light_mode(self) -> None:
        self.__btn_loop.apply_light_mode()
        self.__btn_shuffle.apply_light_mode()
        self.__btn_love.apply_light_mode()
        self.__btn_volume.apply_light_mode()
        self.__btn_timer.apply_light_mode()
        self.__slider_volume.apply_light_mode()
        self.__timer_dialog.apply_light_mode()

    @override
    def apply_dark_mode(self) -> None:
        self.__btn_loop.apply_dark_mode()
        self.__btn_shuffle.apply_dark_mode()
        self.__btn_love.apply_dark_mode()
        self.__btn_volume.apply_dark_mode()
        self.__btn_timer.apply_dark_mode()
        self.__slider_volume.apply_dark_mode()
        self.__timer_dialog.apply_dark_mode()

    @connector
    def set_onclick_loop(self, fn: callable) -> None:
        self.__btn_loop.clicked.connect(lambda: fn())

    @connector
    def set_onclick_shuffle(self, fn: Callable[[bool], None]) -> None:
        self.__btn_shuffle.clicked.connect(lambda: fn(self.is_shuffle()))

    @connector
    def set_onclick_love(self, fn: callable) -> None:
        self.__btn_love.clicked.connect(lambda: fn())

    @connector
    def set_onchange_volume(self, fn: Callable[[int], None]) -> None:
        self.__slider_volume.valueChanged.connect(lambda: self.__onchange_volume(fn))

    @connector
    def set_on_set_timer(self, fn: Callable[[int | None], bool]) -> None:
        self.__onchange_timer = fn

    def set_loop(self, enable: bool) -> None:
        return self.__btn_loop.set_active(enable)

    def set_shuffle(self, enable: bool) -> None:
        return self.__btn_shuffle.set_active(enable)

    def set_love_state(self, is_loved: bool) -> None:
        self.__btn_love.set_active(is_loved)

    def is_looping(self) -> bool:
        return self.__btn_loop.is_active()

    def is_shuffle(self) -> bool:
        return self.__btn_shuffle.is_active()

    def __onchange_volume(self, fn: Callable[[int], None]) -> None:
        volume: int = self.__slider_volume.value()
        self.__change_volume_icon_based_on(volume)
        fn(volume)

    def __change_volume_icon_based_on(self, volume: int) -> None:
        VOLUME_UP_ICON: int = 0
        VOLUME_DOWN_ICON: int = 1
        SILENT_ICON: int = 2
        icon = SILENT_ICON

        if 0 < volume <= 33:
            icon = VOLUME_DOWN_ICON
        if 33 < volume <= 100:
            icon = VOLUME_UP_ICON
        self.__btn_volume.set_state_index(icon)

    def __open_timer_dialog(self) -> None:
        minutes = AudioPlayer.get_instance().get_time_left_to_timer()
        self.__timer_dialog.set_minutes_left(minutes)
        self.__timer_dialog.show()

    @staticmethod
    def __build_option_btn_with_icon(
        icon: AppIcon,
        inactive_icon_color: Color = Colors.GRAY,
        inactive_background: Background = Backgrounds.CIRCLE_HIDDEN_GRAY_25,
        active_icon_color: Color = Colors.PRIMARY,
        active_background: Background = Backgrounds.CIRCLE_HIDDEN_PRIMARY_10
    ) -> ToggleIconButton:
        return ToggleIconButton.build(
            size=Icons.LARGE,
            padding=Paddings.RELATIVE_50,
            active_btn=IconButtonStyle(
                light_mode_icon=icon.with_color(active_icon_color),
                light_mode_background=active_background,
            ),
            inactive_btn=IconButtonStyle(
                light_mode_icon=icon.with_color(inactive_icon_color),
                light_mode_background=inactive_background,
            )
        )


class TimerDialog(Dialogs.Dialog):
    __on_accept_fn: callable = Callable[[str, str], None]

    def __init__(self):
        super().__init__()
        self.__minutes: int = 0
        self.set_minutes_left(0)

    @override
    def _build_content(self) -> None:
        self.__image = Cover()
        self.__image.setAlignment(Qt.AlignHCenter)

        self.__label_time = LabelWithDefaultText.build(
            font=FontBuilder.build(family="Segoe UI Semibold", size=11),
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            dark_mode_style=TextStyle(text_color=ColorBoxes.WHITE),
        )
        self.__label_time.setAlignment(Qt.AlignCenter)

        self.__slider_time = HorizontalSlider.build(
            height=16,
            light_mode_style=SliderStyle(
                handler_color=ColorBoxes.PRIMARY,
                track_active_color=ColorBoxes.PRIMARY,
            ),
            dark_mode_style=SliderStyle(
                handler_color=ColorBoxes.PRIMARY,
                track_active_color=ColorBoxes.PRIMARY,
            ),
        )

        self.__slider_time.sliderMoved.connect(self.__change_time)

        self.__accept_btn = ActionButton.build(
            font=FontBuilder.build(family="Segoe UI Semibold", size=11),
            size=QSize(0, 48),
            light_mode=TextStyle(text_color=ColorBoxes.WHITE,
                                 background=Backgrounds.ROUNDED_PRIMARY_75.with_border_radius(8)),
            dark_mode=TextStyle(text_color=ColorBoxes.WHITE, background=Backgrounds.ROUNDED_WHITE_25)
        )
        self.__accept_btn.clicked.connect(lambda: self._on_accepted())

        self.__main_view = QWidget()
        self.__main_view.setContentsMargins(24, 24, 24, 24)
        self.__view_layout = QVBoxLayout(self.__main_view)
        self.__view_layout.setContentsMargins(0, 0, 0, 0)
        self.__view_layout.setAlignment(Qt.AlignVCenter)
        self.__view_layout.addWidget(self.__image)
        self.__view_layout.addWidget(self.__label_time)
        self.__view_layout.addWidget(self.__slider_time)
        self.__view_layout.addSpacing(8)
        self.__view_layout.addWidget(self.__accept_btn)
        self.addWidget(self.__main_view)

        self.__image.set_cover(CoverProp.from_bytes(Images.TIMER, width=128))
        self.__label_time.setText("Stop playing")
        self.__accept_btn.setText("Set Now")

        self.setFixedWidth(360)
        self.setFixedHeight(self.sizeHint().height())

    @override
    def apply_dark_mode(self) -> None:
        super().apply_dark_mode()
        self.__label_time.apply_dark_mode()
        self.__slider_time.apply_dark_mode()
        self.__accept_btn.apply_dark_mode()

    @override
    def apply_light_mode(self) -> None:
        super().apply_light_mode()
        self.__label_time.apply_light_mode()
        self.__slider_time.apply_light_mode()
        self.__accept_btn.apply_light_mode()

    @connector
    def on_apply_change(self, fn: Callable[[int], bool]) -> None:
        self.__on_accept_fn = fn

    def set_minutes_left(self, minutes: float) -> None:
        if minutes is None:
            self.__minutes = None
            self.__label_time.setText(f"Stop playing")
            self.__slider_time.setValue(0)
        else:
            self.__minutes = int(math.ceil(minutes))
            self.__label_time.setText(f"Stop after {self.__minutes} minutes")
            self.__slider_time.setValue(self.__minutes * 98 // 90)

    def __change_time(self) -> None:
        minutes = int(self.__slider_time.value() / 98 * 90)
        if minutes == 0:
            self.__minutes = None
            self.__label_time.setText(f"Stop playing")
        else:
            self.__minutes = minutes
            self.__label_time.setText(f"Stop after {minutes} minutes")

    def _on_accepted(self) -> None:
        if self.__on_accept_fn is None:
            super().__on_accept_fn()
            self.close()
            return

        can_close = self.__on_accept_fn(None if self.__minutes == 0 else self.__minutes)
        if can_close:
            self.close()
