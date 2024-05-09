import os
import uuid
from typing import Optional, Callable

from PyQt5.QtCore import QObject, pyqtSignal, QThread
from eyed3 import load, mp3, id3

from app.common.exceptions import ResourceException
from app.helpers.base import Strings
from app.helpers.others import Logger


class Song(QObject):
    __id: str
    __location: str
    __title: str
    __artist: str
    __cover: bytes
    __length: float
    __isLoved: bool
    __sampleRate: float

    loved = pyqtSignal(bool)
    coverChanged = pyqtSignal(bytes)
    updated = pyqtSignal(str)
    deleted = pyqtSignal()

    def __init__(self, location: str = None, title: str = None, artist: str = None, cover: bytes = None, length: float = 0, sampleRate: float = 48000,
                 loved: bool = False):
        super().__init__()
        self.__id = str(uuid.uuid4())
        self.__location = location
        self.__title = title
        self.__artist = artist
        self.__length = length
        self.__sampleRate = sampleRate
        self.__isLoved = loved
        if cover is not None:
            self.__cover = cover

    @staticmethod
    def fromFile(location: str, title: str = None) -> Optional['Song']:
        """
        Load a song from explorer. Return None if song is load failed.
        """
        try:
            data = SongReader(location)

            song = Song(location, title=data.getTitle(), artist=data.getArtist(), length=data.getLength(), sampleRate=data.getSampleRate())

            if song.getTitle() is None:
                if title is not None:
                    song.updateInfo(title, song.getArtist())
                else:
                    raise ResourceException("No title provided.")
            return song
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
            assert hasattr(self, '__cover'), 'Cover is not loaded.'
            return True
        except AssertionError:
            return False

    def loadCover(self) -> None:
        if not self.isCoverLoaded():
            CoverLoaderThread(self.__location, onLoaded=self.__setCover).run()

    def __setCover(self, cover: bytes) -> None:
        self.__cover = cover
        if self.__cover is not None:
            self.coverChanged.emit(self.__cover)

    def updateInfo(self, title: str, artist: str) -> None:
        """
        Rename title and artist of the song.
        throws: ResourceException if update failed
        """
        writer = SongWriter(self.__location)

        if not Strings.equals(self.__title, title):
            writer.writeTitle(title)
            self.__title = title
            self.updated.emit("title")

        if not Strings.equals(self.__artist, artist):
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


class SongReader:

    def __init__(self, file: str):
        self.__data: mp3.Mp3AudioFile = load(file)

    def getTitle(self) -> Optional[str]:
        try:
            return self.__data.tag.title
        except AttributeError:
            return None

    def getArtist(self) -> Optional[str]:
        try:
            return self.__data.tag.artist
        except AttributeError:
            return None

    def getLength(self) -> int:
        try:
            return int(self.__data.info.time_secs)
        except AttributeError:
            return 0

    def getCover(self) -> Optional[bytes]:
        try:
            images = self.__data.tag.images
            for image in images:
                if image.image_data is None:
                    continue
                return image.image_data
        except AttributeError:
            return None

    def getSampleRate(self) -> int:
        try:
            return self.__data.info.sample_freq
        except AttributeError:
            return 0


class SongWriter:
    __data: mp3.Mp3AudioFile

    def __init__(self, file: str):
        try:
            self.__data = load(file)
        except (FileNotFoundError, IOError):
            raise ResourceException.notFound()

    def writeTitle(self, title: str) -> None:
        try:
            if self.__data.tag is None:
                self.__data.initTag()

            self.__data.tag.title = title
            self.__data.tag.save(version=id3.ID3_V2_3)
        except (FileNotFoundError, IOError):
            raise ResourceException.notFound()
        except PermissionError:
            raise ResourceException.unChangeable()

    def writeArtist(self, artist: str) -> None:
        try:
            if self.__data.tag is None:
                self.__data.initTag()

            self.__data.tag.artist = artist
            self.__data.tag.save(version=id3.ID3_V2_3)
        except (FileNotFoundError, IOError):
            raise ResourceException.notFound()
        except PermissionError:
            raise ResourceException.unChangeable()

    def writeCover(self, cover: bytes) -> None:
        try:
            if self.__data.tag is None:
                self.__data.initTag()

            self.__removeExistingCovers()
            self.__addNewCover(cover)
        except FileNotFoundError:
            raise ResourceException.notFound()
        except (PermissionError, IOError):
            raise ResourceException.unChangeable()

    def __removeExistingCovers(self) -> None:
        images = self.__data.tag.images
        [images.remove(image.description) for image in images]

    def __addNewCover(self, cover: bytes, description: str = "Added by Meelody") -> None:
        self.__data.tag.images.set(3, cover, description)
        self.__data.tag.save(version=id3.ID3_V2_3)


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
