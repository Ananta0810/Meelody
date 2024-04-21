from abc import ABC
from typing import final

from app.helpers.base import override
from .color import Color, Colors
from .stylesheet_props import StylesheetProps


class Background(StylesheetProps, ABC):

    def __init__(self, color: Color = None):
        self.color = color

    def __str__(self) -> str:
        return self.color.__str__()

    @override
    def toStylesheet(self) -> str:
        return f"background-color:{'None' if self.color is None else self.color.toStylesheet()}"

    def withOpacity(self, opacity: int) -> 'Background':
        return Background(self.color.withOpacity(opacity))


@final
class Backgrounds:
    NONE = Background(color=Colors.NONE)
    PRIMARY = Background(color=Colors.PRIMARY)
    SUCCESS = Background(color=Colors.SUCCESS)
    DANGER = Background(color=Colors.DANGER)
    WARNING = Background(color=Colors.WARNING)
    WHITE = Background(color=Colors.WHITE)
    BLACK = Background(color=Colors.BLACK)
    GRAY = Background(color=Colors.GRAY)
