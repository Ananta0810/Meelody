from modules.helpers.types.Decorators import override
from modules.models.view.Border import Border
from modules.models.view.ColorBox import ColorBox
from modules.models.view.StylesheetElement import StylesheetElement


class Background(StylesheetElement):

    def __init__(self, border: Border = None, border_radius: float = 0, color: ColorBox = None):
        self.border = border
        self.border_radius = border_radius
        self.color = color

    def with_border(self, border: Border) -> 'Background':
        return Background(border, self.border_radius, self.color)

    def with_border_radius(self, border_radius: float) -> 'Background':
        return Background(self.border, border_radius, self.color)

    def with_color(self, color: ColorBox) -> 'Background':
        return Background(self.border, self.border_radius, color)

    def and_border(self, border: Border) -> 'Background':
        self.border = border
        return self

    def and_border_radius(self, border_radius: float) -> 'Background':
        self.border_radius = border_radius
        return self

    def and_color(self, color: ColorBox) -> 'Background':
        self.color = color
        return self

    def get_color_style(self, active: bool = False) -> str:
        if self.color is None:
            return 'None'
        return self.color.to_stylesheet(active)

    def get_border_style(self, active: bool = False) -> str:
        if self.border is None:
            return 'None'
        return self.border.to_stylesheet(active)

    def get_border_darius_style(self, size: float = 0) -> float:
        return self.border_radius \
            if self.border_radius > 1 \
            else self.border_radius * (size or 0)

    @override
    def to_stylesheet(self, active_color: bool = False, active_border: bool = False, border_radius_size: float = 0) -> str:
        return (
            f"""
            border:{self.get_border_style(active_border)};
            border-radius:{self.get_border_darius_style(border_radius_size)};
            background-color:{self.get_color_style(active_color)}; 
            """
        )
