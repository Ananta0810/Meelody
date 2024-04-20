from PyQt5.QtWidgets import QWidget

from app.helpers.base import Dicts, Strings
from app.helpers.stylesheets.translators.props_translators.class_name import ClassName
from app.helpers.stylesheets.translators.props_translators.props_translator import PropsTranslator
from app.helpers.stylesheets.translators.props_translators.props_translators import PropsTranslators


class ClassNameTranslator:
    @staticmethod
    def translate(classNames: str, element: QWidget) -> str:
        states = Dicts.group([ClassName.of(cn) for cn in classNames.split(" ")], by=lambda c: c.state)
        elementName = element.__class__.__name__
        translators = PropsTranslators.Translators

        result = ""
        for state, classes in states.items():
            props = [ClassNameTranslator.translate_(classes, translator, element) for translator in translators]
            stylesheets = Strings.join(props, ";")
            result += f"{elementName}{'' if state is None else f':{state}'} {{{stylesheets}}}\n"

        return result

    @staticmethod
    def translate_(classNames: list[ClassName], translator: PropsTranslator, element: QWidget):
        id_ = translator.id()
        validNames = [cn for cn in classNames if id_ == cn.key]
        if len(validNames) == 0:
            return None
        return translator.translate(validNames, element)
