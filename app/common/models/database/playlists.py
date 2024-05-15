import os

from PyQt5.QtCore import QObject, pyqtSignal, pyqtBoundSignal

from app.common.models import Song, Playlist
from app.common.models.playlists import UserPlaylist
from app.utils.others import Jsons
from app.utils.reflections import SingletonQObjectMeta


class _Database:

    def __init__(self, path: str) -> None:
        self.__path = path

    def load(self, songs: list[Song]) -> list[Playlist]:
        if os.path.exists(self.__path):
            data: list[dict] = Jsons.readFromFile(self.__path)
            if data is not None:
                return [UserPlaylist.fromDict(item, songs) for item in data]

        self.save([])
        return []

    def save(self, data: list[UserPlaylist]) -> None:
        data = [playlist.toDict() for playlist in data]
        Jsons.writeToFile(self.__path, data)


class Playlists(QObject, metaclass=SingletonQObjectMeta):
    loaded: pyqtBoundSignal = pyqtSignal()
    changed: pyqtBoundSignal = pyqtSignal(list)

    def __init__(self, librarySongs: list[Song]) -> None:
        super().__init__()
        self.__items = []
        self.__database = _Database("configuration/playlists.json")
        self.__load(librarySongs)

        self.changed.connect(lambda playlists_: self.__updateToDatabase())

    def __load(self, songs: list[Song]) -> None:
        items = self.__database.load(songs)

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
        return self.__database.save([item for item in self.__items])
