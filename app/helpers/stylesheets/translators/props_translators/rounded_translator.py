from PyQt5.QtWidgets import QWidget

from app.helpers.base import Lists
from app.helpers.stylesheets.translators.props_translators.class_name import ClassName
from app.helpers.stylesheets.translators.props_translators.props_translator import PropsTranslator

__SIZES = {
    "sm": 2,
    "md": 4,
    "lg": 8,
    "xl": 16,
    "2xl": 32
}


def _toProps(cn: ClassName, target: QWidget) -> int | float:
    if cn.value is None:
        raise ValueError("Please add value to rounded")

    if cn.value == "full":
        smallerEdge = min(target.width(), target.height())
        return smallerEdge / 2

    if cn.value in __SIZES:
        return __SIZES[cn.value]

    if "/" in cn.value:
        smallerEdge = min(target.width(), target.height())
        return smallerEdge * float(cn.value)

    return float(cn.value)


class RoundedTranslator(PropsTranslator):

    def ids(self) -> set[str]:
        return {"rounded"}

    def translate(self, names: list[ClassName], target: QWidget) -> str:
        cn = Lists.lastOf(names)
        result = _toProps(cn, target)

        return f"border-radius: {result}px"
