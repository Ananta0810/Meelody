from app.helpers.base import override
from .color_box import ColorBox
from .stylesheet_props import StylesheetProps


class Border(StylesheetProps):
    def __init__(self, size: int, color: ColorBox, style: str = "solid"):
        self.size = size
        self.style = style
        self.color = color

    def withSize(self, size: int) -> 'Border':
        return Border(size, self.color, self.style)

    def withStyle(self, style: str) -> 'Border':
        return Border(self.size, self.color, style)

    def withColor(self, color: ColorBox) -> 'Border':
        return Border(self.size, color, self.style)

    def andSize(self, size: int) -> 'Border':
        self.size = size
        return self

    def andStyle(self, style: str) -> 'Border':
        self.style = style
        return self

    def andColor(self, color: ColorBox) -> 'Border':
        self.color = color
        return self

    @override
    def toStylesheet(self, active: bool = False) -> str:
        return f"{self.size}px {self.style} {self.color.toStylesheet(active)}"

    def __str__(self) -> str:
        return f"(size: {self.size}, style: {self.style}, color: {self.color})"
