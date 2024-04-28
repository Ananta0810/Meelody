from PyQt5.QtWidgets import QWidget

from app.helpers.base import Dicts
from app.helpers.stylesheets.translators.props_translators.class_name import ClassName
from app.helpers.stylesheets.translators.props_translators.props_translator import PropsTranslator


def _paddingOf(cn):
    return cn.value.split("-")[-1] + "px"


def _toProps(cn: ClassName):
    if "x-" in cn.value:
        padding = _paddingOf(cn)
        return {"left": padding, "right": padding}
    if "y-" in cn.value:
        padding = _paddingOf(cn)
        return {"top": padding, "bottom": padding}
    if "l-" in cn.value:
        padding = _paddingOf(cn)
        return {"left": padding}
    if "r-" in cn.value:
        padding = _paddingOf(cn)
        return {"right": padding}
    if "t-" in cn.value:
        padding = _paddingOf(cn)
        return {"top": padding}
    if "b-" in cn.value:
        padding = _paddingOf(cn)
        return {"bottom": padding}
    padding = cn.value
    return {"left": padding, "right": padding, "top": padding, "bottom": padding}


class PaddingTranslator(PropsTranslator):

    def id(self) -> str:
        return "p"

    def translate(self, names: list[ClassName], target: QWidget) -> str:
        dictionary = Dicts.mergeListOfDicts([_toProps(name) for name in names])

        top = dictionary.get('top', '0px')
        right = dictionary.get('right', '0px')
        bottom = dictionary.get('bottom', '0px')
        left = dictionary.get('left', '0px')

        return f"padding: {top} {right} {bottom} {left}"
