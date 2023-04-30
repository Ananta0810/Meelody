import os
import uuid

from modules.helpers import Printers
from modules.helpers.types.Bytes import Bytes
from modules.helpers.types.Decorators import override
from modules.helpers.types import Strings
from modules.models.AudioExtractor import AudioExtractor


class Song:
    __id: str
    __location: str
    __title: str
    __artist: str
    __cover: bytes
    __length: float
    __is_loved: bool
    __sample_rate: float

    def __init__(
        self,
        location: str = None,
        title: str = None,
        artist: str = None,
        cover: bytes = None,
        length: float = 0,
        sample_rate: float = 48000,
        loved: bool = False,
    ):
        self.__location = location
        self.__title = title
        self.__artist = artist
        self.__cover = cover
        self.__length = length
        self.__sample_rate = sample_rate
        self.__is_loved = loved

    @staticmethod
    def from_file(location: str) -> 'Song':
        song = Song(location)
        song.__id = str(uuid.uuid4())
        song.__load_info_from(location)
        return song

    @staticmethod
    def from_json(json: dict) -> 'Song':
        song = Song(
            location=json['location'],
            title=json['title'],
            artist=json['artist'],
            cover=Bytes.encode(json['cover']),
            length=json['length'],
            sample_rate=json['sample_rate'],
            loved=json['is_loved'],
        )
        song.__id = json['id']
        return song

    def clone(self) -> 'Song':
        song = Song(location=self.__location, title=self.__title, artist=self.__artist, cover=self.__cover,
                    length=self.__length, loved=self.__is_loved, )
        song.__id = self.__id
        return song

    def to_dict(self) -> dict:
        return {
            'id': self.__id,
            'location': self.__location,
            'title': self.__title,
            'artist': self.__artist,
            'cover': Bytes.decode(self.__cover),
            'length': self.__length,
            'sample_rate': self.__sample_rate,
            'is_loved': self.__is_loved,
        }

    @override
    def __str__(self):
        return f"Song({self.__title}, {self.__artist}, {self.__length}, {self.__is_loved})"

    @override
    def __eq__(self, other: 'Song') -> bool:
        """
        Check if two songs is the same one.
        """
        return (
            self.__location == other.__location
            and self.__title == other.__title
            and self.__artist == other.__artist
            and self.__cover == other.__cover
            and self.__length == other.__length
            and self.__is_loved == other.__is_loved
            and self.__sample_rate == other.__sample_rate
        )

    def __load_info_from(self, location: str) -> None:
        """
        Load the information of the song when having the audio file
        """
        audio = AudioExtractor.load_from(location)
        self.__title = Strings.get_file_basename(location)
        self.__artist = audio.get_artist()
        self.__cover = audio.get_cover()
        self.__length = audio.get_length()
        self.__sample_rate = audio.get_sample_rate()

    def set_title(self, title: str) -> bool:
        """
        Rename title of the song. In addition, rename the audio file name.
        """
        try:
            newLocation = Strings.rename_file(self.__location, title)
            if os.path.exists(newLocation):
                return False
            os.rename(self.__location, newLocation)
            self.__location = newLocation
            self.__title = title
            return True
        except PermissionError:
            return False

    def set_artist(self, artist: str) -> bool:
        """
        Rename artist of the song. Save the new artist into the audio file.
        """
        change_successfully: bool = AudioExtractor.load_from(self.__location).set_artist(artist)
        if change_successfully:
            self.__artist = artist
        return change_successfully

    def set_cover(self, cover: bytes) -> bool:
        """
        Change cover of the song. Save the new cover into the audio file.
        """
        change_successfully: bool = AudioExtractor.load_from(self.__location).set_cover(cover)
        if change_successfully:
            self.__cover = cover
        else:
            Printers.error("Save cover failed.")
        return change_successfully

    def get_id(self) -> str:
        return self.__id

    def get_title(self) -> str:
        return self.__title

    def get_location(self) -> str:
        return self.__location

    def get_artist(self) -> str:
        return self.__artist

    def get_cover(self) -> bytes:
        return self.__cover

    def get_length(self) -> int:
        return int(self.__length)

    def get_sample_rate(self) -> float:
        return self.__sample_rate

    def is_loved(self) -> bool:
        return self.__is_loved

    def delete(self) -> bool:
        """
        Delete audio file.
        """
        try:
            os.remove(self.__location)
            return True
        except FileNotFoundError:
            return False

    def reverse_love_state(self) -> None:
        """
        Reverse the current love state to the opposite.
        """
        self.__is_loved = not self.__is_loved

    def set_love_state(self, state: bool) -> None:
        """
        Reverse the current love state to the opposite.
        """
        self.__is_loved = state
