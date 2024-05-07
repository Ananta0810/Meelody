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
            self.updated.emit()

        def insert(self, song: Song) -> None:
            super().insert(song)
            song.updated.connect(lambda updatedField: self._onSongUpdated(song, updatedField))

            self.updated.emit()

        def _onSongUpdated(self, song: Song, updatedField: str) -> None:
            if updatedField == "title":
                self._songs.remove(song)
                newPosition = self.__findInsertPosition(song)
                self._songs.insert(newPosition, song)

            self.updated.emit()

        def insertAll(self, songs: list[Song]) -> None:
            super().insertAll(songs)
            if songs is not None:
                for song in songs:
                    song.loved.connect(lambda a0: self.__saveDatabase())
                self.updated.emit()

        def removeAll(self, songs: list[Song]) -> None:
            super().removeAll(songs)
            if songs is not None:
                for song in songs:
                    song.loved.disconnect(lambda a0: self.__saveDatabase())
                self.updated.emit()

        def remove(self, song: Song) -> None:
            super().remove(song)

            with suppress(TypeError):
                song.loved.disconnect(lambda a0: self.__saveDatabase())
            self.updated.emit()

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
