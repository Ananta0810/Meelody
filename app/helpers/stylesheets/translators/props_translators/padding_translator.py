from PyQt5.QtWidgets import QWidget

from app.helpers.stylesheets.translators.props_translators.class_name import ClassName
from app.helpers.stylesheets.translators.props_translators.props_translator import PropsTranslator
from app.utils.base import Dicts


def _paddingOf(cn) -> str:
    return cn.value.split("-")[-1] + "px"


def _toProps(cn: ClassName) -> dict[str, str]:
    if cn.key == "px":
        padding = _paddingOf(cn)
        return {"left": padding, "right": padding}
    if cn.key == "py":
        padding = _paddingOf(cn)
        return {"top": padding, "bottom": padding}
    if cn.key == "pl":
        padding = _paddingOf(cn)
        return {"left": padding}
    if cn.key == "pr":
        padding = _paddingOf(cn)
        return {"right": padding}
    if cn.key == "pt":
        padding = _paddingOf(cn)
        return {"top": padding}
    if cn.key == "pb":
        padding = _paddingOf(cn)
        return {"bottom": padding}
    padding = cn.value
    return {"left": padding, "right": padding, "top": padding, "bottom": padding}


class PaddingTranslator(PropsTranslator):

    def ids(self) -> set[str]:
        return {"p", "px", "py", "pl", "pr", "pt", "pb"}

    def translate(self, names: list[ClassName], target: QWidget) -> str:
        dictionary = Dicts.mergeListOfDicts([_toProps(name) for name in names])

        top = dictionary.get('top', '0px')
        right = dictionary.get('right', '0px')
        bottom = dictionary.get('bottom', '0px')
        left = dictionary.get('left', '0px')

        return f"padding: {top} {right} {bottom} {left}"
