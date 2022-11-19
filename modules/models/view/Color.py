from dataclasses import dataclass
from typing import Self

from PyQt5.QtGui import QColor

from modules.models.view.StylesheetElement import StylesheetElement


@dataclass(frozen=True)
class Color(StylesheetElement):
    red: int
    green: int
    blue: int
    alpha: float = 1.0

    def __str__(self) -> str:
        return self.to_stylesheet()

    def to_stylesheet(self) -> str:
        return f"rgba({self.red}, {self.green}, {self.blue}, {self.alpha})"

    def with_alpha(self, alpha: float) -> Self:
        return Color(self.red, self.green, self.blue, alpha)

    def with_opacity(self, alpha: int) -> Self:
        return self.with_alpha(255 * alpha)

    def to_QColor(self) -> QColor:
        return QColor(self.red, self.green, self.blue, self.alpha * 255)