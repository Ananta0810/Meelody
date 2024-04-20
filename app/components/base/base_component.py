from abc import ABCMeta, abstractmethod

from PyQt5.QtWidgets import QWidget

from app.helpers.stylesheets.translators import ClassNameTranslator


class MixinMeta(type(QWidget), ABCMeta):
    pass


class Component(metaclass=MixinMeta):

    @abstractmethod
    def _createUI(self) -> None:
        pass

    @abstractmethod
    def _connectSignalSlots(self) -> None:
        pass

    def setClassName(self, className: str) -> None:
        self.setStyleSheet(ClassNameTranslator.translate(className, self))

    @abstractmethod
    def _assignShortcuts(self) -> None:
        pass

    @abstractmethod
    def applyDarkMode(self) -> None:
        pass

    @abstractmethod
    def applyLightMode(self) -> None:
        pass
