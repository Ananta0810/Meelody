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

    def __str__(self):
        return self.toStylesheet()

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

    def __str__(self):
        return f"Color-1: {self.normal.toStylesheet()}, Color-2: {self.active.toStylesheet() if self.active is not None else 'None'}"


class Padding:
    def __init__(self, width, height=None, relativeOnly: bool = False):
        self.width = width
        self.height = width if height is None else height
        self.relativeOnly = relativeOnly

    def getWidth(self, size: int = 0) -> float:
        width = self.width
        if self.relativeOnly:
            return width * size
        if width <= 1:
            return width * size
        return width

    def getHeight(self, size: int = 0) -> float:
        height = self.height
        if self.relativeOnly:
            return height * size
        if height <= 1:
            return height * size
        return height

    def toStylesheet(self, size: int = 0) -> str:
        return f"{self.getWidth(size)}px {self.getHeight(size)}px"

    def toStylesheetWithRatio(self, size: int = 0, ratio: float = 1.0) -> str:
        return f"{self.getWidth(size) * ratio}px {self.getHeight(size) * ratio}px"


class Border(StylesheetElement):
    def __init__(self, size: int, style: str, color: ColorBox):
        self.size = size
        self.style = style
        self.color = color

    def toStylesheet(self, active: bool = False) -> str:
        return f"{self.size}px {self.style} {None if self.color is None else self.color.toStylesheet(active)}"


class Background:
    def __init__(self, border: Border = None, borderRadius: float = 0, color: ColorBox = None):
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

    def borderRadiusStyleSheet(self, size: int = 0) -> int:
        radius = self.borderRadius if self.borderRadius >= 1 else self.borderRadius * size
        return radius

    def __str__(self):
        return f"border:{self.border};border-radius:{self.borderRadius};color:{self.color}"
