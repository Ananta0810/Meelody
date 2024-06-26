from typing import Optional

from PyQt5.QtWidgets import QWidget, QPushButton

from app.common.others import appCenter
from app.common.statics.styles import Colors
from app.components.base.app_icon import AppIcon
from app.components.base.base_component import Component
from app.helpers.stylesheets import ClassNameTheme
from app.helpers.stylesheets import ClassNameTranslator
from app.utils.base import Strings
from app.utils.reflections import suppressException


class StateIcon:
    lightModeIcon: AppIcon
    darkModeIcon: AppIcon
    toolTip: str

    def __init__(self, lightModeIcon: AppIcon, darkModeIcon: AppIcon = None, toolTip: str = None) -> None:
        self.lightModeIcon = lightModeIcon
        self.darkModeIcon = darkModeIcon or lightModeIcon
        self.toolTip = toolTip


class MultiStatesIconButton(QPushButton, Component):

    def __init__(self, parent: Optional[QWidget] = None):
        self._icons: list[StateIcon] = []
        self._currentIndex: int = 0
        self._changeStateOnPressed: bool = True
        self._currentClassName = ""
        super().__init__(parent)
        super()._initComponent()

    def keepSpaceWhenHiding(self) -> None:
        policy = self.sizePolicy()
        policy.setRetainSizeWhenHidden(True)
        self.setSizePolicy(policy)

    def setIcons(self, icons: list[StateIcon]) -> None:
        self._icons = icons

    def setToolTips(self, toolTips: list[str]) -> None:
        for index, icon in enumerate(self._icons):
            self._icons[index].toolTip = toolTips[index]
        self._changeButtonBasedOnState()

    def addChild(self, child: StateIcon) -> None:
        self._icons.append(child)

    def setChangeStateOnPressed(self, a0: bool) -> None:
        self._changeStateOnPressed = a0

    def setActiveState(self, index: int) -> None:
        if index >= len(self._icons):
            return
        self._currentIndex = index
        self._changeButtonBasedOnState()

    def toNextState(self) -> None:
        self.setActiveState((self._currentIndex + 1) % len(self._icons))

    def _changeButtonBasedOnState(self) -> None:
        button = self._icons[self._currentIndex]
        self.setClassName(self._currentClassName)

        self.setToolTip(button.toolTip)
        if appCenter.isLightMode:
            self.setIcon(button.lightModeIcon)
            super().applyLightMode()
        else:
            self.setIcon(button.darkModeIcon or button.lightModeIcon)
            super().applyDarkMode()

    @suppressException
    def setClassName(self, *classNames: str) -> None:
        self._currentClassName = Strings.join(" ", classNames)
        super().setClassName(self._currentClassName)

    def mousePressEvent(self, event) -> None:
        super().mousePressEvent(event)
        if self._changeStateOnPressed:
            self.toNextState()

    def applyLightMode(self) -> None:
        super().applyLightMode()
        self._changeButtonBasedOnState()

    def applyDarkMode(self) -> None:
        super().applyDarkMode()
        self._changeButtonBasedOnState()


class ToggleIconButton(MultiStatesIconButton):
    __isActive: bool = True

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setCheckable(True)

    def keepSpaceWhenHiding(self) -> None:
        policy = self.sizePolicy()
        policy.setRetainSizeWhenHidden(True)
        self.setSizePolicy(policy)

    def setActive(self, active: bool) -> None:
        if active != self.isActive():
            self.__isActive = active
            self.setActiveState(0 if active else 1)
            super()._changeButtonBasedOnState()

    def setActiveIcon(self, lightModeIcon: AppIcon, darkModeIcon: AppIcon = None) -> None:
        icon = StateIcon(lightModeIcon, darkModeIcon)
        if len(self._icons) > 0:
            self._icons[0] = icon
            return
        self._icons.append(icon)

    def setInactiveIcon(self, lightModeIcon: AppIcon, darkModeIcon: AppIcon = None) -> None:
        icon = StateIcon(lightModeIcon, darkModeIcon)
        if len(self._icons) > 1:
            self._icons[1] = icon
            return
        self._icons.append(icon)

    def isActive(self) -> bool:
        return self._currentIndex == 0

    def isInactive(self) -> bool:
        return self._currentIndex == 1

    @suppressException
    def setClassName(self, *classNames: str) -> None:
        self._currentClassName = Strings.join(" ", classNames)

        light, dark = ClassNameTranslator.translateElements(self._currentClassName, self)
        self._lightModeStyle = self.__buildStyle(light)
        self._darkModeStyle = self.__buildStyle(dark)

    def __buildStyle(self, theme: ClassNameTheme) -> str:
        normal = theme.getElement("none")
        active = theme.getElement("active" if self.isActive() else "inactive")

        style = f"""
             QPushButton {{{Strings.joinStyles([normal.state("none").toProps(), active.state("none").toProps()])}}}
             QPushButton::hover {{{Strings.joinStyles([normal.state("hover").toProps(), active.state("hover").toProps()])}}}
             """
        return style


class IconButton(QPushButton, Component):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        super()._initComponent()
        self.__lightModeIcon: Optional[AppIcon] = None
        self.__darkModeIcon: Optional[AppIcon] = None

    def keepSpaceWhenHiding(self) -> None:
        policy = self.sizePolicy()
        policy.setRetainSizeWhenHidden(True)
        self.setSizePolicy(policy)

    def setLightModeIcon(self, icon: AppIcon) -> None:
        self.__lightModeIcon = icon
        if self.icon() is None:
            self.setIcon(icon)

    def setDarkModeIcon(self, icon: AppIcon) -> None:
        self.__darkModeIcon = icon
        if self.icon() is None:
            self.setIcon(icon)

    @suppressException
    def applyLightMode(self) -> None:
        super().applyLightMode()
        self.setIcon(self.__lightModeIcon)

    @suppressException
    def applyDarkMode(self) -> None:
        super().applyDarkMode()
        self.setIcon(self.__darkModeIcon or self.__lightModeIcon)

    @suppressException
    def setDisabled(self, disabled: bool) -> None:
        super().setDisabled(disabled)
        if not isinstance(self.icon(), AppIcon):
            return

        icon = self.__lightModeIcon if appCenter.isLightMode else self.__darkModeIcon or self.__lightModeIcon
        if disabled:
            self.setIcon(icon.withColor(Colors.gray))
        else:
            self.setIcon(icon)
