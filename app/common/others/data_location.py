from PyQt5.QtCore import QObject, QDir, QStandardPaths

from app.utils.others import Logger
from app.utils.reflections import SingletonQObjectMeta


class DataLocation(QObject, metaclass=SingletonQObjectMeta):
    def __init__(self) -> None:
        super().__init__()
        self.__dataPath: str = QStandardPaths.writableLocation(QStandardPaths.AppLocalDataLocation) + "/Meelody"
        dataPathDir = QDir(self.__dataPath)
        if not dataPathDir.exists():
            # create the directory (including parent directories if they don't exist);
            # that the argument of mkpath is relative to the QDir's object path, so
            # using '.' means that it will create the actual dataPath
            dataPathDir.mkpath('.')

        Logger.info(f"Current application appdata in '{self.__dataPath}'")

    @property
    def library(self) -> str:
        return f"{self.__dataPath}/library"

    @property
    def configuration(self) -> str:
        return f"{self.__dataPath}/configuration"
