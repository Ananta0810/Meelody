from modules.helpers.types.Decorators import override
from modules.models.view.ColorBox import ColorBox
from modules.models.view.StylesheetElement import StylesheetElement


class Border(StylesheetElement):
    def __init__(self, size: int, style: str, color: ColorBox):
        self.size = size
        self.style = style
        self.color = color

    def with_size(self, size: int) -> 'Border':
        return Border(size, self.style, self.color)

    def with_style(self, style: str) -> 'Border':
        return Border(self.size, style, self.color)

    def with_color(self, color: ColorBox) -> 'Border':
        return Border(self.size, self.style, color)

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
