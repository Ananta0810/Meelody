from abc import ABC, abstractmethod


class ViewComponent(ABC):

    @abstractmethod
    def apply_dark_mode(self) -> None:
        pass

    @abstractmethod
    def apply_light_mode(self) -> None:
        pass

    @abstractmethod
    def connect_signal(self) -> None:
        pass

    @abstractmethod
    def translate(self) -> None:
        pass