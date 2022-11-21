from typing import Optional

from PyQt5.QtWidgets import QHBoxLayout, QWidget

from modules.models.view.AppIcon import AppIcon
from modules.models.view.builder.IconButtonStyle import IconButtonStyle
from modules.models.view.builder.SliderStyle import SliderStyle
from modules.statics.view.Material import Icons, Paddings, Colors, Backgrounds, ColorBoxes
from modules.widgets.HorizontalSlider import HorizontalSlider
from modules.widgets.IconButton import IconButton
from modules.widgets.StatelessIconButton import StatelessIconButton
from modules.widgets.ToggleIconButton import ToggleIconButton


class MusicPlayerRightSide(QHBoxLayout):
    btn_loop: ToggleIconButton
    btn_shuffle: ToggleIconButton
    btn_love: ToggleIconButton
    btn_volume: StatelessIconButton

    right_boxes: QHBoxLayout
    inputs: QWidget
    slider_volume: HorizontalSlider
    btn_timer: IconButton

    def __init__(self, parent: Optional["QWidget"] = None):
        super(MusicPlayerRightSide, self).__init__(parent)
        self.setup_ui()

    def setup_ui(self) -> None:
        self.btn_loop = self.__build_option_btn_with_icon(Icons.LOOP)
        self.btn_shuffle = self.__build_option_btn_with_icon(Icons.SHUFFLE)
        self.btn_love = self.__build_option_btn_with_icon(Icons.LOVE)

        self.btn_volume = StatelessIconButton.build(
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
        self.btn_volume.set_change_state_on_pressed(False)

        self.inputs = QWidget()
        self.right_boxes = QHBoxLayout(self.inputs)
        self.right_boxes.setContentsMargins(0, 0, 0, 0)

        self.slider_volume = HorizontalSlider.build(
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
        self.slider_volume.setSliderPosition(100)
        self.right_boxes.addWidget(self.slider_volume)

        self.btn_timer = IconButton.build(
            padding=Paddings.RELATIVE_50,
            size=Icons.LARGE,
            style=IconButtonStyle(
                light_mode_icon=Icons.TIMER.with_color(Colors.PRIMARY),
                light_mode_background=Backgrounds.CIRCLE_HIDDEN_PRIMARY_25
            )
        )
        self.btn_volume.clicked.connect(lambda signal: self.slider_volume.setVisible(not self.slider_volume.isVisible()))

        self.addWidget(self.btn_loop)
        self.addWidget(self.btn_shuffle)
        self.addWidget(self.btn_love)
        self.addWidget(self.btn_volume)
        self.addWidget(self.inputs, 1)
        self.addWidget(self.btn_timer)

    def apply_light_mode(self) -> None:
        self.btn_loop.apply_light_mode()
        self.btn_shuffle.apply_light_mode()
        self.btn_love.apply_light_mode()
        self.btn_volume.apply_light_mode()
        self.btn_timer.apply_light_mode()
        self.slider_volume.apply_light_mode()

    def apply_dark_mode(self) -> None:
        self.btn_loop.apply_dark_mode()
        self.btn_shuffle.apply_dark_mode()
        self.btn_love.apply_dark_mode()
        self.btn_volume.apply_dark_mode()
        self.btn_timer.apply_dark_mode()
        self.slider_volume.apply_dark_mode()

    @staticmethod
    def __build_option_btn_with_icon(icon: AppIcon) -> ToggleIconButton:
        return ToggleIconButton.build(
            size=Icons.LARGE,
            padding=Paddings.RELATIVE_50,
            active_btn=IconButtonStyle(
                light_mode_icon=icon.with_color(Colors.PRIMARY),
                light_mode_background=Backgrounds.CIRCLE_HIDDEN_PRIMARY_25,
            ),
            inactive_btn=IconButtonStyle(
                light_mode_icon=icon.with_color(Colors.DANGER),
                light_mode_background=Backgrounds.CIRCLE_HIDDEN_DANGER_25,
            )
        )
