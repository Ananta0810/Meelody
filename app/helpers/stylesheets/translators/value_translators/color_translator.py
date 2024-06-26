from typing import List, Optional

from app.common.statics.styles import Colors
from app.helpers.stylesheets import Color
from app.helpers.stylesheets.translators.value_translators.value_translator import ValueTranslator

_VARIANTS: dict[str, Color] = {
    "primary": Colors.primary,

    "success": Colors.success,
    "danger": Colors.danger,
    "warning": Colors.warning,

    "dark": Colors.dark,
    "white": Colors.white,
    "black": Colors.black,
    "gray": Colors.gray,
    "none": Colors.none,
    "transparent": Colors.none,
}

_CONTRAST_BACKGROUNDS: dict[str, Color] = {
    "b": Colors.black,
    "w": Colors.white
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
