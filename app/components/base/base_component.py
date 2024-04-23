from app.common.others import signalBus
from app.helpers.base import Strings
from app.helpers.stylesheets.translators import ClassNameTranslator


class Component:
    _lightModeStyle: str = None
    _darkModeStyle: str = None

    def _initComponent(self):
        self._createUI()
        self._createThreads()
        self._connectSignalSlots()
        self._assignShortcuts()
        signalBus.themeChanged.connect(lambda light: self.applyLightMode() if light else self.applyDarkMode())

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
