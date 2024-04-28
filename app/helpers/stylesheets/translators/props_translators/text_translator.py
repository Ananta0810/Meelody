from PyQt5.QtWidgets import QWidget

from app.helpers.stylesheets import Color
from app.helpers.stylesheets.translators.props_translators.class_name import ClassName
from app.helpers.stylesheets.translators.props_translators.props_translator import PropsTranslator
from app.helpers.stylesheets.translators.value_translators import ValueTranslators


def _toProps(cn: ClassName) -> Color | None:
    color = cn.value
    if color is None:
        raise ValueError(f"Invalid color, please add color to {cn}")
    try:
        return ValueTranslators.Color.translate([color])
    except Exception:
        raise ValueError(f"Invalid className: {cn}")


class TextTranslator(PropsTranslator):

    def ids(self) -> set[str]:
        return {"text"}

    def translate(self, names: list[ClassName], target: QWidget) -> str:
        color = _toProps(names[-1])
        return f"color: {color.toStylesheet()}"
