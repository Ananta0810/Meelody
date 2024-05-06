import uuid

from PyQt5.QtCore import QObject, pyqtSignal

from app.common.models.song import Song
from app.helpers.base import Strings


class Playlist:
    class Info:
        def __init__(self, name: str = None, cover: bytes = None, coverPath: str = None, id: str | None = None):
            self.__name: str = name
            self.__cover: bytes = cover
            self.__coverPath: str = coverPath
            self.__id: str = id or str(uuid.uuid4())

        def __eq__(self, other: 'Playlist.Info') -> bool:
            return Strings.equals(self.__name, other.__name) and self.__cover == other.__cover

        def getId(self) -> str:
            return self.__id

        def getName(self) -> str:
            return self.__name

        def setName(self, name: str) -> None:
            self.__name = name

        def setCover(self, cover: bytes) -> None:
            self.__cover = cover

        def getCover(self) -> bytes:
            return self.__cover

        def getCoverPath(self) -> str:
            return self.__coverPath

        def isNew(self) -> bool:
            return self.__name is None

        def clone(self) -> 'Playlist.Info':
            return Playlist.Info(self.__name, self.__cover, self.__coverPath, self.__id)

    class Songs(QObject):
        updated = pyqtSignal()

        def clone(self) -> 'Playlist.Songs':
            """
               Create a shallow copy of this instance
            """
            ...

        def setSongs(self, songs: list[Song]) -> None:
            """
                Initialize songs to library. A signal will be fired after init succeed.
            """
            ...

        def getSongs(self) -> list[Song]:
            """
                Get a copy list of songs.
            """
            ...

        def hasAnySong(self) -> bool:
            """
                Check if the playlist songs is empty or not.
            """
            ...

        def hasSong(self, song: Song) -> bool:
            """
                Check if certain song existed in the playlist.
            """
            ...

        def moveSong(self, fromIndex: int, toIndex: int) -> None:
            """
                Move a song from certain position to another position.
            """
            ...

        def size(self) -> int:
            """
                return the number of songs in the list
            """
            ...

        def indexOf(self, song: Song) -> int:
            """
                Find the index Of song in the list
            """
            ...

        def getSongAt(self, index: int) -> Song:
            """
                Get the song at the given index
            """
            ...

        def getSongIndexWithId(self, songId: str) -> int:
            """
                Find index of a song by its id. Return -1  if no song found.
            """
            ...

        def insert(self, song: Song) -> None:
            """
                Add song to the list of songs. A signal will be fired after inserted succeed.
            """
            ...

        def insertAll(self, songs: list[Song]):
            """
                Add list of songs to the list of songs. A signal will be fired after inserted succeed.
            """
            ...

        def remove(self, song: Song) -> None:
            """
                Remove a song from current playlist if found. A signal will be fired after inserted succeed.
            """
            ...

        def removeAll(self, songs: list[Song]) -> None:
            """
                Remove list of songs from current playlist. A signal will be fired after inserted succeed.
            """
            ...

    def __init__(self, info: 'Playlist.Info', songs: 'Playlist.Songs'):
        self.__info = info
        self.__songs = songs

    def getInfo(self) -> 'Playlist.Info':
        return self.__info

    def getSongs(self) -> 'Playlist.Songs':
        return self.__songs

    def size(self) -> int:
        """
        :return: total songs of this playlist. 0 if playlist has no songs.
        :rtype: int
        """
        return 0 if self.__songs is None else self.__songs.size()

    def equals(self, other) -> bool:
        """
        Check if two playlists are the same one
        """
        return self.__info == other.__info

    def clone(self) -> 'Playlist':
        return Playlist(self.__info.clone(), self.__songs.clone())
