from typing import Union

from eyed3 import id3, load, mp3

from modules.helpers import Printers


class AudioExtractor:
    __data: mp3.Mp3AudioFile

    def __init__(self, file: str):
        self.__data = load(file)

    @staticmethod
    def load_from(file: str) -> 'AudioExtractor':
        return AudioExtractor(file)

    def get_artist(self) -> str:
        try:
            return self.__data.tag.artist
        except AttributeError:
            return ''

    def get_length(self) -> int:
        try:
            return int(self.__data.info.time_secs)
        except AttributeError:
            return 0

    def get_cover(self) -> Union[bytes, None]:
        try:
            images = self.__data.tag.images
            for image in images:
                if image.image_data is None:
                    continue
                return image.image_data
        except AttributeError:
            return None

    def get_sample_rate(self) -> int:
        try:
            return self.__data.info.sample_freq
        except AttributeError:
            return 0

    def set_artist(self, artist: str) -> bool:
        try:
            self.__data.tag.artist = artist
            self.__data.tag.save(version=id3.ID3_V2_3)
            return True
        except (FileNotFoundError, PermissionError):
            return False

    def set_cover(self, new_cover: bytes) -> bool:
        if self.__data.tag is None:
            self.__data.initTag()
        try:
            self.__remove_existing_covers()
            self.__add_new_cover(new_cover)
            return True
        except (FileNotFoundError, PermissionError) as e:
            Printers.error(e)
            return False

    def __remove_existing_covers(self) -> None:
        images = self.__data.tag.images
        [images.remove(image.description) for image in images]

    def __add_new_cover(self, new_cover: bytes, description: str = "Added by Meelody") -> None:
        self.__data.tag.images.set(3, new_cover, description)
        self.__data.tag.save(version=id3.ID3_V2_3)
