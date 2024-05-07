from typing import Callable

from app.common.models.playlist import Playlist
from app.common.models.song import Song
from app.helpers.base import Lists, Strings


class CommonPlaylist:
    class Info(Playlist.Info):
        def __init__(self, name: str = None, cover: bytes = None, coverPath: str = None, id: str | None = None):
            self.__name: str = name
            self.__cover: bytes = cover
            self.__coverPath: str = coverPath
            self.__id: str = id or str(Strings.randomId())

        def __eq__(self, other: Playlist.Info) -> bool:
            return Strings.equals(self.getName(), other.getName()) and self.getCoverPath() == other.getCoverPath()

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

        def clone(self) -> Playlist.Info:
            return CommonPlaylist.Info(self.__name, self.__cover, self.__coverPath, self.__id)

    class Songs(Playlist.Songs):

        def __init__(self, songs: list[Song] = None, isSorted: bool = True):
            super().__init__()
            self._songs: list[Song] = []
            self._isSorted: bool = isSorted

            if songs is not None:
                self.insertAll(songs)

        def __str__(self):
            string = ""
            for index, song in enumerate(self._songs):
                string += f"{index}. {str(song)}\n"
            return string

        def setSongs(self, songs: list[Song]) -> None:
            self._songs = []
            self.insertAll(songs)

        def clone(self) -> Playlist.Songs:
            return CommonPlaylist.Songs(self._songs)

        def getSongs(self) -> list[Song]:
            return [song for song in self._songs]

        def hasAnySong(self) -> bool:
            return len(self._songs) > 0

        def hasSong(self, song: Song) -> bool:
            return any(song == song_ for song_ in self._songs)

        def moveSong(self, fromIndex: int, toIndex: int) -> None:
            Lists.moveElement(self._songs, fromIndex, toIndex)

        def size(self) -> int:
            return len(self._songs)

        def getSongAt(self, index: int) -> Song:
            if self.size() == 0:
                raise ValueError("Playlist has no song.")
            return self._songs[index]

        def insert(self, song: Song) -> None:
            self._insert(song)

        def _insert(self, song: Song) -> None:
            if self._isSorted:
                position = self.__findInsertPosition(song)
                self._songs.insert(position, song)
            else:
                self._songs.append(song)

        def __findInsertPosition(self, song: Song) -> int:
            return Lists.binarySearch(self._songs, song, comparator=self.__comparator(), nearest=True)

        def __moveSongAfterUpdate(self, song: Song) -> None:
            self._songs.remove(song)
            newPosition = self.__findInsertPosition(song)
            self._songs.insert(newPosition, song)

        def insertAll(self, songs: list[Song]) -> None:
            if songs is not None:
                for song in songs:
                    self._insert(song)

        def removeAll(self, songs: list[Song]) -> None:
            if songs is not None:
                for song in songs:
                    try:
                        self._songs.remove(song)
                    except ValueError:
                        pass

        def remove(self, song: Song) -> None:
            try:
                self._songs.remove(song)
            except ValueError:
                pass

        def indexOf(self, song: Song) -> int:
            return (
                Lists.binarySearch(self._songs, song, self.__comparator())
                if self._isSorted
                else Lists.linearSearch(self._songs, song, self.__comparator())
            )

        @staticmethod
        def __comparator() -> Callable[[Song, Song], int]:
            return lambda s1, s2: Strings.compare(s1.getTitle(), s2.getTitle())
