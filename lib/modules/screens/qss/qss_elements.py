from abc import ABC, abstractmethod
from sys import path

from PyQt5.QtGui import QFont

path.append("./lib")
from modules.models.color import Color


class StylesheetElement(ABC):
    @abstractmethod
    def toStylesheet(self) -> str:
        pass


class QSSColor(StylesheetElement):
    def __init__(self, normal: Color, active: Color = None):
        self.normal = normal
        self.active = active

    def toStylesheet(self, active: bool = False) -> str:
        state = self.normal
        if active and self.active is not None:
            state = self.active
        return f"{state}"


class QSSPadding:
    def __init__(self, width, height=None):
        self.width = width
        self.height = height if height is not None else width

    def getWidth(self, size: int):
        width = self.width
        if width <= 1:
            width *= size
        return width

    def getHeight(self, size: int):
        height = self.height
        if height <= 1:
            height *= size
        return height

    def toStylesheet(self, size: int = 0) -> str:
        return f"{self.getWidth(size)}px {self.getHeight(size)}px"


class QSSBorder(StylesheetElement):
    def __init__(self, size: int, style: str, color: QSSColor):
        self.size = size
        self.style = style
        self.color = color

    def toStylesheet(self, active: bool = False) -> str:
        return f"{self.size}px {self.style} {None if self.color is None else self.color.toStylesheet(active)}"


class QSSBackground:
    def __init__(
        self, border: QSSBorder = None, borderRadius=0, color: QSSColor = None
    ):
        self.border = border
        self.borderRadius = borderRadius
        self.color = color

    def colorStyleSheet(self, active: bool = False) -> str:
        if self.color is None:
            return None
        return self.color.toStylesheet(active)

    def borderStyleSheet(self, active: bool = False) -> str:
        if self.border is None:
            return None
        return self.border.toStylesheet(active)

    def borderRadiusStyleSheet(self, size: int = 0) -> str:
        radius = (
            self.borderRadius if self.borderRadius >= 1 else self.borderRadius * size
        )
        return f"{radius}px"
