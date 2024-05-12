import os
from contextlib import suppress
from typing import Optional

from app.common.statics.enums import ThemeMode
from app.utils.base import SingletonMeta
from app.utils.others import Jsons

SETTINGS_PATH = "configuration/settings.json"


class AppSettings(metaclass=SingletonMeta):

    def __init__(self) -> None:
        data = self.__loadSettings()

        self.__playingSongId: Optional[str] = data.get('song_id')
        self.__isLooping: bool = data.get('loop')
        self.__isShuffle: bool = data.get('shuffle')
        self.__theme: ThemeMode = ThemeMode.of(data.get('theme'))
        self.__language: str = data.get('lang')

    @property
    def playingSongId(self) -> Optional[str]:
        return self.__playingSongId

    @property
    def isLooping(self) -> bool:
        return self.__isLooping

    @property
    def isShuffle(self) -> bool:
        return self.__isShuffle

    @property
    def theme(self) -> ThemeMode:
        return self.__theme

    @property
    def language(self) -> str:
        return self.__language

    def setPlayingSongId(self, id: str) -> None:
        if self.__playingSongId != id:
            self.__playingSongId = id
            self.__save()

    def setIsLooping(self, a0: bool) -> None:
        if self.__isLooping != a0:
            self.__isLooping = a0
            self.__save()

    def setIsShuffle(self, a0: bool) -> None:
        if self.__isShuffle != a0:
            self.__isShuffle = a0
            self.__save()

    def setTheme(self, a0: ThemeMode) -> None:
        if self.__theme != a0:
            self.__theme = a0
            self.__save()

    def setLanguage(self, a0: str) -> None:
        if self.__language != a0:
            self.__language = a0
            self.__save()

    @staticmethod
    def __loadSettings() -> (str, bool, bool):
        defaultSettings = {'song_id': None, 'loop': False, 'shuffle': False, 'theme': f"{ThemeMode.SYSTEM}", 'lang': "en"}

        with suppress(Exception):
            if os.path.exists(SETTINGS_PATH):
                data: dict = Jsons.readFromFile(SETTINGS_PATH) or {}
                return {
                    'song_id': data.get('song_id', defaultSettings['song_id']),
                    'loop': data.get('loop', defaultSettings['loop']),
                    'shuffle': data.get('shuffle', defaultSettings['shuffle']),
                    'theme': data.get('theme', defaultSettings['theme']),
                    'lang': data.get('lang', defaultSettings['lang']),
                }

        Jsons.writeToFile(SETTINGS_PATH, defaultSettings)
        return defaultSettings

    def __save(self) -> None:
        Jsons.writeToFile(SETTINGS_PATH,
                          {'song_id': self.playingSongId,
                           'loop': self.isLooping,
                           'shuffle': self.isShuffle,
                           'theme': f"{self.theme}",
                           'lang': self.language})
