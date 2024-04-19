from typing import List

from app.helpers.stylesheets import Color, Background
from app.helpers.stylesheets.translators.props_translators.props_translator import PropsTranslator
from app.helpers.stylesheets.translators.value_translators import ValueTranslators


def _toProps(name: str) -> Color | None:
    color = name[name.find('-') + 1:]
    try:
        if color in ["transparent", "none"]:
            return None

        return ValueTranslators.Color.translate([color])
    except Exception:
        raise ValueError(f"Invalid className: {name}")


class BackgroundTranslator(PropsTranslator[Background]):
    __defaultSize = 1
    __defaultColor = Color(128, 128, 128)
    __defaultStyle = "solid"

    def id(self) -> str:
        return "bg"

    def translate(self, names: List[str]) -> Background:
        color = _toProps(names[-1])
        return Background(color)
