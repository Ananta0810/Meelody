from abc import ABC
from typing import Optional

from PyQt5.QtWidgets import QWidget, QPushButton

from modules.helpers.types.Decorators import override
from modules.models.view.Padding import Padding
from modules.screens.AbstractScreen import BaseView
from modules.statics.view.Material import Paddings
from modules.widgets.Icons import AppIcon


class ActionButton(QPushButton, BaseView, ABC):
    padding: Padding = Paddings.DEFAULT

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

    def setPadding(self, padding: Padding) -> None:
        self.padding = padding

    @override
    def setText(self, text: str) -> None:
        super().setText(text)
        self.__paddingText()

    def __paddingText(self) -> None:
        if self.padding is Paddings.DEFAULT:
            return
        textSize = self.sizeHint()
        self.setFixedSize(
            textSize.width() + self.padding.get_width(textSize.width()),
            textSize.height() + self.padding.get_height(textSize.height()),
        )

    def __setLightModeBackground(self, style: str) -> None:
        self.__lightModeBackground = style

    def __setDarkModeBackground(self, style: str) -> None:
        self.__darkModeBackground = style


class StatelessIconButtonThemeData:
    lightModeIcon: AppIcon
    lightModeBackground: str
    darkModeIcon: AppIcon
    darkModeBackground: str

    def __init__(
        self,
        lightModeIcon: AppIcon,
        lightModeBackground: str,
        darkModeIcon: AppIcon = None,
        darkModeBackground: str = None
    ):
        self.lightModeIcon = lightModeIcon
        self.lightModeBackground = lightModeBackground

        self.darkModeIcon = darkModeIcon or lightModeIcon
        self.darkModeBackground = darkModeBackground or lightModeBackground


class StatelessIconButton(QPushButton, BaseView, ABC):
    _children: list[StatelessIconButtonThemeData] = []
    _currentIndex: int = 0
    __changeStateOnPressed: bool = True
    __isDarkMode: bool = False

    def __init__(self, parent: Optional["QWidget"] = None):
        super().__init__(parent)

    def keepSpaceWhenHiding(self) -> None:
        policy = self.sizePolicy()
        policy.setRetainSizeWhenHidden(True)
        self.setSizePolicy(policy)

    def setChildren(self, children: list[StatelessIconButtonThemeData]) -> None:
        self._children = children

    def addChild(self, child: StatelessIconButtonThemeData) -> None:
        self._children.append(child)

    def setChangeStateOnPressed(self, a0: bool) -> None:
        self.__changeStateOnPressed = a0

    def setStateIndex(self, index: int) -> None:
        if index >= len(self._children):
            return
        self._currentIndex = index
        self._changeButtonBasedOnState()

    def toNextState(self) -> None:
        self.setStateIndex((self._currentIndex + 1) % len(self._children))

    def _changeButtonBasedOnState(self) -> None:
        button = self._children[self._currentIndex]

        if self.__isDarkMode:
            self.setIcon(button.darkModeIcon)
            self.setStyleSheet(button.darkModeBackground)
            return

        self.setIcon(button.lightModeIcon)
        self.setStyleSheet(button.lightModeBackground)

    @override
    def mousePressEvent(self, event) -> None:
        super().mousePressEvent(event)
        if self.__changeStateOnPressed:
            self.toNextState()


class ToggleIconButton(StatelessIconButton, ABC):
    __isActive: bool = True

    def __init__(self, parent: Optional["QWidget"] = None):
        super().__init__(parent)

    def keepSpaceWhenHiding(self) -> None:
        policy = self.sizePolicy()
        policy.setRetainSizeWhenHidden(True)
        self.setSizePolicy(policy)

    def setActive(self, active: bool) -> None:
        self.__isActive = active
        self.setStateIndex(0 if active else 1)
        super()._changeButtonBasedOnState()

    def setActiveBtn(self, button: StatelessIconButtonThemeData) -> None:
        if len(self._children) > 0:
            self._children[0] = button
            return
        self._children.append(button)

    def setInactiveBtn(self, button: StatelessIconButtonThemeData) -> None:
        if len(self._children) > 1:
            self._children[1] = button
            return
        self._children.append(button)

    def setButtons(self, activeButton: StatelessIconButtonThemeData,
                   inactiveButton: StatelessIconButtonThemeData) -> None:
        self.setActive_btn(activeButton)
        self.setInactiveBtn(inactiveButton)

    def isActive(self) -> bool:
        return self._currentIndex == 0

    def isInactive(self) -> bool:
        return self._currentIndex == 1


class IconButton(QPushButton, BaseView, ABC):
    __isDarkMode: bool = False
    __lightModeIcon: AppIcon
    __darkModeIcon: AppIcon
    __lightModeBackground: str
    __darkModeBackground: str

    def __init__(self, parent: Optional["QWidget"] = None):
        super().__init__(parent)

    def keepSpaceWhenHiding(self) -> None:
        policy = self.sizePolicy()
        policy.setRetainSizeWhenHidden(True)
        self.setSizePolicy(policy)

    def setLightModeIcon(self, icon: AppIcon) -> None:
        self.__lightModeIcon = icon

    def setDarkModeIcon(self, icon: AppIcon) -> None:
        self.__darkModeIcon = icon

    def setLightModeBackground(self, style: str) -> None:
        self.__lightModeBackground = style

    def setDarkModeBackground(self, style: str) -> None:
        self.__darkModeBackground = style
