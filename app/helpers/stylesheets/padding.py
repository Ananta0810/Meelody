from abc import ABC

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

    def toStylesheet(self, size: int = 0) -> str:
        return f"{self.getWidth(size)}px {self.getHeight(size)}px"
