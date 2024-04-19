from app.helpers.stylesheets import StylesheetProps
from app.helpers.stylesheets.translators.props_translators.props_translators import PropsTranslators


class ClassNameTranslator:
    @staticmethod
    def translate(classNames: str) -> StylesheetProps:
        return PropsTranslators.Border.translate(
            [name for name in classNames.split(" ") if PropsTranslators.Border.id()])
