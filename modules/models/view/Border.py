from modules.helpers.types.Decorators import override
from modules.models.view.ColorBox import ColorBox
from modules.models.view.StylesheetElement import StylesheetElement


class Border(StylesheetElement):
    def __init__(self, size: int, color: ColorBox, style: str = "solid"):
        self.size = size
        self.style = style
        self.color = color

    def with_size(self, size: int) -> 'Border':
        return Border(size, self.color, self.style)

    def with_style(self, style: str) -> 'Border':
        return Border(self.size, self.color, style)

    def with_color(self, color: ColorBox) -> 'Border':
        return Border(self.size, color, self.style)

    def and_size(self, size: int) -> 'Border':
        self.size = size
        return self

    def and_style(self, style: str) -> 'Border':
        self.style = style
        return self

    def and_color(self, color: ColorBox) -> 'Border':
        self.color = color
        return self

    @override
    def to_stylesheet(self, active: bool = False) -> str:
        return f"{self.size}px {self.style} {self.color or self.color.to_stylesheet(active)}"
