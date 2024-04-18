from abc import abstractmethod, ABC


class StylesheetProps(ABC):
    @abstractmethod
    def toStylesheet(self, *args, **kwargs) -> str:
        pass
