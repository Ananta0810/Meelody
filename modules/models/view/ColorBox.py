from modules.models.view.Color import Color
from modules.models.view.StylesheetElement import StylesheetElement


class ColorBox(StylesheetElement):
    def __init__(self, normal: Color, active: Color = None):
        self.normal = normal
        self.active = active

    def to_stylesheet(self, active: bool = False) -> str:
        status = self.active \
            if active and self.active is not None \
            else self.normal

        return f"{status.to_stylesheet()}"

    def is_active(self) -> bool:
        return self.active is not None

    def __str__(self) -> str:
        return f"Color-1: {self.normal.to_stylesheet()}, Color-2: {self.active.to_stylesheet() if self.is_active() else 'None'}"
