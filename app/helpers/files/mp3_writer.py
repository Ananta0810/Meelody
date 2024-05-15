from eyed3 import load, mp3, id3

from app.common.exceptions import ResourceException


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
