from abc import ABC

from app.helpers.base import override
from .border import Border
from .color_box import ColorBox
from .stylesheet_props import StylesheetProps


class Background(StylesheetProps, ABC):

    def __init__(self, border: Border = None, borderRadius: float = 0, color: ColorBox = None):
        self.border = border
        self.borderRadius = borderRadius
        self.color = color

    def withBorder(self, border: Border) -> 'Background':
        return Background(border, self.borderRadius, self.color)

    def withBorderRadius(self, borderRadius: float) -> 'Background':
        return Background(self.border, borderRadius, self.color)

    def withColor(self, color: ColorBox) -> 'Background':
        return Background(self.border, self.borderRadius, color)

    def andBorder(self, border: Border) -> 'Background':
        self.border = border
        return self

    def andBorderRadius(self, borderRadius: float) -> 'Background':
        self.borderRadius = borderRadius
        return self

    def andColor(self, color: ColorBox) -> 'Background':
        self.color = color
        return self

    def getColorStyle(self, active: bool = False) -> str:
        if self.color is None:
            return 'None'
        return self.color.toStylesheet(active)

    def getBorderStyle(self, active: bool = False) -> str:
        if self.border is None:
            return 'None'
        return self.border.toStylesheet(active)

    def getBorderDariusStyle(self, size: float = 0) -> float:
        return self.borderRadius \
            if self.borderRadius > 1 \
            else self.borderRadius * (size or 0)

    @override
    def toStylesheet(self, activeColor: bool = False, activeBorder: bool = False,
                     borderRadiusSize: float = 0) -> str:
        return (
            f"""
            border:{self.getBorderStyle(activeBorder)};
            border-radius:{self.getBorderDariusStyle(borderRadiusSize)};
            background-color:{self.getColorStyle(activeColor)}; 
            """
        )
