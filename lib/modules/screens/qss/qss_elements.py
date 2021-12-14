from abc import ABC, abstractmethod
from dataclasses import dataclass


class StylesheetElement(ABC):
    @abstractmethod
    def toStylesheet(self) -> str:
        pass


@dataclass(frozen=True)
class Color(StylesheetElement):
    red: int
    green: int
    blue: int
    alpha: float = 1.0

    def toStylesheet(self) -> str:
        return f"rgba({self.red}, {self.green}, {self.blue}, {self.alpha})"

    def withAlpha(self, alpha: float):
        return Color(self.red, self.green, self.blue, alpha)


class ColorBox(StylesheetElement):
    def __init__(self, normal: Color, active: Color = None):
        self.normal = normal
        self.active = active

    def toStylesheet(self, active: bool = False) -> str:
        state = self.normal
        if active and self.active is not None:
            state = self.active
        return f"{state.toStylesheet()}"


class Padding:
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


class Border(StylesheetElement):
    def __init__(self, size: int, style: str, color: ColorBox):
        self.size = size
        self.style = style
        self.color = color

    def toStylesheet(self, active: bool = False) -> str:
        return f"{self.size}px {self.style} {None if self.color is None else self.color.toStylesheet(active)}"


class Background:
    def __init__(
        self, border: Border = None, borderRadius=0, color: ColorBox = None
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
            self.borderRadius
            if self.borderRadius >= 1
            else self.borderRadius * size
        )
        return f"{radius}px"
