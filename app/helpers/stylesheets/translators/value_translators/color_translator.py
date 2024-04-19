from typing import List

from app.helpers.base import override
from app.helpers.stylesheets import Color
from app.helpers.stylesheets.translators.value_translators.value_translator import ValueTranslator

variants: dict[str, Color] = {
    "primary": Color(128, 64, 255),

    "success": Color(50, 216, 100),
    "danger": Color(255, 80, 80),
    "warning": Color(255, 170, 28),

    "white": Color(255, 255, 255),
    "black": Color(0, 0, 0),
    "gray": Color(128, 128, 128),
    "none": Color(255, 255, 255, 0),
}


class ColorTranslator(ValueTranslator[Color]):

    @override
    def translate(self, classNames: List[str]) -> Color:
        colorsFound = [self.transform(cn) for cn in classNames if self.isValid(cn)]
        return colorsFound[0]

    def isValid(self, cn: str) -> bool:
        parts = cn.split("-")
        length = len(parts)
        if length <= 2:
            return parts[0] in variants
        return False

    def transform(self, cn: str) -> Color:
        parts = cn.split("-")
        color_variant = parts[0]
        color = variants[color_variant]
        try:
            return color.withOpacity(int(parts[-1]))
        except ValueError:
            return color
