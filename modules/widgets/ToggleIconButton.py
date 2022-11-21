from typing import Self

from PyQt5.QtCore import QSize, QObject

from modules.models.view.Padding import Padding
from modules.models.view.builder.IconButtonStyle import IconButtonStyle
from modules.statics.view.Material import Paddings, Cursors
from modules.widgets.StatelessIconButton import StatelessIconButton, StatelessIconButtonThemeData


class ToggleIconButton(StatelessIconButton):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_active: bool = True

    def set_active(self, active: bool) -> None:
        self._is_active = active
        self.set_state_index(0 if active else 1)
        super()._change_button_based_on_state()

    def set_active_btn(self, button: StatelessIconButtonThemeData) -> None:
        if len(self._children) > 0:
            self._children[0] = button
            return
        self._children.append(button)

    def set_inactive_btn(self, button: StatelessIconButtonThemeData) -> None:
        if len(self._children) > 1:
            self._children[1] = button
            return
        self._children.append(button)

    def set_buttons(self, active_button: StatelessIconButtonThemeData, inactive_button: StatelessIconButtonThemeData) -> None:
        self.set_active_btn(active_button)
        self.set_inactive_btn(inactive_button)

    def set_change_state_on_pressed(self, a0: bool) -> Self:
        self.change_state_on_pressed = a0
        return self

    def is_active(self) -> bool:
        return self._current_index == 0

    def is_inactive(self) -> bool:
        return self._current_index == 1

    @staticmethod
    def build(
        size: QSize,
        active_btn: IconButtonStyle,
        inactive_btn: IconButtonStyle,
        padding: Padding = Paddings.DEFAULT,
        parent: QObject = None,
    ) -> Self:
        button = ToggleIconButton(parent)

        button.set_children([StatelessIconButtonThemeData.of(child, size.width()) for child in [active_btn, inactive_btn]])
        button.set_state_index(0)
        button.setCheckable(True)
        button.setIconSize(size - padding.get_width(size))
        button.setFixedSize(size)
        button.setCursor(Cursors.HAND)

        return button
