import os
from contextlib import suppress
from typing import Optional

from app.common.models import ThemeMode
from app.helpers.base import SingletonMeta
from app.helpers.others import Jsons

SETTINGS_PATH = "configuration/settings.json"


class AppSettings(metaclass=SingletonMeta):

    def __init__(self) -> None:
        playingSongId, isLooping, isShuffle, theme = self.__loadSettings()

        self.__playingSongId: Optional[str] = playingSongId
        self.__isLooping: bool = isLooping
        self.__isShuffle: bool = isShuffle
        self.__theme: ThemeMode = ThemeMode.of(theme)

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

    @staticmethod
    def __loadSettings() -> (str, bool, bool):
        with suppress(Exception):
            if os.path.exists(SETTINGS_PATH):
                data: dict = Jsons.readFromFile(SETTINGS_PATH) or {}
                return data.get('song_id', None), data.get('loop', False), data.get('shuffle', False), data.get('theme', f"{ThemeMode.SYSTEM}")

        Jsons.writeToFile(SETTINGS_PATH, {'song_id': None, 'loop': False, 'shuffle': False, 'theme': f"{ThemeMode.SYSTEM}"})
        return None, False, False, f"{ThemeMode.SYSTEM}"

    def __save(self) -> None:
        Jsons.writeToFile(SETTINGS_PATH,
                          {'song_id': self.playingSongId, 'loop': self.isLooping, 'shuffle': self.isShuffle, 'theme': f"{self.__theme}"})
