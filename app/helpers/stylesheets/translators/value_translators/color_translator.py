from typing import List

from app.helpers.base import override
from app.helpers.stylesheets import Color, Colors
from app.helpers.stylesheets.translators.value_translators.value_translator import ValueTranslator

variants: dict[str, Color] = {
    "primary": Colors.PRIMARY,

    "success": Colors.SUCCESS,
    "danger": Colors.DANGER,
    "warning": Colors.WARNING,

    "dark": Colors.DARK,
    "white": Colors.WHITE,
    "black": Colors.BLACK,
    "gray": Colors.GRAY,
    "none": Colors.NONE,
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
