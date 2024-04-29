import os
import uuid
from enum import Enum
from typing import Optional

from PyQt5.QtCore import QObject, pyqtSignal
from eyed3 import load, mp3

from app.helpers.base import Strings


class Song(QObject):
    class Order(Enum):
        TITLE = 'title',
        ARTIST = 'artist',
        LENGTH = 'length'

    __id: str
    __location: str
    __title: str
    __artist: str
    __cover: bytes
    __length: float
    __isLoved: bool
    __sampleRate: float

    loved = pyqtSignal(bool)

    def __init__(self, location: str = None, title: str = None, artist: str = None, cover: bytes = None, length: float = 0, sampleRate: float = 48000,
                 loved: bool = False):
        super().__init__()
        self.__id = str(uuid.uuid4())
        self.__location = location
        self.__title = title
        self.__artist = artist
        self.__cover = cover
        self.__length = length
        self.__sampleRate = sampleRate
        self.__isLoved = loved

    @staticmethod
    def fromFile(location: str) -> 'Song':
        song = SongReader(location)

        return Song(
            location,
            title=Strings.getFileBasename(location),
            artist=song.getArtist(),
            cover=song.getCover(),
            length=song.getLength(),
            sampleRate=song.getSampleRate()
        )

    def clone(self) -> 'Song':
        song = Song(location=self.__location, title=self.__title, artist=self.__artist, cover=self.__cover,
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
        return (
            self.__location == other.__location
            and self.__title == other.__title
            and self.__artist == other.__artist
            and self.__cover == other.__cover
            and self.__length == other.__length
            and self.__isLoved == other.__isLoved
            and self.__sampleRate == other.__sampleRate
        )

    def __str__(self):
        return f"Song({self.__title}, {self.__artist}, {self.__length}, {self.__isLoved})"

    def changeTitle(self, title: str) -> bool:
        """
        Rename title of the song. In addition, rename the audio file name.
        """
        try:
            # newLocation = Strings.rename_file(self.__location, title)
            # if os.path.exists(newLocation):
            #     return False
            # os.rename(self.__location, newLocation)
            # self.__location = newLocation
            # self.__title = title
            return True
        except PermissionError:
            return False

    def changeArtist(self, artist: str) -> bool:
        """
        Rename artist of the song. Save the new artist into the audio file.
        """
        # change_successfully: bool = AudioExtractor.load_from(self.__location).set_artist(artist)
        # if change_successfully:
        #     self.__artist = artist
        # return change_successfully

    def changeCover(self, cover: bytes) -> bool:
        """
        Change cover of the song. Save the new cover into the audio file.
        """
        # change_successfully: bool = AudioExtractor.load_from(self.__location).set_cover(cover)
        # if change_successfully:
        #     self.__cover = cover
        # else:
        #     Printers.error("Save cover failed.")
        # return change_successfully

    def setCover(self, cover: bytes) -> None:
        """
        Change cover of the song. Save the new cover into the audio file.
        """
        self.__cover = cover

    def getId(self) -> str:
        return self.__id

    def getTitle(self) -> str:
        return self.__title

    def getLocation(self) -> str:
        return self.__location

    def getArtist(self) -> str:
        return self.__artist

    def getCover(self) -> bytes | None:
        return self.__cover

    def getLength(self) -> int:
        return int(self.__length)

    def getSampleRate(self) -> float:
        return self.__sampleRate

    def isLoved(self) -> bool:
        return self.__isLoved

    def delete(self) -> bool:
        """
        Delete audio file.
        """
        try:
            os.remove(self.__location)
            return True
        except FileNotFoundError:
            return False

    def changeLoveState(self, state: bool = None) -> None:
        """
        Reverse the current love state to the opposite.
        """
        if state is None:
            self.__isLoved = not self.__isLoved
        else:
            self.__isLoved = state
        self.loved.emit(self.__isLoved)


class SongReader:
    __data: mp3.Mp3AudioFile

    def __init__(self, file: str):
        self.__data = load(file)

    def getArtist(self) -> str:
        try:
            return self.__data.tag.artist
        except AttributeError:
            return ''

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
