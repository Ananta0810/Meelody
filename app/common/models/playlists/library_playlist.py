from contextlib import suppress

from app.common.models.playlist import Playlist
from app.common.models.song import Song
from app.helpers.base import returnOnFailed, SingletonMeta
from .common_playlist import CommonPlaylist


class Library(Playlist, metaclass=SingletonMeta):
    class Info(CommonPlaylist.Info, metaclass=SingletonMeta):
        def __init__(self):
            super().__init__(id="Library", name="Library")

    class Songs(CommonPlaylist.Songs):

        def __init__(self):
            super().__init__(None, isSorted=True)
            self.updated.connect(lambda: self.__saveDatabase())

        def setSongs(self, songs: list[Song]) -> None:
            super().setSongs(songs)

            for song in songs:
                self.__connectToSong(song)

            self.updated.emit()

        def insert(self, song: Song) -> None:
            super().insert(song)
            self.__connectToSong(song)
            self.updated.emit()

        def insertAll(self, songs: list[Song]) -> None:
            super().insertAll(songs)

            if songs is None:
                return

            for song in songs:
                self.__connectToSong(song)

            self.updated.emit()

        def removeAll(self, songs: list[Song]) -> None:
            super().removeAll(songs)
            if songs is None:
                return

            for song in songs:
                self.__disconnectToSong(song)

            self.updated.emit()

        def remove(self, song: Song) -> None:
            super().remove(song)
            self.__disconnectToSong(song)
            self.updated.emit()

        def __connectToSong(self, song: Song) -> None:
            song.updated.connect(lambda updatedField: self._onSongUpdated(song, updatedField))
            song.deleted.connect(lambda: self.remove(song))

        def _onSongUpdated(self, song: Song, updatedField: str) -> None:
            if updatedField == "title":
                self._songs.remove(song)
                newPosition = self.__findInsertPosition(song)
                self._songs.insert(newPosition, song)

            self.updated.emit()

        def __disconnectToSong(self, song: Song) -> None:
            with suppress(TypeError):
                song.updated.disconnect(lambda updatedField: self._onSongUpdated(song, updatedField))
                song.deleted.disconnect(lambda: self.remove(song))

        def moveSong(self, fromIndex: int, toIndex: int) -> None:
            super().moveSong(fromIndex, toIndex)
            self.updated.emit()

        @returnOnFailed(0)
        def getSongIndexWithId(self, songId: str) -> int:
            if self.size() == 0:
                raise 0

            for index, song in enumerate(self._songs):
                if song.getId() == songId:
                    return index
            return 0

        def clone(self) -> Playlist.Songs:
            return self

        def __saveDatabase(self) -> None:
            from app.common.others import database
            database.songs.save(self.getSongs())

    def clone(self) -> 'Playlist':
        return self
