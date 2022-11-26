from abc import abstractmethod, ABC


class StylesheetElement(ABC):
    @abstractmethod
    def to_stylesheet(self, *args, **kwargs) -> str:
        pass
