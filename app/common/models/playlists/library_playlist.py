from app.common.models.playlist import Playlist
from app.common.models.song import Song
from .common_playlist import CommonPlaylist


class Library(Playlist):
    class Info(CommonPlaylist.Info):
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
                self.__songs.remove(song)
                newPosition = self.__findInsertPosition(song)
                self.__songs.insert(newPosition, song)

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

        def removeSong(self, song: Song) -> None:
            super().removeSong(song)

            song.loved.disconnect(lambda a0: self.__saveDatabase())
            self.updated.emit()

        def moveSong(self, fromIndex: int, toIndex: int) -> None:
            super().moveSong(fromIndex, toIndex)
            self.updated.emit()

        def __saveDatabase(self) -> None:
            from app.common.others import database
            database.songs.save(self.getSongs())
