import uuid
from typing import Callable, TypeVar

from app.common.models.song import Song
from app.helpers.base import Lists, Strings

T = TypeVar('T')


class _SongComparator:
    def __init__(self, key_provider: Callable[[Song], T], comparator: Callable[[T, T], int]) -> None:
        self.__key_provider = key_provider
        self.__comparator = comparator

    def keyOf(self, song: Song) -> T:
        return self.__key_provider(song)

    def comparator(self) -> Callable[[Song, Song], int]:
        return lambda s1, s2: self.__comparator(self.__key_provider(s1), self.__key_provider(s2))


_comparatorMap: dict[Song.Order, _SongComparator] = {
    Song.Order.TITLE: _SongComparator(Song.getTitle, Strings.compare),
    Song.Order.ARTIST: _SongComparator(Song.getArtist, Strings.compare),
    Song.Order.LENGTH: _SongComparator(Song.getLength, lambda x, y: x - y),
}


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

    class Songs:

        def __init__(self, songs: list[Song] = None, isSorted: bool = True, orderBy: Song.Order = Song.Order.TITLE):
            self.__songs: list[Song] = []
            self.__orderBy: Song.Order = orderBy
            self.__isSorted: bool = isSorted
            if songs is not None:
                self.insertAll(songs)

        def __str__(self):
            string = ""
            for index, song in enumerate(self.__songs):
                string += f"{index}. {str(song)}\n"
            return string

        def clone(self) -> 'Playlist.Songs':
            return Playlist.Songs(self.__songs, self.__isSorted, self.__orderBy)

        def getSongs(self) -> list[Song]:
            return [song for song in self.__songs]

        def isSorted(self):
            return self.__isSorted

        def hasAnySong(self) -> bool:
            return len(self.__songs) > 0

        def hasSong(self, song: Song) -> bool:
            return any(song == song_ for song_ in self.__songs)

        def moveSong(self, fromIndex: int, toIndex: int) -> None:
            Lists.moveElement(self.__songs, fromIndex, toIndex)

        def size(self) -> int:
            """
            return the number of songs in the list
            """
            return len(self.__songs)

        def setOrderBy(self, prop: Song.Order.TITLE) -> None:
            self.__orderBy = prop

        def getSongAt(self, index: int) -> Song:
            """
            Get the song at the given index
            """
            if self.size() == 0:
                raise ValueError("Playlist has no song.")
            return self.__songs[index]

        def getSongIndexWithId(self, songId: str) -> int:
            """
            Get the song at the given index
            """
            if self.size() == 0:
                raise ValueError("Playlist has no song.")

            for index, song in enumerate(self.__songs):
                if song.getId() == songId:
                    return index
            return -1

        def insert(self, song: Song) -> int:
            """
            Add song to the list of songs. If added successfully, it will return the position of the song in the playlist
            """
            position = self.__findInsertPosition(song)

            if self.isSorted():
                self.__songs.insert(position, song)
                return position

            self.__songs.append(song)
            return len(self.__songs) - 1

        def __findInsertPosition(self, song) -> int:
            return Lists.binarySearch(self.__songs, song, comparator=self.__comparator(), nearest=True)

        def insertAll(self, songs: list[Song]):
            if songs is not None:
                for song in songs:
                    self.insert(song)

        def removeSong(self, song: Song) -> None:
            if self.isSorted():
                indexToRemoveOnBackupSongs = Lists.binarySearch(self.__songs, song, self.__comparator())

                self.__songs.remove(self.__songs[indexToRemoveOnBackupSongs])
                return

            indexToRemoveOnDisplaySongs = Lists.linearSearch(self.__songs, song, self.__comparator())

            self.__songs.remove(self.__songs[indexToRemoveOnDisplaySongs])

        def indexOf(self, song: Song) -> int:
            """
            Find the index Of song in the list
            """
            return (
                Lists.binarySearch(self.__songs, song, self.__comparator())
                if self.__isSorted
                else Lists.linearSearch(self.__songs, song, self.__comparator())
            )

        def __comparator(self):
            return _comparatorMap[self.__orderBy].comparator()

    def __init__(self, info: 'Playlist.Info', songs: 'Playlist.Songs'):
        self.__info = info
        self.__songs = songs

    @staticmethod
    def create(name: str, cover: bytes = None, songs: 'Playlist.Songs' = None) -> 'Playlist':
        return Playlist(Playlist.Info(name, cover), songs or Playlist.Songs())

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
