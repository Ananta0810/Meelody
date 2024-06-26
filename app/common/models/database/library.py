import os
from contextlib import suppress

from PyQt5.QtCore import pyqtSignal, pyqtBoundSignal, QFileSystemWatcher

from app.common.models.playlist import Playlist
from app.common.models.playlists.common_playlist import CommonPlaylist
from app.common.models.song import Song
from app.common.others.data_location import DataLocation
from app.common.others.translator import Translator
from app.components.asyncs import Debounce
from app.utils.base import Lists, Strings
from app.utils.others import Jsons, Files, Logger
from app.utils.reflections import SingletonMeta, returnOnFailed, SingletonQObjectMeta


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
    class Info(CommonPlaylist.Info, metaclass=SingletonQObjectMeta):

        def __init__(self):
            translator = Translator()
            super().__init__(id="Library", name=translator.translate("PLAYLIST_CAROUSEL.LIBRARY"))
            translator.changed.connect(lambda: self.__setName(translator.translate("PLAYLIST_CAROUSEL.LIBRARY")))

        def setName(self, name: str) -> None:
            pass

        def __setName(self, name: str) -> None:
            self._name = name

        def setCover(self, cover: bytes) -> None:
            pass

    class Songs(CommonPlaylist.Songs):
        loaded: pyqtBoundSignal = pyqtSignal()
        moved: pyqtBoundSignal = pyqtSignal(int, int)

        def __init__(self):
            super().__init__(None, isSorted=True)
            self._path = DataLocation().library
            self._database = _Database(f"{DataLocation().configuration}/songs.json")
            self._loadSongs()

            self._watcher = QFileSystemWatcher(self)
            self._watcherDebounce = Debounce(lambda: self.__insertFailedImportSongs(), self, delay=200)
            self.updated.connect(lambda: self.__saveDatabase())

        def watchMissingSongs(self):
            self._watcher.addPath(self._path)
            self._watcherDebounce.call()
            self._watcher.directoryChanged.connect(lambda paths: self._watcherDebounce.call())

        def _loadSongs(self) -> None:
            for song in self._database.load(self._path, withExtension="mp3"):
                self._insert(song)
                self.__connectToSong(song)

            self.loaded.emit()

        def setSongs(self, songs: list[Song]) -> None:
            pass

        def __insertFailedImportSongs(self) -> None:
            """
                Sometimes our application is error while inserting songs, which make some songs failed to import
                to database even when it is imported successfully. Therefore, we will watch for those situation.
            """
            files = Files.getFrom(self._path, withExtension="mp3")

            newFiles = Lists.itemsInLeftOnly(files, [song.getLocation() for song in self.toList()])

            validFiles = [file for file in newFiles if Strings.isRandomId(Strings.getFileBasename(file))]
            songs = Lists.nonNull([Song.fromFile(file, Strings.getFileBasename(file)) for file in validFiles])
            newSongs = [song for song in songs if not self.hasSongWithTitle(song.getTitle())]

            if len(newSongs) > 0:
                self.insertAll(newSongs)
                Logger.info(f"Import missing songs successfully: {[song.getTitle() for song in newSongs]}")

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
                oldSongs = [song for song in self._songs]
                super().remove(song)
                super().insert(song)
                newSongs = [song for song in self._songs]

                oldPosition, newPosition = Lists.findMoved(oldSongs, newSongs)
                if oldPosition >= 0 and newPosition >= 0:
                    self.moved.emit(oldPosition, newPosition)

            self.updated.emit()

        def __disconnectToSong(self, song: Song) -> None:
            with suppress(TypeError):
                song.updated.disconnect(lambda updatedField: self._onSongUpdated(song, updatedField))
                song.deleted.disconnect(lambda: self.remove(song))

        def hasSongWithTitle(self, title: str) -> bool:
            return Lists.binarySearch(self._songs, title, comparator=lambda t_, song: Strings.compare(t_, song.getTitle())) >= 0

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
