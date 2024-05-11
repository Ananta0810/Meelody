import json
import os.path

from PyQt5.QtCore import QObject, pyqtSignal


class Translator(QObject):
    changed = pyqtSignal()

    def __init__(self):
        super().__init__(None)
        self.__dictionary = {}

    def setLanguage(self, lang: str) -> None:
        fileName = f"app/resource/lang/{lang}.json"
        if not os.path.exists(fileName):
            fileName = f"app/resource/lang/en.json"

        with open(fileName, 'r', encoding='utf-8') as file:
            self.__dictionary = json.load(file)

        self.changed.emit()

    def translate(self, key: str) -> str:
        section, key = key.split(".", maxsplit=1)
        return self.__dictionary.get(section).get(key)


translator = Translator()
