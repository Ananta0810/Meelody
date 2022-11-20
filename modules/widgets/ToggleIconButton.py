from typing import Self, overload

from PyQt5.QtCore import QSize, QObject

from modules.models.view.Padding import Padding
from modules.models.view.builder.IconButtonStyle import IconButtonStyle
from modules.statics.view.Material import Paddings
from modules.widgets.StatelessIconButton import StatelessIconButton, StatelessIconButtonThemeData


class ToggleIconButton(StatelessIconButton):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_active: bool = True

    def set_active_btn(self, button: StatelessIconButtonThemeData) -> None:
        if len(self.children) > 0:
            self.children[0] = button
            return
        self.children.append(button)

    def set_inactive_btn(self, button: StatelessIconButtonThemeData) -> None:
        if len(self.children) > 1:
            self.children[1] = button
            return
        self.children.append(button)

    def set_buttons(self, active_button: StatelessIconButtonThemeData, inactive_button: StatelessIconButtonThemeData) -> None:
        self.set_active_btn(active_button)
        self.set_inactive_btn(inactive_button)

    def set_change_state_on_pressed(self, a0: bool) -> Self:
        self.change_state_on_pressed = a0
        return self

    def is_active(self) -> bool:
        return self.current_index == 0

    def is_inactive(self) -> bool:
        return self.current_index == 1

    @staticmethod
    def build(
        size: QSize,
        active_btn: IconButtonStyle,
        inactive_btn: IconButtonStyle,
        padding: Padding = Paddings.DEFAULT,
        parent: QObject = None,
    ) -> Self:
        return StatelessIconButton.build(size, [active_btn, inactive_btn], padding, parent)
