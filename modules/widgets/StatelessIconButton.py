from typing import Self

from PyQt5.QtCore import QSize, QObject
from PyQt5.QtWidgets import QPushButton

from modules.helpers.types.Decorators import override
from modules.models.view.AppIcon import AppIcon
from modules.models.view.Padding import Padding
from modules.models.view.builder.BackgroundThemeBuilder import BackgroundThemeBuilder
from modules.models.view.builder.IconButtonStyle import IconButtonStyle
from modules.statics.view.Material import Cursors, Paddings
from modules.views.ViewComponent import ViewComponent


class StatelessIconButtonThemeData:
    light_mode_icon: AppIcon
    light_mode_background: str
    dark_mode_icon: AppIcon
    dark_mode_background: str

    def __init__(
        self,
        light_mode_icon: AppIcon,
        light_mode_background: str,
        dark_mode_icon: AppIcon = None,
        dark_mode_background: str = None
    ):
        self.light_mode_icon = light_mode_icon
        self.light_mode_background = light_mode_background

        self.dark_mode_icon = dark_mode_icon or light_mode_icon
        self.dark_mode_background = dark_mode_background or light_mode_background

    @staticmethod
    def of(data: IconButtonStyle, icon_size: float) -> Self:
        return StatelessIconButtonThemeData(
            data.light_mode_icon,
            BackgroundThemeBuilder.build(BackgroundThemeBuilder.BUTTON, icon_size, data.light_mode_background),
            data.dark_mode_icon,
            BackgroundThemeBuilder.build(BackgroundThemeBuilder.BUTTON, icon_size, data.dark_mode_background),
        )


class StatelessIconButton(QPushButton, ViewComponent):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._children: list[StatelessIconButtonThemeData] = []
        self._current_index = 0
        self._change_state_on_pressed = True
        self._is_dark_mode = False

    def set_children(self, children: list[StatelessIconButtonThemeData]) -> None:
        self._children = children

    def add_child(self, child: StatelessIconButtonThemeData) -> None:
        self._children.append(child)

    def set_change_state_on_pressed(self, a0: bool) -> Self:
        self._change_state_on_pressed = a0
        return self

    @override
    def mousePressEvent(self, event) -> None:
        super().mousePressEvent(event)
        if self._change_state_on_pressed:
            self.to_next_state()

    def set_state_index(self, index: int) -> None:
        if index >= len(self._children):
            return
        self._current_index = index
        self._change_button_based_on_state()

    def to_next_state(self) -> None:
        self.set_state_index((self._current_index + 1) % len(self._children))

    @override
    def apply_light_mode(self):
        self._is_dark_mode = False
        self._change_button_based_on_state()

    @override
    def apply_dark_mode(self):
        self._is_dark_mode = True
        self._change_button_based_on_state()

    def _change_button_based_on_state(self) -> None:
        button = self._children[self._current_index]

        if self._is_dark_mode:
            self.setIcon(button.dark_mode_icon)
            self.setStyleSheet(button.dark_mode_background)
            return

        self.setIcon(button.light_mode_icon)
        self.setStyleSheet(button.light_mode_background)

    @staticmethod
    def build(
        size: QSize,
        children: list[IconButtonStyle],
        padding: Padding = Paddings.DEFAULT,
        parent: QObject = None,
    ) -> Self:
        button = StatelessIconButton(parent)

        button.set_children([StatelessIconButtonThemeData.of(child, size.width()) for child in children])
        button.set_state_index(0)
        button.setCheckable(True)
        button.setIconSize(size - padding.get_width(size))
        button.setFixedSize(size)
        button.setCursor(Cursors.HAND)

        return button
