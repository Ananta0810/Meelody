from sys import path

path.append("./lib")
from random import shuffle

from modules.entities.song import Song
from utils.helpers.my_list import MyList


class PlaylistSongs:
    _songs: list[Song]
    _backupSongs: list[Song]
    _sortMethod: str
    _isSorted: bool

    def __init__(self, sortMethod: str = "title"):
        self._songs = []
        self._backupSongs = []
        self._sortMethod = sortMethod
        self._isSorted = True

    def __str__(self):
        string = ""
        for index, song in enumerate(self._songs):
            string += f"{index}. {str(song)}\n"
        return string

    def getSongs(self) -> list[Song]:
        return self._songs

    def isSorted(self):
        return self._isSorted

    def hasSong(self) -> bool:
        return len(self._songs) > 0

    def moveSong(self, index: int, newIndex: int):
        MyList.moveElement(self._songs, index, newIndex)

    def size(self) -> int:
        """
        return the number of songs in the list
        """
        return len(self._songs)

    def setSortMethod(self, state: str):
        self._sortMethod = state

    def getSong(self, index: int):
        """
        Get the song at the given index
        """
        if len(self._songs) == 0:
            return None
        return self._songs[index]

    def insert(self, song: Song) -> int:
        """
        Add song to the list of songs. If added SUCCESSfully, it will return the position of the song in the playlist
        """
        if len(self._songs) != 0 and self._isSorted and self._sortMethod == "title":
            position: int = MyList.binaryInsertSearchByTitle(self._songs, song.title)
            self._songs.insert(position, song)
            return position
        self._songs.append(song)
        return len(self._songs) - 1

    def shuffle(self):
        self._backupSongs = self._songs.copy()
        self._isSorted = False
        shuffle(self._songs)

    def unshuffle(self):
        self._songs = self._backupSongs.copy()
        self._isSorted = True
        self._backupSongs.clear()

    def findSongByTitle(self, title):
        if self._isSorted:
            return MyList.binarySearchByTitle(self._songs, title)
        return MyList.linearSearchByTitle(self._songs, title)

    def findSongInsertPosition(self, title):
        return MyList.binaryInsertSearchByTitle(self._songs, title)

    def find(self, song: Song) -> int:
        """
        Find the index Of song in the list
        """
        if not self._isSorted:
            return MyList.linearSearch(self._songs, song)

        if self._sortMethod == "title":
            return MyList.binarySearchByTitle(self._songs, song.title)

        return MyList.binarySearchByArtist(self._songs, song.artist)
