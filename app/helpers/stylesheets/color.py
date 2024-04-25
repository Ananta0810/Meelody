from abc import ABC
from dataclasses import dataclass
from typing import final

from PyQt5.QtGui import QColor

from app.helpers.base import override, Numbers
from app.helpers.stylesheets.stylesheet_props import StylesheetProps


@dataclass(frozen=True)
class Color(StylesheetProps, ABC):
    red: int
    green: int
    blue: int
    alpha: int = 255

    def __str__(self) -> str:
        return self.toStylesheet()

    @override
    def toStylesheet(self) -> str:
        return f"rgba({self.red}, {self.green}, {self.blue}, {self.alpha / 255})"

    def withAlpha(self, alpha: int) -> 'Color':
        value: int = Numbers.clamp(alpha, 0, 255)
        return Color(self.red, self.green, self.blue, value)

    def withOpacity(self, opacity: int) -> 'Color':
        value: int = Numbers.clamp(opacity, 0, 100)
        return self.withAlpha(255 * value // 100)

    def toQColor(self) -> QColor:
        return QColor(self.red, self.green, self.blue, int(self.alpha))


@final
class Colors:
    PRIMARY = Color(100, 32, 255)
    SUCCESS = Color(50, 216, 100)
    DANGER = Color(255, 80, 80)
    WARNING = Color(255, 170, 28)
    WHITE = Color(255, 255, 255)
    BLACK = Color(0, 0, 0)
    GRAY = Color(128, 128, 128)
    NONE = Color(255, 255, 255, 0)
