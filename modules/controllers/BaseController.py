from abc import abstractmethod


class BaseController:

    @abstractmethod
    def connect_to_view(self) -> None:
        pass
