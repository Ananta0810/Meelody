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

        def insert(self, song: Song) -> None:
            song.loved.connect(lambda a0: self.__saveDatabase())
            super().insert(song)

        def insertAll(self, songs: list[Song]) -> None:
            super().insertAll(songs)
            if songs is not None:
                for song in songs:
                    song.loved.connect(lambda a0: self.__saveDatabase())

        def removeAll(self, songs: list[Song]) -> None:
            super().removeAll(songs)
            if songs is not None:
                for song in songs:
                    song.loved.disconnect(lambda a0: self.__saveDatabase())

        def removeSong(self, song: Song) -> None:
            super().removeSong(song)
            song.loved.disconnect(lambda a0: self.__saveDatabase())

        def __saveDatabase(self) -> None:
            from app.common.others import database
            database.songs.save(self.getSongs())
