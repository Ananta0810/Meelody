from typing import Callable

from app.common.models import Playlist, Song
from app.helpers.base import Lists, Strings


class PlaylistSongs(Playlist.Songs):

    def __init__(self, songs: list[Song] = None, isSorted: bool = True):
        super().__init__()
        self.__songs: list[Song] = []
        self.__isSorted: bool = isSorted

        if songs is not None:
            self.insertAll(songs)

    def __str__(self):
        string = ""
        for index, song in enumerate(self.__songs):
            string += f"{index}. {str(song)}\n"
        return string

    def setSongs(self, songs: list[Song]) -> None:
        self.__songs = []
        self.insertAll(songs)

    def clone(self) -> Playlist.Songs:
        return PlaylistSongs(self.__songs)

    def getSongs(self) -> list[Song]:
        return [song for song in self.__songs]

    def hasAnySong(self) -> bool:
        return len(self.__songs) > 0

    def hasSong(self, song: Song) -> bool:
        return any(song == song_ for song_ in self.__songs)

    def moveSong(self, fromIndex: int, toIndex: int) -> None:
        Lists.moveElement(self.__songs, fromIndex, toIndex)
        self.updated.emit()

    def size(self) -> int:
        return len(self.__songs)

    def getSongAt(self, index: int) -> Song:
        if self.size() == 0:
            raise ValueError("Playlist has no song.")
        return self.__songs[index]

    def getSongIndexWithId(self, songId: str) -> int:
        if self.size() == 0:
            raise ValueError("Playlist has no song.")

        for index, song in enumerate(self.__songs):
            if song.getId() == songId:
                return index
        return -1

    def insert(self, song: Song) -> None:
        if self.__isSorted:
            position = self.__findInsertPosition(song)
            self.__songs.insert(position, song)
        else:
            self.__songs.append(song)

        song.updated.connect(lambda updatedField: self.__onSongUpdated(song, updatedField))

    def __onSongUpdated(self, song: Song, updatedField: str) -> None:
        if updatedField == "title":
            self.__songs.remove(song)
            newPosition = self.__findInsertPosition(song)
            self.__songs.insert(newPosition, song)
            self.updated.emit()
        if updatedField == "love":
            self.updated.emit()

    def __findInsertPosition(self, song: Song) -> int:
        return Lists.binarySearch(self.__songs, song, comparator=self.__comparator(), nearest=True)

    def __moveSongAfterUpdate(self, song: Song) -> None:
        self.__songs.remove(song)
        newPosition = self.__findInsertPosition(song)
        self.__songs.insert(newPosition, song)

    def insertAll(self, songs: list[Song]):
        if songs is not None:
            for song in songs:
                self.insert(song)
            self.updated.emit()

    def removeAll(self, songs: list[Song]) -> None:
        if songs is not None:
            for song in songs:
                try:
                    self.__songs.remove(song)
                except ValueError:
                    pass
            self.updated.emit()

    def removeSong(self, song: Song) -> None:
        self.__songs.remove(song)
        self.updated.emit()

    def indexOf(self, song: Song) -> int:
        return (
            Lists.binarySearch(self.__songs, song, self.__comparator())
            if self.__isSorted
            else Lists.linearSearch(self.__songs, song, self.__comparator())
        )

    @staticmethod
    def __comparator() -> Callable[[Song, Song], int]:
        return lambda s1, s2: Strings.compare(s1.getTitle(), s2.getTitle())
