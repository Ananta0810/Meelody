from os import remove

from modules.models.audio import MyAudio

from sys import path

path.append(".lib/modules/")


class Song:
    location: str
    title: str
    artist: str
    cover: bytes
    length: float
    loved: bool

    def __init__(
        self,
        id: int = 0,
        location: str = None,
        title: str = None,
        artist: str = None,
        cover: bytes = None,
        length: float = 0,
        loved: bool = False,
    ):
        self.id = id
        self.location = location
        self.title = title
        self.artist = artist
        self.cover = cover
        self.length = length
        self.loved = loved
        self._audio = MyAudio(self.location)

    def __str__(self):
        return f"song({self.title}, {self.artist}, {self.length}, {self.loved})"

    def equals(self, other):
        return (
            self.location == other.location
            and self.title == other.title
            and self.artist == other.artist
            and self.cover == other.cover
            and self.length == other.length
            and self.loved == other.loved
        )

    def getSampleRate(self) -> int:
        return self._audio.getSampleRate()

    def loadInfo(self):
        """
        Load the information of the song when having the audio file
        """
        self.artist = self._audio.getArtist()
        self.cover = self._audio.getCover()
        self.length = self._audio.getLength()

    def changeTitle(self, title: str) -> bool:
        pass

    def changeArtist(self, artist: str) -> bool:
        changeSuccessfully: bool = self._audio.setArtist(artist)
        if changeSuccessfully:
            self.artist = artist
        return changeSuccessfully

    def changeCover(self, cover: bytes) -> bool:
        changeSuccessfully: bool = self._audio.setCover(cover)
        if changeSuccessfully:
            self.cover = cover
        return changeSuccessfully

    def delete(self) -> bool:
        try:
            remove(self.location)
            return True
        except FileNotFoundError:
            return False

    def reverseLoveState(self):
        self.loved = not self.loved
