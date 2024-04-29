from typing import Optional

from PyQt5.QtCore import QObject, pyqtSignal

from app.common.models import Playlist


class Playlists(QObject):
    changed = pyqtSignal(list)

    def __init__(self, items: Optional[list[Playlist]] = None) -> None:
        super().__init__()
        self.__items = items or []
        self.changed.emit(self.__items)

    def append(self, item: Playlist) -> None:
        self.__items.append(item)
        self.changed.emit(self.__items)

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

    def validItems(self) -> list:
        return [item for item in self.__items if not item.getInfo().isNew()]
