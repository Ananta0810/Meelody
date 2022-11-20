from typing import Optional, Any, Union

from PyQt5.QtWidgets import QHBoxLayout, QWidget

from modules.models.view.AppIcon import AppIcon
from modules.models.view.builder.IconButtonStyle import IconButtonStyle
from modules.statics.view.Material import Icons, Paddings, Colors, Backgrounds
from modules.widgets.IconButton import IconButton
from modules.widgets.StatelessIconButton import StatelessIconButton
from modules.widgets.ToggleIconButton import ToggleIconButton


class MusicPlayerRightSide(QHBoxLayout):
    timer_btn: IconButton
    right_boxes: QHBoxLayout
    inputs: QWidget
    volume_btn: StatelessIconButton
    loveBtn: ToggleIconButton
    shuffle_btn: ToggleIconButton
    loop_btn: ToggleIconButton

    def __init__(self, parent: Optional["QWidget"] = None):
        super(MusicPlayerRightSide, self).__init__(parent)
        self.setup_ui()

    def setup_ui(self) -> None:
        self.loop_btn = self.__build_btn_with_icon(Icons.LOOP)
        self.shuffle_btn = self.__build_btn_with_icon(Icons.SHUFFLE)
        self.loveBtn = self.__build_btn_with_icon(Icons.LOVE)

        self.volume_btn = StatelessIconButton.build(
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
        self.volume_btn.set_change_state_on_pressed(False)

        self.inputs = QWidget()
        self.right_boxes = QHBoxLayout(self.inputs)
        self.right_boxes.setContentsMargins(0, 0, 0, 0)

        self.timer_btn = IconButton.build(
            padding=Paddings.RELATIVE_50,
            size=Icons.LARGE,
            style=IconButtonStyle(
                light_mode_icon=Icons.TIMER.with_color(Colors.PRIMARY),
                light_mode_background=Backgrounds.CIRCLE_HIDDEN_PRIMARY_25
            )
        )

        self.addWidget(self.loop_btn)
        self.addWidget(self.shuffle_btn)
        self.addWidget(self.loveBtn)
        self.addWidget(self.volume_btn)
        self.addWidget(self.inputs, 1)
        self.addWidget(self.timer_btn)

    def apply_light_mode(self) -> None:
        self.loop_btn.apply_light_mode()
        self.shuffle_btn.apply_light_mode()
        self.loveBtn.apply_light_mode()
        self.volume_btn.apply_light_mode()
        self.timer_btn.apply_light_mode()

    def apply_dark_mode(self) -> None:
        self.loop_btn.apply_dark_mode()
        self.shuffle_btn.apply_dark_mode()
        self.loveBtn.apply_dark_mode()
        self.volume_btn.apply_dark_mode()
        self.timer_btn.apply_dark_mode()

    @staticmethod
    def __build_btn_with_icon(icon: AppIcon) -> ToggleIconButton:
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
