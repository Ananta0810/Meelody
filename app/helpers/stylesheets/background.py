from abc import ABC
from typing import final

from .color import Color, Colors
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


@final
class Backgrounds:
    none = Background(color=Colors.none)
    primary = Background(color=Colors.primary)
    success = Background(color=Colors.success)
    danger = Background(color=Colors.danger)
    warning = Background(color=Colors.warning)
    white = Background(color=Colors.white)
    black = Background(color=Colors.black)
    gray = Background(color=Colors.gray)
