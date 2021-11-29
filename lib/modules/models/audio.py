from eyed3 import id3, load, mp3


class MyAudio:
    _data: mp3.Mp3AudioFile

    def __init__(self, file):
        self._data = load(file)

    def getArtist(self) -> str:
        try:
            return self._data.tag.artist
        except:
            return None

    def getLength(self) -> int:
        try:
            return int(self._data.info.time_secs)
        except:
            return 0

    def getCover(self) -> bytes:
        data = None
        try:
            images = self._data.tag.images
            for image in images:
                if image.image_data is None:
                    continue
                data = image.image_data
        except:
            pass
        return data

    def getSampleRate(self) -> int:
        try:
            return self._data.info.sample_freq
        except:
            return 0

    def setArtist(self, artist: str) -> bool:
        try:
            self._data.tag.artist = artist
            self._data.tag.save(version=id3.ID3_V2_3)
            return True
        except FileNotFoundError:
            return False

    def setCover(self, new_cover: bytes) -> None:
        if self._data.tag == None:
            self._data.initTag()

        self.__removeExistingCovers()
        self.__addNewCover(new_cover)

    def __removeExistingCovers(self) -> None:
        images = self._data.tag.images
        [images.remove(image.description) for image in images]

    def __addNewCover(self, new_cover: bytes, description: str = None) -> None:
        self._data.tag.images.set(3, new_cover, description)
        self._data.tag.save(version=id3.ID3_V2_3)
