import os
from contextlib import suppress

from PyQt5.QtCore import pyqtSignal, pyqtBoundSignal

from app.common.models.playlist import Playlist
from app.common.models.playlists.common_playlist import CommonPlaylist
from app.common.models.song import Song
from app.common.others.translator import translator
from app.utils.base import Lists, Strings
from app.utils.others import Jsons, Files
from app.utils.reflections import SingletonMeta, returnOnFailed


class _Database:

    def __init__(self, path: str) -> None:
        self.__path = path

    def load(self, directory: str, withExtension: str) -> list[Song]:
        if not os.path.exists(directory):
            os.mkdir(directory)

        if os.path.exists(self.__path):
            data: list[dict] = Jsons.readFromFile(self.__path)
            if data is not None:
                return [Song.fromDict(item) for item in data]

        return self.__loadSongsFromFolder(directory, withExtension)

    def __loadSongsFromFolder(self, directory, withExtension):
        files: set = Files.getFrom(directory, withExtension)
        songs = Lists.nonNull([Song.fromFile(file, Strings.getFileBasename(file)) for file in files])
        self.save(songs)
        return songs

    def save(self, songs: list[Song]) -> None:
        Jsons.writeToFile(self.__path, [song.toDict() for song in songs])


class Library(Playlist, metaclass=SingletonMeta):
    class Info(CommonPlaylist.Info, metaclass=SingletonMeta):

        def __init__(self):
            super().__init__(id="Library", name="Library")
            translator.changed.connect(lambda: self.__setName(translator.translate("PLAYLIST_CAROUSEL.LIBRARY")))

        def setName(self, name: str) -> None:
            pass

        def __setName(self, name: str) -> None:
            self._name = name

        def setCover(self, cover: bytes) -> None:
            pass

    class Songs(CommonPlaylist.Songs):
        loaded: pyqtBoundSignal = pyqtSignal()

        def __init__(self):
            super().__init__(None, isSorted=True)
            self._database = _Database("configuration/songs.json")
            self._loadSongs()

            self.updated.connect(lambda: self.__saveDatabase())

        def _loadSongs(self) -> None:
            for song in self._database.load("library", withExtension="mp3"):
                self._insert(song)
                self.__connectToSong(song)

            self.loaded.emit()

        def setSongs(self, songs: list[Song]) -> None:
            pass

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

        def hasSongWithTitle(self, title: str) -> bool:
            return title.strip().lower() in {song.getTitle().lower() for song in self.toList()}

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
            self._database.save(self.toList())

    def __init__(self):
        super().__init__(Library.Info(), Library.Songs())

    def clone(self) -> 'Playlist':
        return self

    def getSongs(self) -> 'Library.Songs':
        return super().getSongs()
