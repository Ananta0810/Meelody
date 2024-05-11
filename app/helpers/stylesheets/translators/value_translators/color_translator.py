from typing import List, Optional

from app.helpers.stylesheets import Color, Colors
from app.helpers.stylesheets.translators.value_translators.value_translator import ValueTranslator

_VARIANTS: dict[str, Color] = {
    "primary": Colors.PRIMARY,

    "success": Colors.SUCCESS,
    "danger": Colors.DANGER,
    "warning": Colors.WARNING,

    "dark": Colors.DARK,
    "white": Colors.WHITE,
    "black": Colors.BLACK,
    "gray": Colors.GRAY,
    "none": Colors.NONE,
    "transparent": Colors.NONE,
}

_CONTRAST_BACKGROUNDS: dict[str, Color] = {
    "b": Colors.BLACK,
    "w": Colors.WHITE
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
            variant, mayBeOpacity = parts

            if variant not in _VARIANTS:
                raise ValueError(f"Class name is not supported: {cn}. Variant '{variant}' is not existed.")

            color = _VARIANTS[variant]

            isSolidColor = mayBeOpacity.startswith("[") and mayBeOpacity.endswith("]")
            if not isSolidColor:
                opacity = int(mayBeOpacity)
                return color.darken(opacity / 100).toStylesheet() if opacity > 100 else color.withOpacity(opacity).toStylesheet()

            mayBeOpacity = mayBeOpacity[1:-1]
            contrastBg = mayBeOpacity.rstrip('0123456789')
            opacity = mayBeOpacity[len(contrastBg):]

            if contrastBg not in _CONTRAST_BACKGROUNDS:
                raise ValueError(f"Class name is not supported: {cn}. contrast background '{contrastBg}' is not existed.")

            contrastBackgroundColor = _CONTRAST_BACKGROUNDS[contrastBg]
            opacity_ = int(opacity)

            if opacity_ > 100:
                return color.darken(opacity_ / 100)

            return color.withOpacity(opacity_).toSolidColor(contrastBackgroundColor).toStylesheet()

        # This can be primary, danger, warning or custom color such as [rgb(128, 128, 128)]
        color = parts[0]

        if color in _VARIANTS:
            return _VARIANTS[color].toStylesheet()

        if not color.startswith("[") and color.endswith("]"):
            raise ValueError(f"Class name is not supported: {cn}. This is not in custom color format")

        customColor = color[1:-1]
        return customColor
