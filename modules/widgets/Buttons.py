from typing import Optional

from PyQt5.QtCore import QSize, QObject
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QPushButton

from modules.helpers.types.Decorators import override
from modules.models.view.Padding import Padding
from modules.models.view.builder.BackgroundThemeBuilder import BackgroundThemeBuilder
from modules.models.view.builder.IconButtonStyle import IconButtonStyle
from modules.models.view.builder.TextStyle import TextStyle
from modules.screens.AbstractScreen import BaseView
from modules.statics.view.Material import Paddings, Cursors
from modules.widgets.Icons import AppIcon


class ActionButton(QPushButton, BaseView):
    padding: Padding = Paddings.DEFAULT

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

    def set_padding(self, padding: Padding) -> None:
        self.padding = padding

    @override
    def setText(self, text: str) -> None:
        super().setText(text)
        self.__padding_text()

    def __padding_text(self) -> None:
        if self.padding is Paddings.DEFAULT:
            return
        textSize = self.sizeHint()
        self.setFixedSize(
            textSize.width() + self.padding.get_width(textSize.width()),
            textSize.height() + self.padding.get_height(textSize.height()),
        )

    def __set_light_mode_background(self, style: str) -> None:
        self.__light_mode_background = style

    def __set_dark_mode_background(self, style: str) -> None:
        self.__dark_mode_background = style

    @override
    def apply_light_mode(self) -> None:
        self.setStyleSheet(self.__light_mode_background)

    @override
    def apply_dark_mode(self) -> None:
        self.setStyleSheet(self.__dark_mode_background)

    @staticmethod
    def build(
        size: QSize,
        font: QFont,
        light_mode: TextStyle,
        dark_mode: TextStyle = None,
        padding: Padding = Paddings.DEFAULT,
        parent: QObject = None,
    ) -> 'ActionButton':
        button = ActionButton(parent)
        button.setFixedSize(size)
        button.setCursor(Cursors.HAND)
        button.set_padding(padding)
        button.setFont(font)

        button.__set_light_mode_background(
            BackgroundThemeBuilder.build(element=BackgroundThemeBuilder.BUTTON,
                                         element_size=size.width(),
                                         background=light_mode.background,
                                         text_color=light_mode.text_color
                                         ))

        dark_mode = dark_mode or light_mode
        button.__set_dark_mode_background(
            BackgroundThemeBuilder.build(element=BackgroundThemeBuilder.BUTTON,
                                         element_size=size.width(),
                                         background=dark_mode.background,
                                         text_color=dark_mode.text_color
                                         ))
        return button


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
    def of(data: IconButtonStyle, icon_size: float) -> 'StatelessIconButtonThemeData':
        return StatelessIconButtonThemeData(
            data.light_mode_icon,
            BackgroundThemeBuilder.build(BackgroundThemeBuilder.BUTTON, icon_size, data.light_mode_background),
            data.dark_mode_icon,
            BackgroundThemeBuilder.build(BackgroundThemeBuilder.BUTTON, icon_size, data.dark_mode_background),
        )


class StatelessIconButton(QPushButton, BaseView):
    _children: list[StatelessIconButtonThemeData] = []
    _current_index: int = 0
    __change_state_on_pressed: bool = True
    __is_dark_mode: bool = False

    def __init__(self, parent: Optional["QWidget"] = None):
        super().__init__(parent)

    def set_children(self, children: list[StatelessIconButtonThemeData]) -> None:
        self._children = children

    def add_child(self, child: StatelessIconButtonThemeData) -> None:
        self._children.append(child)

    def set_change_state_on_pressed(self, a0: bool) -> None:
        self.__change_state_on_pressed = a0

    def set_state_index(self, index: int) -> None:
        if index >= len(self._children):
            return
        self._current_index = index
        self._change_button_based_on_state()

    def to_next_state(self) -> None:
        self.set_state_index((self._current_index + 1) % len(self._children))

    def _change_button_based_on_state(self) -> None:
        button = self._children[self._current_index]

        if self.__is_dark_mode:
            self.setIcon(button.dark_mode_icon)
            self.setStyleSheet(button.dark_mode_background)
            return

        self.setIcon(button.light_mode_icon)
        self.setStyleSheet(button.light_mode_background)

    @override
    def mousePressEvent(self, event) -> None:
        super().mousePressEvent(event)
        if self.__change_state_on_pressed:
            self.to_next_state()

    @override
    def apply_light_mode(self):
        self.__is_dark_mode = False
        self._change_button_based_on_state()

    @override
    def apply_dark_mode(self):
        self.__is_dark_mode = True
        self._change_button_based_on_state()

    @staticmethod
    def build(
        size: QSize,
        children: list[IconButtonStyle],
        padding: Padding = Paddings.DEFAULT,
        parent: QObject = None,
    ) -> 'StatelessIconButton':
        button = StatelessIconButton(parent)

        button.set_children([StatelessIconButtonThemeData.of(child, size.width()) for child in children])
        button.set_state_index(0)
        button.setCheckable(True)
        button.setIconSize(size - padding.get_width(size))
        button.setFixedSize(size)
        button.setCursor(Cursors.HAND)

        return button


