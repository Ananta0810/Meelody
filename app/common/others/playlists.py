from PyQt5.QtCore import QObject, pyqtSignal

from app.common.models import Playlist
from .database import database


class Playlists(QObject):
    loaded = pyqtSignal()
    changed = pyqtSignal(list)

    def __init__(self) -> None:
        super().__init__()
        self.__items = []
        self.changed.connect(lambda playlists_: self.__updateToDatabase())

    def load(self, items: list[Playlist]) -> None:
        for item in items:
            self.__items.append(item)
            item.getSongs().updated.connect(lambda: self.__updateToDatabase())
        self.loaded.emit()

    def append(self, item: Playlist) -> None:
        self.__items.append(item)
        item.getSongs().updated.connect(lambda: self.__updateToDatabase())
        self.changed.emit(self.__items)

    def appendAll(self, items: list[Playlist]) -> None:
        for item in items:
            self.__items.append(item)
            item.getSongs().updated.connect(lambda: self.__updateToDatabase())
        self.changed.emit(self.__items)

    def replace(self, item: Playlist) -> None:
        for index, playlist in enumerate(self.__items):
            if playlist.getInfo().getId() == item.getInfo().getId():
                self.__items[index] = item
                self.changed.emit(self.__items)
                break

    def remove(self, item: Playlist) -> None:
        self.__items.remove(item)
        self.changed.emit(self.__items)

    def removeAt(self, index: int) -> None:
        self.__items.remove(self.__items[index])
        self.changed.emit(self.__items)

    def items(self) -> list:
        return self.__items

    def __updateToDatabase(self):
        validItems = [item for item in self.__items if not item.getInfo().isNew()]
        return database.playlists.save(validItems)
