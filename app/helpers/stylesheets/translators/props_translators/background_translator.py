from typing import List

from PyQt5.QtWidgets import QWidget

from app.helpers.stylesheets import Color
from app.helpers.stylesheets.translators.props_translators.class_name import ClassName
from app.helpers.stylesheets.translators.props_translators.props_translator import PropsTranslator
from app.helpers.stylesheets.translators.value_translators import ValueTranslators

TRANSPARENT_COLOR = Color(0, 0, 0, 0)


def _toProps(cn: ClassName) -> Color | None:
    color = cn.value
    if color is None:
        raise ValueError(f"Invalid color, please add color to {cn}")
    try:
        if color in ["transparent", "none"]:
            return TRANSPARENT_COLOR

        return ValueTranslators.Color.translate([color])
    except Exception:
        raise ValueError(f"Invalid className: {cn}")


class BackgroundTranslator(PropsTranslator):
    __defaultSize = 1
    __defaultColor = Color(128, 128, 128)
    __defaultStyle = "solid"

    def id(self) -> str:
        return "bg"

    def translate(self, names: List[ClassName], target: QWidget) -> str:
        color = _toProps(names[-1])
        return f"background: {'None' if color is None else color.toStylesheet()}"
