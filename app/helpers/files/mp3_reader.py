from typing import Optional

from eyed3 import load, mp3


class SongReader:

    def __init__(self, file: str):
        self.__data: mp3.Mp3AudioFile = load(file)

    def isValid(self) -> bool:
        try:
            return int(self.__data.info.time_secs) > 0
        except AttributeError:
            return False

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
