from abc import ABC
from dataclasses import dataclass
from typing import final

from PyQt5.QtGui import QColor

from app.helpers.base import Numbers
from app.helpers.stylesheets.stylesheet_props import StylesheetProps

_LUMINANCE_RED = 0.2126
_LUMINANCE_GREEN = 0.7152
_LUMINANCE_BLUE = 0.0722


@dataclass(frozen=True)
class Color(StylesheetProps, ABC):
    red: int
    green: int
    blue: int
    alpha: int = 255

    def __str__(self) -> str:
        return self.toStylesheet()

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

    def isDarkColor(self) -> bool:
        return self.__luminance() < 140

    def __luminance(self) -> float:
        return self.red * _LUMINANCE_RED + self.green * _LUMINANCE_GREEN + self.blue * _LUMINANCE_BLUE


@final
class Colors:
    PRIMARY = Color(100, 32, 255)
    SUCCESS = Color(50, 216, 100)
    DANGER = Color(255, 80, 80)
    WARNING = Color(255, 170, 28)
    WHITE = Color(255, 255, 255)
    DARK = Color(32, 32, 32)
    BLACK = Color(0, 0, 0)
    GRAY = Color(128, 128, 128)
    NONE = Color(255, 255, 255, 0)
