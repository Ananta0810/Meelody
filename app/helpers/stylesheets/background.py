from abc import ABC

from app.helpers.base import override
from .color import Color
from .stylesheet_props import StylesheetProps


class Background(StylesheetProps, ABC):

    def __init__(self, color: Color = None):
        self.color = color

    @override
    def toStylesheet(self, activeColor: bool = False, activeBorder: bool = False,
                     borderRadiusSize: float = 0) -> str:
        return (
            f"""
            background-color:{self.__getColorStyle()}; 
            """
        )

    def __getColorStyle(self) -> str:
        if self.color is None:
            return 'None'
        return self.color.toStylesheet()

    def __str__(self) -> str:
        return self.color.__str__()
