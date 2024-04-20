from PyQt5.QtWidgets import QWidget

from app.helpers.base import Dicts, Strings
from app.helpers.stylesheets.translators.props_translators.class_name import ClassName
from app.helpers.stylesheets.translators.props_translators.props_translator import PropsTranslator
from app.helpers.stylesheets.translators.props_translators.props_translators import PropsTranslators


class ClassNameTranslator:
    @staticmethod
    def translate(classNames: str, element: QWidget) -> (str, str):
        darkClassNames = classNames.split(" ")
        darkClassNames.sort(key=lambda cn: 1 if "dark" in cn else 0)
        lightClassNames = [cn for cn in darkClassNames if "dark" not in cn]

        lightStyle = ClassNameTranslator.__toStyle(lightClassNames, element)
        darkStyle = ClassNameTranslator.__toStyle(darkClassNames, element)
        return lightStyle, darkStyle

    @staticmethod
    def __toStyle(classNameList, element):
        states = Dicts.group([ClassName.of(cn) for cn in classNameList], by=lambda c: c.state)
        elementName = element.__class__.__name__
        translators = PropsTranslators.Translators
        result = ""
        for state, classes in states.items():
            props = [ClassNameTranslator.__toProp(classes, translator, element) for translator in translators]
            result += f"{elementName}{'' if state is None else f':{state}'} {{{Strings.join(props, ';')}}}\n"
        return result

    @staticmethod
    def __toProp(classNames: list[ClassName], translator: PropsTranslator, element: QWidget):
        id_ = translator.id()
        validNames = [cn for cn in classNames if id_ == cn.key]
        if len(validNames) == 0:
            return None
        translate = translator.translate(validNames, element)
        return translate
