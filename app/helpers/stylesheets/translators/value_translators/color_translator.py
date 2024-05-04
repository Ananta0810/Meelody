from typing import List, Optional

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


class ColorTranslator(ValueTranslator[str]):

    def translate(self, classNames: List[str]) -> str:
        colorsFound = [self.transform(cn) for cn in classNames]
        return colorsFound[0]

    @staticmethod
    def transform(cn: str) -> Optional[str]:
        parts = cn.split("-")
        length = len(parts)
        if length > 2:
            raise ValueError(f"Class name is not supported: {cn}")

        # ex: gray-12, white-10, black-50...
        if length == 2:
            variant, opacity = parts

            if variant not in variants:
                raise ValueError(f"Class name is not supported: {cn}. Variant '{variant}' is not existed.")

            color = variants[variant]
            opacity = int(opacity)

            return color.withOpacity(opacity).toStylesheet()

        # This can be primary, danger, warning or custom color such as [rgb(128, 128, 128)]
        color = parts[0]

        if color in variants:
            return variants[color].toStylesheet()

        if not color.startswith("[") and color.endswith("]"):
            raise ValueError(f"Class name is not supported: {cn}. This is not in custom color format")

        customColor = color[1:-1]
        return customColor
