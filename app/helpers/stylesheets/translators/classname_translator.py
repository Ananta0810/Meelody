from typing import List

from app.helpers.stylesheets.translators.props_translators.props_translator import PropsTranslator
from app.helpers.stylesheets.translators.props_translators.props_translators import PropsTranslators


class ClassNameTranslator:
    @staticmethod
    def translate(classNames: str) -> List[str]:
        classes = classNames.split(" ")
        stylesheets = [ClassNameTranslator.translateProps(classes, translator) for translator in
                       [PropsTranslators.Border, PropsTranslators.Background]]
        return [v for v in stylesheets if v is not None]

    @staticmethod
    def translateProps(classNames: List[str], translator: PropsTranslator):
        id_ = translator.id()
        validNames = [name for name in classNames if id_ in name]
        if len(validNames) == 0:
            return None
        return translator.translate(validNames)
