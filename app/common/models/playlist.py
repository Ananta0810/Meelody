from PyQt5.QtCore import QObject, pyqtSignal

from app.common.models.song import Song


class Playlist:
    class Info:

        def getId(self) -> str:
            """
            Return unique id of playlist.
            """
            ...

        def getName(self) -> str:
            """
                Return name of playlist. This name is not unique.
            """
            ...

        def setName(self, name: str) -> None:
            """
                Change name for playlist.
            """
            ...

        def setCover(self, cover: bytes) -> None:
            """
                Set the cover for playlist. This cover will be used to render to UI.
            """
            ...

        def getCover(self) -> bytes:
            """
                Return cover as bytes to render to UI
            """
            ...

        def getCoverPath(self) -> str:
            """
                Return the path to load cover.
            """
            ...

        def clone(self) -> 'Playlist.Info':
            """
                Clone a shallow copy info from the current one.
            """
            ...

    class Songs(QObject):
        updated = pyqtSignal()

        def clone(self) -> 'Playlist.Songs':
            """
               Create a shallow copy of this instance
            """
            ...

        def setSongs(self, songs: list[Song]) -> None:
            """
                Initialize songs to playlist. A signal will be fired after init succeed.
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

        def insert(self, song: Song) -> None:
            """
                Add song to the list of songs. A signal will be fired after inserted succeed.
            """
            ...

        def insertAll(self, songs: list[Song]) -> None:
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

    def clone(self) -> 'Playlist':
        return Playlist(self.__info.clone(), self.__songs.clone())
