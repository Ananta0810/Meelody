from abc import ABCMeta, abstractmethod, ABC

from PyQt5.QtCore import QObject


class MixinMeta(type(QObject), ABCMeta):
    pass


class ViewComponent(metaclass=MixinMeta):

    @abstractmethod
    def apply_dark_mode(self) -> None:
        pass

    @abstractmethod
    def apply_light_mode(self) -> None:
        pass
