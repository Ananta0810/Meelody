from typing import Optional

from PyQt5.QtWidgets import QHBoxLayout, QWidget

from modules.helpers.types.Decorators import override
from modules.models.view.AppIcon import AppIcon
from modules.models.view.Background import Background
from modules.models.view.Color import Color
from modules.models.view.builder.IconButtonStyle import IconButtonStyle
from modules.models.view.builder.SliderStyle import SliderStyle
from modules.statics.view.Material import Icons, Paddings, Colors, Backgrounds, ColorBoxes
from modules.views.ViewComponent import ViewComponent
from modules.widgets.HorizontalSlider import HorizontalSlider
from modules.widgets.IconButton import IconButton
from modules.widgets.StatelessIconButton import StatelessIconButton
from modules.widgets.ToggleIconButton import ToggleIconButton


class MusicPlayerRightSide(QHBoxLayout, ViewComponent):
    __btn_loop: ToggleIconButton
    __btn_shuffle: ToggleIconButton
    __btn_love: ToggleIconButton
    __btn_volume: StatelessIconButton

    __right_boxes: QHBoxLayout
    __inputs: QWidget
    __slider_volume: HorizontalSlider
    __btn_timer: IconButton

    def __init__(self, parent: Optional["QWidget"] = None):
        super(MusicPlayerRightSide, self).__init__(parent)
        self.__init_ui()

    def __init_ui(self) -> None:
        self.__btn_loop = self.__build_option_btn_with_icon(icon=Icons.LOOP)
        self.__btn_shuffle = self.__build_option_btn_with_icon(icon=Icons.SHUFFLE)
        self.__btn_love = self.__build_option_btn_with_icon(
            icon=Icons.LOVE,
            active_icon_color=Colors.DANGER,
            active_background=Backgrounds.CIRCLE_HIDDEN_DANGER_25,
        )

        self.__btn_volume = StatelessIconButton.build(
            size=Icons.LARGE,
            padding=Paddings.RELATIVE_50,
            children=[
                IconButtonStyle(
                    light_mode_icon=Icons.VOLUME_UP.with_color(Colors.PRIMARY),
                    light_mode_background=Backgrounds.CIRCLE_HIDDEN_PRIMARY_25,
                ),
                IconButtonStyle(
                    light_mode_icon=Icons.VOLUME_DOWN.with_color(Colors.PRIMARY),
                    light_mode_background=Backgrounds.CIRCLE_HIDDEN_PRIMARY_25,
                ),
                IconButtonStyle(
                    light_mode_icon=Icons.VOLUME_SILENT.with_color(Colors.PRIMARY),
                    light_mode_background=Backgrounds.CIRCLE_HIDDEN_PRIMARY_25,
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
                background=Backgrounds.ROUNDED_PRIMARY_25,
            ),
            dark_mode_style=SliderStyle(
                handler_color=ColorBoxes.PRIMARY,
                track_active_color=ColorBoxes.PRIMARY,
                background=Backgrounds.ROUNDED_WHITE_25,
            ),
        )
        self.__slider_volume.setSliderPosition(100)
        self.__slider_volume.valueChanged.connect(self.__change_volume_icon)
        self.__right_boxes.addWidget(self.__slider_volume)

        self.__btn_timer = IconButton.build(
            padding=Paddings.RELATIVE_50,
            size=Icons.LARGE,
            style=IconButtonStyle(
                light_mode_icon=Icons.TIMER.with_color(Colors.PRIMARY),
                light_mode_background=Backgrounds.CIRCLE_HIDDEN_PRIMARY_25
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

    def __change_volume_icon(self) -> None:
        volume: int = self.__slider_volume.value()

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
        active_background: Background = Backgrounds.CIRCLE_HIDDEN_PRIMARY_25
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
