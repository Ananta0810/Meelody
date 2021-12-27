from os import path, remove, rename

from joblib import Memory
from modules.models.audio import MyAudio

memory = Memory("caches/songs", verbose=0)


@memory.cache
def getInfoFromAudio(fileName: str):
    audio = MyAudio(fileName)
    return [audio.getArtist(), audio.getCover(), audio.getLength()]


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
        return MyAudio(self.location).getSampleRate()

    def loadInfo(self):
        """
        Load the information of the song when having the audio file
        """
        info = getInfoFromAudio(self.location)
        self.artist = info[0]
        self.cover = info[1]
        self.length = info[2]

    def setTitle(self, title: str) -> bool:
        try:
            newLocation = self.location.replace(self.title, title)
            if path.exists(newLocation):
                return False
            rename(self.location, newLocation)
            self.location = newLocation
            self.title = title
            return True
        except PermissionError:
            return False

    def setArtist(self, artist: str) -> bool:
        changeSuccessfully: bool = MyAudio(self.location).setArtist(artist)
        if changeSuccessfully:
            self.artist = artist
        return changeSuccessfully

    def setCover(self, cover: bytes) -> bool:
        changeSuccessfully: bool = MyAudio(self.location).setCover(cover)
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
