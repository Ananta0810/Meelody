from abc import ABC

from .color import Color
from .stylesheet_props import StylesheetProps


class Background(StylesheetProps, ABC):

    def __init__(self, color: Color = None):
        self.color = color

    def __str__(self) -> str:
        return self.color.__str__()

    def toStylesheet(self) -> str:
        return f"background-color:{'None' if self.color is None else self.color.toStylesheet()}"

    def withOpacity(self, opacity: int) -> 'Background':
        return Background(self.color.withOpacity(opacity))
