from typing import Optional, Callable

from PyQt5.QtWidgets import QHBoxLayout, QWidget

from modules.helpers.types.Decorators import override, connector
from modules.widgets.Icons import AppIcon
from modules.models.view.Background import Background
from modules.models.view.Color import Color
from modules.models.view.builder.IconButtonStyle import IconButtonStyle
from modules.models.view.builder.SliderStyle import SliderStyle
from modules.statics.view.Material import Icons, Paddings, Colors, Backgrounds, ColorBoxes
from modules.screens.AbstractScreen import BaseView
from modules.widgets.Sliders import HorizontalSlider
from modules.widgets.Buttons import ToggleIconButton, StatelessIconButton, IconButton


class MusicPlayerRightSideView(QHBoxLayout, BaseView):
    __btn_loop: ToggleIconButton
    __btn_shuffle: ToggleIconButton
    __btn_love: ToggleIconButton
    __btn_volume: StatelessIconButton

    __right_boxes: QHBoxLayout
    __inputs: QWidget
    __slider_volume: HorizontalSlider
    __btn_timer: IconButton

    def __init__(self, parent: Optional["QWidget"] = None):
        super(MusicPlayerRightSideView, self).__init__(parent)
        self.__init_ui()

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

        self.__inputs = QWidget()
        self.__right_boxes = QHBoxLayout(self.__inputs)
        self.__right_boxes.setContentsMargins(0, 0, 0, 0)

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
        self.__right_boxes.addWidget(self.__slider_volume)

        self.__btn_timer = IconButton.build(
            padding=Paddings.RELATIVE_50,
            size=Icons.LARGE,
            style=IconButtonStyle(
                light_mode_icon=Icons.TIMER.with_color(Colors.PRIMARY),
                light_mode_background=Backgrounds.CIRCLE_HIDDEN_PRIMARY_10
            )
        )
        self.__btn_volume.clicked.connect(
            lambda signal: self.__slider_volume.setVisible(not self.__slider_volume.isVisible()))

        self.addWidget(self.__btn_loop)
        self.addWidget(self.__btn_shuffle)
        self.addWidget(self.__btn_love)
        self.addWidget(self.__btn_volume)
        self.addWidget(self.__inputs, 1)
        self.addWidget(self.__btn_timer)

    @override
    def apply_light_mode(self) -> None:
        self.__btn_loop.apply_light_mode()
        self.__btn_shuffle.apply_light_mode()
        self.__btn_love.apply_light_mode()
        self.__btn_volume.apply_light_mode()
        self.__btn_timer.apply_light_mode()
        self.__slider_volume.apply_light_mode()

    @override
    def apply_dark_mode(self) -> None:
        self.__btn_loop.apply_dark_mode()
        self.__btn_shuffle.apply_dark_mode()
        self.__btn_love.apply_dark_mode()
        self.__btn_volume.apply_dark_mode()
        self.__btn_timer.apply_dark_mode()
        self.__slider_volume.apply_dark_mode()

    @connector
    def set_onclick_loop(self, fn: callable) -> None:
        self.__btn_loop.clicked.connect(lambda: fn())

    @connector
    def set_onclick_shuffle(self, fn: callable) -> None:
        self.__btn_shuffle.clicked.connect(lambda: fn())

    @connector
    def set_onclick_love(self, fn: callable) -> None:
        self.__btn_love.clicked.connect(lambda: fn())

    @connector
    def set_onchange_volume(self, fn: Callable[[int], None]) -> None:
        self.__slider_volume.valueChanged.connect(lambda: self.__onchange_volume(fn))

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
