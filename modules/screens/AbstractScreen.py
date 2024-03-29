from abc import ABCMeta, abstractmethod

from PyQt5.QtCore import QObject


class MixinMeta(type(QObject), ABCMeta):
    pass


class BaseView(metaclass=MixinMeta):

    @abstractmethod
    def apply_dark_mode(self) -> None:
        pass

    @abstractmethod
    def apply_light_mode(self) -> None:
        pass

    def assign_shortcuts(self) -> None:
        pass


class BaseControl:

    @abstractmethod
    def connect_signals(self) -> None:
        pass
