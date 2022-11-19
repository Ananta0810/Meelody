from modules.models.view.Border import Border
from modules.models.view.ColorBox import ColorBox
from modules.models.view.StylesheetElement import StylesheetElement


class Background(StylesheetElement):

    def __init__(self, border: Border = None, border_radius: float = 0, color: ColorBox = None):
        self.border = border
        self.borderRadius = border_radius
        self.color = color

    def colorStyleSheet(self, active: bool = False) -> str:
        if self.color is None:
            return 'None'
        return self.color.to_stylesheet(active)

    def borderStyleSheet(self, active: bool = False) -> str:
        if self.border is None:
            return 'None'
        return self.border.to_stylesheet(active)

    def calculate_radius(self, size: int = 0) -> float:
        return self.borderRadius \
            if self.borderRadius >= 1 \
            else self.borderRadius * size

    def to_stylesheet(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"border:{self.border};border-radius:{self.borderRadius};color:{self.color}"