class ToggleIconButton(StatelessIconButton):
    __is_active: bool = True

    def __init__(self, parent: Optional["QWidget"] = None):
        super().__init__(parent)

    def set_active(self, active: bool) -> None:
        self.__is_active = active
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

    def set_buttons(self, active_button: StatelessIconButtonThemeData,
                    inactive_button: StatelessIconButtonThemeData) -> None:
        self.set_active_btn(active_button)
        self.set_inactive_btn(inactive_button)

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
    ) -> 'ToggleIconButton':
        button = ToggleIconButton(parent)

        button.set_children(
            [StatelessIconButtonThemeData.of(child, size.width()) for child in [active_btn, inactive_btn]])
        button.set_state_index(0)
        button.setCheckable(True)
        button.set_active(False)
        button.setIconSize(size - padding.get_width(size))
        button.setFixedSize(size)
        button.setCursor(Cursors.HAND)

        return button


class IconButton(QPushButton, BaseView):
    __is_dark_mode: bool = False
    __light_mode_icon: AppIcon
    __dark_mode_icon: AppIcon
    __light_mode_background: str
    __dark_mode_background: str

    def __init__(self, parent: Optional["QWidget"] = None):
        super().__init__(parent)

    def keep_space_when_hiding(self) -> None:
        policy = self.sizePolicy()
        policy.setRetainSizeWhenHidden(True)
        self.setSizePolicy(policy)

    def set_light_mode_icon(self, icon: AppIcon) -> None:
        self.__light_mode_icon = icon

    def set_dark_mode_icon(self, icon: AppIcon) -> None:
        self.__dark_mode_icon = icon

    def set_light_mode_background(self, style: str) -> None:
        self.__light_mode_background = style

    def set_dark_mode_background(self, style: str) -> None:
        self.__dark_mode_background = style

    @override
    def apply_light_mode(self) -> None:
        self.__is_dark_mode = False
        self.__change_icon_based_on_state()

    @override
    def apply_dark_mode(self) -> None:
        self.__is_dark_mode = True
        self.__change_icon_based_on_state()

    def __change_icon_based_on_state(self):
        if self.__is_dark_mode:
            background: str = self.__dark_mode_background or self.__light_mode_background
            self.setStyleSheet(background)
            self.setIcon((self.__dark_mode_icon or self.__light_mode_icon))
        else:
            self.setStyleSheet(self.__light_mode_background)
            self.setIcon(self.__light_mode_icon)

    @staticmethod
    def build(
        size: QSize,
        padding: Padding,
        style: IconButtonStyle,
        parent: QObject = None,
    ) -> 'IconButton':
        button = IconButton(parent)
        button.setIcon(style.light_mode_icon)
        button.setIconSize(size - padding.get_width(size))
        button.setFixedSize(size)
        button.setCursor(Cursors.HAND)

        button.set_light_mode_icon(style.light_mode_icon)
        button.set_dark_mode_icon(style.dark_mode_icon)
        button.set_light_mode_background(
            BackgroundThemeBuilder.build(BackgroundThemeBuilder.BUTTON, size.width(), style.light_mode_background))
        button.set_dark_mode_background(
            BackgroundThemeBuilder.build(BackgroundThemeBuilder.BUTTON, size.width(), style.dark_mode_background))
        return button
