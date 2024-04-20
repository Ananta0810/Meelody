from abc import ABC
from typing import final

from app.helpers.base import override
from app.helpers.stylesheets.stylesheet_props import StylesheetProps


class Padding(StylesheetProps, ABC):
    def __init__(self, width: float, height: float = None, isRelative: bool = False):
        self.width = width
        self.height = width if height is None else height
        self.isRelative = isRelative

    def getWidth(self, size: int = 0) -> float:
        if self.isRelative:
            return self.width * size
        if self.width <= 1:
            return self.width * size
        return self.width

    def getHeight(self, size: int = 0) -> float:
        if self.isRelative:
            return self.height * size
        if self.height <= 1:
            return self.height * size
        return self.height

    @override
    def toStylesheet(self, size: int = 0) -> str:
        return f"{self.getWidth(size)}px {self.getHeight(size)}px"


@final
class Paddings:
    DEFAULT = Padding(0.00)
    RELATIVE_25 = Padding(0.25)
    RELATIVE_33 = Padding(0.33)
    RELATIVE_50 = Padding(0.5)
    RELATIVE_67 = Padding(0.67)
    RELATIVE_75 = Padding(0.75)
    RELATIVE_100 = Padding(1.00)

    ABSOLUTE_SMALL = Padding(4)
    ABSOLUTE_MEDIUM = Padding(12)

    LABEL_SMALL = Padding(1.25, 0.625, isRelative=True)
    LABEL_MEDIUM = Padding(1.25, 0.625, isRelative=True)
    LABEL_LARGE = Padding(1.5, 1, isRelative=True)
