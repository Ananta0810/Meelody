import os
from typing import Optional, Callable

from PyQt5.QtCore import QObject, pyqtSignal, QThread, pyqtBoundSignal

from app.common.exceptions import ResourceException
from app.helpers.files import SongWriter, SongReader
from app.utils.base import Strings
from app.utils.others import Logger


class Song(QObject):
    __id: str
    __location: str
    __title: str
    __artist: str
    __cover: bytes
    __length: float
    __isLoved: bool
    __sampleRate: float

    loved: pyqtBoundSignal = pyqtSignal(bool)
    coverChanged: pyqtBoundSignal = pyqtSignal(bytes)
    updated: pyqtBoundSignal = pyqtSignal(str)
    deleted: pyqtBoundSignal = pyqtSignal()

    def __init__(self, location: str = None, title: str = None, artist: str = None, cover: bytes = None, length: float = 0, sampleRate: float = 48000,
                 loved: bool = False):
        super().__init__()
        self.__id = location
        self.__location = location
        self.__title = title
        self.__artist = artist
        self.__length = length
        self.__sampleRate = sampleRate
        self.__isLoved = loved
        if cover is not None:
            self.__cover = cover

        self.deleted.connect(lambda: self.deleteLater())

    @staticmethod
    def fromFile(location: str, title: str) -> Optional['Song']:
        """
        Load a song from explorer. Return None if song is load failed.
        """
        try:
            data = SongReader(location)

            if not data.isValid():
                raise ResourceException.brokenFile()

            return Song(location,
                        title=data.getTitle() or title,
                        artist=data.getArtist(),
                        length=data.getLength(),
                        sampleRate=data.getSampleRate())
        except ResourceException:
            return None

    @staticmethod
    def fromDict(json: dict) -> 'Song':
        song = Song(
            location=json['location'],
            title=json['title'],
            artist=json['artist'],
            length=json['length'],
            sampleRate=json['sample_rate'],
            loved=json['is_loved'],
        )
        song.__id = json['id']
        return song

    def toDict(self) -> dict:
        return {
            'id': self.__id,
            'location': self.__location,
            'title': self.__title,
            'artist': self.__artist,
            'length': self.__length,
            'sample_rate': self.__sampleRate,
            'is_loved': self.__isLoved,
        }

    def clone(self) -> 'Song':
        song = Song(location=self.__location, title=self.__title, artist=self.__artist, cover=self.getCover(),
                    length=self.__length, loved=self.__isLoved, )
        song.__id = self.__id
        return song

    def __hash__(self) -> int:
        return hash(self.__id)

    def __eq__(self, other: 'Song') -> bool:
        """
        Check if two songs is the same one.
        """
        if other is None:
            return False

        try:
            return self.__id == other.__id
        except AttributeError:
            return False

    def __str__(self):
        return f"Song({self.__title}, {self.__artist}, {self.__length}, {self.__isLoved})"

    def getId(self) -> str:
        return self.__id

    def getTitle(self) -> str:
        return self.__title

    def getLocation(self) -> str:
        return self.__location

    def getArtist(self) -> str:
        return self.__artist

    def getCover(self) -> bytes | None:
        try:
            return self.__cover
        except AttributeError:
            return None

    def getLength(self) -> int:
        return int(self.__length)

    def getSampleRate(self) -> float:
        return self.__sampleRate

    def isLoved(self) -> bool:
        return self.__isLoved

    def isCoverLoaded(self) -> bool:
        try:
            cover = self.__cover
            return True
        except AttributeError:
            return False

    def loadCover(self) -> None:
        if not self.isCoverLoaded():
            CoverLoaderThread(self.__location, onLoaded=self.__setCover).run()

    def __setCover(self, cover: bytes) -> None:
        self.__cover = cover
        if self.__cover is not None:
            self.coverChanged.emit(self.__cover)

    def updateInfo(self, title: str, artist: str, force=False) -> None:
        """
        Rename title and artist of the song.
        throws: ResourceException if update failed
        """
        writer = SongWriter(self.__location)

        if force or not Strings.equals(self.__title, title):
            writer.writeTitle(title)
            self.__title = title
            self.updated.emit("title")

        if force or not Strings.equals(self.__artist, artist):
            writer.writeArtist(artist)
            self.__artist = artist
            self.updated.emit("artist")

    def updateCover(self, cover: bytes) -> None:
        """
        Change cover of the song. Save the new cover into the audio file.
        """
        SongWriter(self.__location).writeCover(cover)
        self.__cover = cover
        self.coverChanged.emit(cover)

    def updateLoveState(self, state: bool = None) -> None:
        """
        Reverse the current love state to the opposite.
        """
        if state is None:
            self.__isLoved = not self.__isLoved
        else:
            if self.__isLoved == state:
                return
            self.__isLoved = state

        self.loved.emit(self.__isLoved)
        self.updated.emit("love")

    def delete(self) -> None:
        """
        Delete audio file.
        """
        try:
            os.remove(self.__location)
            self.deleted.emit()
            Logger.info(f"Remove song at location {self.__location} successfully.")
        except PermissionError:
            raise ResourceException.unChangeable()
        except FileNotFoundError:
            self.deleted.emit()


class CoverLoaderThread(QThread):
    def __init__(self, location: str, onLoaded: Callable[[bytes], None]) -> None:
        super().__init__()
        self.__location = location
        self.__onLoaded = onLoaded

    def run(self) -> None:
        try:
            cover = SongReader(self.__location).getCover()
            self.__onLoaded(cover)
        except:
            pass
