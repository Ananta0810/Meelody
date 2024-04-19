from abc import ABCMeta, abstractmethod

from PyQt5.QtCore import QObject


class MixinMeta(type(QObject), ABCMeta):
    pass


class Component(metaclass=MixinMeta):

    @abstractmethod
    def _createUI(self) -> None:
        pass

    @abstractmethod
    def _connectSignalSlots(self) -> None:
        pass

    @abstractmethod
    def _assignShortcuts(self) -> None:
        pass

    @abstractmethod
    def applyDarkMode(self) -> None:
        pass

    @abstractmethod
    def applyLightMode(self) -> None:
        pass
