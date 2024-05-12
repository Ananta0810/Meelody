from PyQt5.QtWidgets import QWidget

from app.helpers.stylesheets import Colors
from app.helpers.stylesheets.translators.props_translators.class_name import ClassName
from app.helpers.stylesheets.translators.props_translators.props_translator import PropsTranslator
from app.helpers.stylesheets.translators.value_translators import ValueTranslators


def _toProps(cn: ClassName) -> str:
    color = cn.value
    if color is None:
        raise ValueError(f"Invalid color, please add color to {cn}")
    try:
        if color in ["transparent", "none"]:
            return Colors.none.toStylesheet()

        return ValueTranslators.Color.translate([color])
    except Exception:
        raise ValueError(f"Invalid className: {cn}")


class BackgroundTranslator(PropsTranslator):

    def ids(self) -> set[str]:
        return {"bg"}

    def translate(self, names: list[ClassName], target: QWidget) -> str:
        color = _toProps(names[-1])
        return f"background-color: {color}"
