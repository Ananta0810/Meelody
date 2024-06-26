from typing import Optional

from PyQt5.QtWidgets import QWidget

from app.helpers.stylesheets.translators.props_translators import PaddingTranslator, TextTranslator, RoundedTranslator, BackgroundTranslator, \
    BorderTranslator, ClassName, PropsTranslator
from app.utils.base import Dicts, Strings, Lists
from app.utils.reflections import Classes


class ElementStateStyles:

    def __init__(self, eName: Optional[str], state: Optional[str], value: Optional[list[str]]) -> None:
        self.__id = f"{eName} {'' if state is None else f':{state}'}" if eName is not None else None
        self.__value = value

    def toProps(self, defaultProps: Optional[list[str]] = None) -> Optional[str]:
        if self.__value is None:
            return Strings.joinStyles(defaultProps)

        if defaultProps is None:
            return Strings.joinStyles(self.__value)

        existedKeys = {value.split(":", maxsplit=1)[0] for value in self.__value}
        defaultPropsToUse = [prop for prop in defaultProps if prop.split(":", maxsplit=1)[0] not in existedKeys]

        return Strings.joinStyles(self.__value + defaultPropsToUse)

    def toStyleSheet(self, defaultProps: Optional[list[str]] = None) -> str:
        return f"{self.__id} {{{self.toProps(defaultProps)}}}\n"

    def id(self) -> str:
        return self.__id


_NULL_STATE = ElementStateStyles(None, None, None)


class ClassNameElement:

    def __init__(self) -> None:
        self.__states = {}

    def addState(self, name: str, state: ElementStateStyles) -> None:
        self.__states['none' if name is None else name] = state

    def state(self, name: Optional[str] = None) -> ElementStateStyles:
        name = 'none' if name is None else name
        if name in self.__states:
            return self.__states[name]

        return _NULL_STATE


_NULL_ELEMENT = ClassNameElement()


class ClassNameTheme:

    def __init__(self) -> None:
        self.__elements = {}

    def addElement(self, name: str, states: ClassNameElement) -> None:
        self.__elements['none' if name is None else name] = states

    def getElement(self, name: Optional[str] = None) -> ClassNameElement:
        name = 'none' if name is None else name
        if name in self.__elements:
            return self.__elements[name]

        return _NULL_ELEMENT


_NULL_THEME = ClassNameTheme()

_TRANSLATORS = [BorderTranslator(), BackgroundTranslator(), RoundedTranslator(), TextTranslator(), PaddingTranslator()]


class ClassNameTranslator:
    @staticmethod
    def translateElements(classNames: str, element: QWidget) -> (ClassNameTheme, ClassNameTheme):
        if classNames is None:
            return _NULL_THEME, _NULL_THEME

        darkClassNames = classNames.split(" ")
        darkClassNames.sort(key=lambda cn: 1 if "dark" in cn else 0)
        lightClassNames = [cn for cn in darkClassNames if "dark" not in cn]

        lightStyle = ClassNameTranslator.__toElementStyles(lightClassNames, element)
        darkStyle = ClassNameTranslator.__toElementStyles(darkClassNames, element)
        return lightStyle, darkStyle

    @staticmethod
    def __toElementStyles(classNameList, target) -> ClassNameTheme:
        eName = target.__class__.__name__

        elements = Dicts.group([ClassName.of(cn) for cn in classNameList], by=lambda c: c.element)

        theme = ClassNameTheme()

        for element, elementClasses in elements.items():
            states = Dicts.group(elementClasses, by=lambda c: c.state)

            elementResult = ClassNameElement()
            for state, classes in states.items():
                props = [ClassNameTranslator.__toProp(classes, translator, target) for translator in _TRANSLATORS]
                props = Lists.nonNull(props)
                if len(props) > 0:
                    elementResult.addState(state, ElementStateStyles(eName, state, props))

            theme.addElement(element, elementResult)

        return theme

    @staticmethod
    def translate(classNames: str, element: QWidget) -> (str, str):
        if classNames is None:
            return None, None
        darkClassNames = classNames.split(" ")
        darkClassNames.sort(key=lambda cn: 1 if "dark" in cn else 0)
        lightClassNames = [cn for cn in darkClassNames if "dark" not in cn]

        lightStyle = ClassNameTranslator.__toStyle(lightClassNames, element)
        darkStyle = ClassNameTranslator.__toStyle(darkClassNames, element)
        return lightStyle, darkStyle

    @staticmethod
    def __toStyle(classNameList, element):
        states = Dicts.group([ClassName.of(cn) for cn in classNameList], by=lambda c: c.state)
        eName = ClassNameTranslator.__elementId(element)

        styles = []

        for state, classes in states.items():
            props = [ClassNameTranslator.__toProp(classes, translator, element) for translator in _TRANSLATORS]
            styles.append([f"{eName}{'' if state is None else f':{state}'}", Strings.joinStyles(props)])

        return Strings.join("\n", [f"{id} {{{props}}}" for id, props in styles])

    @staticmethod
    def __elementId(element):
        eName = Classes.typeNameOf(element)
        return eName + f"#{element.objectName()}" if Strings.isNotBlank(element.objectName()) else eName

    @staticmethod
    def __toProp(classNames: list[ClassName], translator: PropsTranslator, element: QWidget):
        ids = translator.ids()
        validNames = [cn for cn in classNames if cn.key in ids]
        if len(validNames) == 0:
            return None
        return translator.translate(validNames, element)
