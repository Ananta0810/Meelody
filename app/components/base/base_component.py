from msilib.schema import Component
from typing import final, Optional

from app.common.others import appCenter
from app.helpers.base import Strings
from app.helpers.base.decorators import suppressException
from app.helpers.stylesheets.translators import ClassNameTranslator


class Component:

    def __init__(self):
        self._darkModeStyle: Optional[str] = None
        self._lightModeStyle: Optional[str] = None

    def _initComponent(self, autoChangeTheme: bool = True):
        self._createUI()
        self._createThreads()
        self._connectSignalSlots()
        self._assignShortcuts()
        if autoChangeTheme:
            appCenter.themeChanged.connect(lambda light: self.applyLightMode() if light else self.applyDarkMode())

    def _createUI(self) -> None:
        pass

    def _createThreads(self) -> None:
        pass

    def _connectSignalSlots(self) -> None:
        pass

    def _assignShortcuts(self) -> None:
        pass

    @suppressException
    def setClassName(self, *classNames: str) -> None:
        light, dark = ClassNameTranslator.translate(Strings.join(" ", classNames), self)
        self._lightModeStyle = light
        self._darkModeStyle = dark

    @suppressException
    def applyLightMode(self) -> None:
        self.setStyleSheet(self._lightModeStyle)

    @suppressException
    def applyDarkMode(self) -> None:
        self.setStyleSheet(self._darkModeStyle)

    @final
    def applyTheme(self) -> None:
        if appCenter.isLightMode:
            self.applyLightMode()
        else:
            self.applyDarkMode()

    @suppressException
    def applyThemeToChildren(self) -> None:
        children = self.findChildren(Component)

        if appCenter.isLightMode:
            for component in children:
                component.applyLightMode()
        else:
            for component in children:
                component.applyDarkMode()
