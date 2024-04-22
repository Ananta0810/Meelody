from abc import ABCMeta

from PyQt5.QtWidgets import QWidget

from app.helpers.base import Strings
from app.helpers.stylesheets.translators import ClassNameTranslator


class MixinMeta(type(QWidget), ABCMeta):
    pass


class Component(metaclass=MixinMeta):
    _lightModeStyle: str = None
    _darkModeStyle: str = None

    def _createUI(self) -> None:
        pass

    def _createThreads(self) -> None:
        pass

    def _connectSignalSlots(self) -> None:
        pass

    def _assignShortcuts(self) -> None:
        pass

    def setClassName(self, *classNames: str) -> None:
        light, dark = ClassNameTranslator.translate(Strings.join(" ", classNames), self)
        self._lightModeStyle = light
        self._darkModeStyle = dark

    def applyLightMode(self) -> None:
        self.setStyleSheet(self._lightModeStyle)

    def applyDarkMode(self) -> None:
        self.setStyleSheet(self._darkModeStyle)
