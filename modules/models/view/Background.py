from typing import Self

from modules.models.view.Border import Border
from modules.models.view.ColorBox import ColorBox
from modules.models.view.StylesheetElement import StylesheetElement


class Background(StylesheetElement):

    def __init__(self, border: Border = None, border_radius: float = 0, color: ColorBox = None):
        self.border = border
        self.border_radius = border_radius
        self.color = color

    def with_border(self, border: Border) -> Self:
        return Background(border, self.border_radius, self.color)

    def with_border_radius(self, border_radius: float) -> Self:
        return Background(self.border, border_radius, self.color)

    def with_color(self, color: ColorBox) -> Self:
        return Background(self.border, self.border_radius, color)

    def and_border(self, border: Border) -> Self:
        self.border = border
        return self

    def and_border_radius(self, border_radius: float) -> Self:
        self.border_radius = border_radius
        return self

    def and_color(self, color: ColorBox) -> Self:
        self.color = color
        return self

    def __get_color(self, active: bool = False) -> str:
        if self.color is None:
            return 'None'
        return self.color.to_stylesheet(active)

    def __get_border(self, active: bool = False) -> str:
        if self.border is None:
            return 'None'
        return self.border.to_stylesheet(active)

    def __get_darius(self, size: int = 0) -> float:
        return self.border_radius \
            if self.border_radius >= 1 \
            else self.border_radius * size

    def to_stylesheet(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"border:{self.__get_border()};border-radius:{self.__get_darius()};background-color:{self.__get_color()}"
