from abc import abstractmethod, ABC


class StylesheetProps(ABC):
    @abstractmethod
    def to_stylesheet(self, *args, **kwargs) -> str:
        pass
