from typing import Optional

from PyQt5.QtCore import QObject, pyqtSignal

from app.common.models import Playlist
from .database import database


class Playlists(QObject):
    changed = pyqtSignal(list)

    def __init__(self, items: Optional[list[Playlist]] = None) -> None:
        super().__init__()
        self.__items = items or []
        self.changed.emit(self.__items)

    def append(self, item: Playlist) -> None:
        self.__items = self.saveTempPlaylist(item)
        self.changed.emit(self.__items)

    def saveTempPlaylist(self, item) -> list[Playlist]:
        tempPlaylist = [playlist for playlist in self.__items]
        tempPlaylist.append(item)
        database.playlists.save(self.__validItemsOf(tempPlaylist))
        return tempPlaylist

    def appendAll(self, items: list[Playlist]) -> None:
        for item in items:
            self.__items.append(item)
        self.changed.emit(self.__items)

    def remove(self, item: Playlist) -> None:
        self.__items.remove(item)
        self.changed.emit(self.__items)

    def removeAt(self, index: int) -> None:
        self.__items.remove(self.__items[index])
        self.changed.emit(self.__items)

    def items(self) -> list:
        return self.__items

    @staticmethod
    def __validItemsOf(tempPlaylist):
        return [item for item in tempPlaylist if not item.getInfo().isNew()]
