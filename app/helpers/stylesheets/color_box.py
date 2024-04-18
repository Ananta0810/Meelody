from abc import ABC

from app.helpers import override
from app.helpers.stylesheets.color import Color
from app.helpers.stylesheets.stylesheet_props import StylesheetProps


class ColorBox(StylesheetProps, ABC):
    def __init__(self, normal: Color, active: Color = None):
        self.normal = normal
        self.active = active

    @override
    def toStylesheet(self, active: bool = False) -> str:
        status = self.active \
            if active and self.active is not None \
            else self.normal

        return f"{status.toStylesheet()}"

    def isActive(self) -> bool:
        return self.active is not None

    def __str__(self) -> str:
        return f"Color-normal: {self.normal.toStylesheet()}, Color-active: {self.active.toStylesheet() if self.isActive() else 'None'}"
