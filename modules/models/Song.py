import os

from modules.helpers.types.Decorators import override
from modules.models.AudioExtractor import AudioExtractor


class Song:
    __location: str
    __title: str
    __artist: str
    __cover: bytes
    __length: float
    __is_loved: bool

    def __init__(
        self,
        location: str = None,
        title: str = None,
        artist: str = None,
        cover: bytes = None,
        length: float = 0,
        loved: bool = False,
    ):
        self.__location = location
        self.__title = title
        self.__artist = artist
        self.__cover = cover
        self.__length = length
        self.__is_loved = loved

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
        )

    def get_sample_rate(self) -> int:
        """
        Get sample rate of song for fixing some bugs of pygame audio
        """
        return AudioExtractor.load_from(self.__location).get_sample_rate()

    def load_info(self) -> None:
        """
        Load the information of the song when having the audio file
        """
        (artist, cover, length) = self.__get_info_from_audio(self.__location)
        self.__artist = artist
        self.__cover = cover
        self.__length = length

    def set_title(self, title: str) -> bool:
        """
        Rename title of the song. In addition, rename the audio file name.
        """
        try:
            newLocation = self.__location.replace(self.__title, title)
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
        return change_successfully

    def delete(self) -> bool:
        """
        Delete audio file.
        """
        try:
            os.remove(self.__location)
            return True
        except FileNotFoundError:
            return False

    def reverse_love_state(self):
        """
        Reverse the current love state to the opposite.
        """
        self.__is_loved = not self.__is_loved

    @staticmethod
    def __get_info_from_audio(file_name: str) -> tuple:
        """
        Extract information of song from its file.
        """
        audio = AudioExtractor.load_from(file_name)
        return audio.getArtist(), audio.getCover(), audio.getLength()