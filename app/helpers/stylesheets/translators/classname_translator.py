from typing import Optional

from PyQt5.QtWidgets import QWidget

from app.helpers.base import Dicts, Strings, Lists, Classes
from app.helpers.stylesheets.translators.props_translators.class_name import ClassName
from app.helpers.stylesheets.translators.props_translators.props_translator import PropsTranslator
from app.helpers.stylesheets.translators.props_translators.props_translators import PropsTranslators


class ElementStateStyles:

    def __init__(self, eName: Optional[str], state: Optional[str], value: Optional[list[str]]) -> None:
        self.id = f"{eName} {'' if state is None else f':{state}'}" if eName is not None else None
        self.value = value

    def toProps(self) -> Optional[str]:
        if self.value is None:
            return None
        return Strings.join(self.value, ";")

    def id(self) -> str:
        return self.id


NULL_STATE = ElementStateStyles(None, None, None)


class ClassNameElement:

    def __init__(self) -> None:
        self.__states = {}

    def addState(self, name: str, state: ElementStateStyles) -> None:
        self.__states['none' if name is None else name] = state

    def state(self, name: str = None) -> ElementStateStyles:
        name = 'none' if name is None else name
        if name in self.__states:
            return self.__states[name]

        return NULL_STATE


NULL_ELEMENT = ClassNameElement()


class ClassNameTheme:

    def __init__(self) -> None:
        self.__elements = {}

    def addElement(self, name: str, states: ClassNameElement) -> None:
        self.__elements['none' if name is None else name] = states

    def getElement(self, name: str) -> ClassNameElement:
        name = 'none' if name is None else name
        if name in self.__elements:
            return self.__elements[name]

        return NULL_ELEMENT


class ClassNameTranslator:
    @staticmethod
    def translateElements(classNames: str, element: QWidget) -> (ClassNameTheme, ClassNameTheme):
        darkClassNames = classNames.split(" ")
        darkClassNames.sort(key=lambda cn: 1 if "dark" in cn else 0)
        lightClassNames = [cn for cn in darkClassNames if "dark" not in cn]

        lightStyle = ClassNameTranslator.__toElementStyles(lightClassNames, element)
        darkStyle = ClassNameTranslator.__toElementStyles(darkClassNames, element)
        return lightStyle, darkStyle

    @staticmethod
    def __toElementStyles(classNameList, element) -> ClassNameTheme:
        eName = element.__class__.__name__
        translators = PropsTranslators.Translators

        elements = Dicts.group([ClassName.of(cn) for cn in classNameList], by=lambda c: c.element)

        theme = ClassNameTheme()

        for element, elementClasses in elements.items():
            states = Dicts.group(elementClasses, by=lambda c: c.state)

            elementResult = ClassNameElement()
            for state, classes in states.items():
                props = [ClassNameTranslator.__toProp(classes, translator, element) for translator in translators]
                props = Lists.nonNull(props)
                if len(props) > 0:
                    elementResult.addState(state, ElementStateStyles(eName, state, props))

            theme.addElement(element, elementResult)

        return theme

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
        eName = Classes.typeNameOf(element)
        translators = PropsTranslators.Translators
        result = ""
        for state, classes in states.items():
            props = [ClassNameTranslator.__toProp(classes, translator, element) for translator in translators]
            result += f"{eName}{'' if state is None else f':{state}'} {{{Strings.join(props, ';')}}}\n"
        return result

    @staticmethod
    def __toProp(classNames: list[ClassName], translator: PropsTranslator, element: QWidget):
        id_ = translator.id()
        validNames = [cn for cn in classNames if id_ == cn.key]
        if len(validNames) == 0:
            return None
        return translator.translate(validNames, element)
