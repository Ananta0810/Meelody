from modules.models.view.ColorBox import ColorBox
from modules.models.view.StylesheetElement import StylesheetElement


class Border(StylesheetElement):
    def __init__(self, size: int, style: str, color: ColorBox):
        self.size = size
        self.style = style
        self.color = color

    def to_stylesheet(self, active: bool = False) -> str:
        return f"{self.size}px {self.style} {self.color or self.color.to_stylesheet(active)}"
