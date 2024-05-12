from abc import ABC
from colorsys import rgb_to_hls, hls_to_rgb
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

    def toSolidColor(self, backgroundColor: 'Color') -> 'Color':
        alpha = self.alpha / 255
        oneminusalpha = 1 - alpha

        red = (self.red * alpha) + (oneminusalpha * backgroundColor.red)
        green = (self.green * alpha) + (oneminusalpha * backgroundColor.green)
        blue = (self.blue * alpha) + (oneminusalpha * backgroundColor.blue)

        return Color(int(red), int(green), int(blue))

    def toQColor(self) -> QColor:
        return QColor(self.red, self.green, self.blue, int(self.alpha))

    def isDarkColor(self) -> bool:
        return self.__luminance() < 140

    def __luminance(self) -> float:
        return self.red * _LUMINANCE_RED + self.green * _LUMINANCE_GREEN + self.blue * _LUMINANCE_BLUE

    def darken(self, by: float) -> 'Color':
        factor = 1 / by
        h, l, s = rgb_to_hls(self.red / 255.0, self.green / 255.0, self.blue / 255.0)
        l = max(min(l * factor, 1.0), 0.0)
        r, g, b = hls_to_rgb(h, l, s)
        color = Color(red=int(r * 255), green=int(g * 255), blue=int(b * 255))
        return color


@final
class Colors:
    primary = Color(100, 32, 255)
    success = Color(50, 216, 100)
    danger = Color(255, 80, 80)
    warning = Color(255, 170, 28)
    white = Color(255, 255, 255)
    dark = Color(32, 32, 32)
    black = Color(0, 0, 0)
    gray = Color(128, 128, 128)
    none = Color(255, 255, 255, 0)
