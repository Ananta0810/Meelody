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
        luminance = self.__luminance()
        return luminance < 0.5

    def __luminance(self) -> float:
        """
            View https://stackoverflow.com/a/9733420 for more information
        """
        return (
            self._luminanceOfHeight(self.red) * _LUMINANCE_RED +
            self._luminanceOfHeight(self.green) * _LUMINANCE_GREEN +
            self._luminanceOfHeight(self.blue) * _LUMINANCE_BLUE
        )

    @staticmethod
    def _luminanceOfHeight(color_part: int) -> float:
        v = color_part / 255
        return (
            v / 12.92 if v <= 0.03928
            else pow((v + 0.055) / 1.055, 2.4)
        )


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
