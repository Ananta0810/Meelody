from dataclasses import dataclass

from PyQt5.QtGui import QColor

from modules.helpers.types.Decorators import override
from modules.helpers.types.Numbers import Numbers
from modules.models.view.StylesheetElement import StylesheetElement


@dataclass(frozen=True)
class Color(StylesheetElement):
    red: int
    green: int
    blue: int
    alpha: int = 255

    def __str__(self) -> str:
        return self.to_stylesheet()

    @override
    def to_stylesheet(self) -> str:
        return f"rgba({self.red}, {self.green}, {self.blue}, {self.alpha / 255})"

    def with_alpha(self, alpha: int) -> 'Color':
        value: int = Numbers.clamp_int(alpha, 0, 255)
        return Color(self.red, self.green, self.blue, value)

    def with_opacity(self, opacity: int) -> 'Color':
        value: int = Numbers.clamp_int(opacity, 0, 100)
        return self.with_alpha(255 * value // 100)

    def to_QColor(self) -> QColor:
        return QColor(self.red, self.green, self.blue)
