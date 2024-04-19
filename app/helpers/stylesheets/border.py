from app.helpers.base import override
from .color import Color
from .stylesheet_props import StylesheetProps


class Border(StylesheetProps):
    def __init__(self, size: int, color: Color, style: str = "solid"):
        self.size = size
        self.style = style
        self.color = color

    def withSize(self, size: int) -> 'Border':
        return Border(size, self.color, self.style)

    def withStyle(self, style: str) -> 'Border':
        return Border(self.size, self.color, style)

    def withColor(self, color: Color) -> 'Border':
        return Border(self.size, color, self.style)

    @override
    def toStylesheet(self) -> str:
        return f"{self.size}px {self.style} {self.color.toStylesheet()}"

    def __str__(self) -> str:
        return f"(size: {self.size}, style: {self.style}, color: {self.color})"
