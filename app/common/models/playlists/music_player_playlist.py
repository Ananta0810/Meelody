from typing import Optional

from app.common.models.playlist import Playlist
from app.common.models.song import Song
from app.helpers.base import Lists, Numbers
from .common_playlist import CommonPlaylist


class MusicPlayerPlaylistSongs(Playlist.Songs):
    """
    This playlist songs will be used inside music player.
    """

    def __init__(self, playlist: Playlist.Songs):
        super().__init__()
        self.__playlist: Playlist.Songs = playlist
        self.__shufflePlaylist: Optional[Playlist.Songs] = None

    def setShuffle(self, shuffle: bool) -> None:
        if shuffle:
            songs = Lists.shuffle(self.__playlist.toList())
            self.__shufflePlaylist = CommonPlaylist.Songs(songs, isSorted=False)
            self.__playlist.updated.connect(lambda: self.__updateShufflePlaylistSongs())
        else:
            try:
                self.__playlist.updated.disconnect(lambda: self.__updateShufflePlaylistSongs())
            except TypeError:
                pass
            self.__shufflePlaylist = None

    def __updateShufflePlaylistSongs(self):
        if self.__shufflePlaylist is None:
            return

        addedSongs = Lists.itemsInLeftOnly(self.__playlist.toList(), self.__shufflePlaylist.toList())
        removedSongs = set(Lists.itemsInLeftOnly(self.__playlist.toList(), self.__shufflePlaylist.toList()))

        songs = [song for song in self.__shufflePlaylist.toList() if song not in removedSongs]

        for song in addedSongs:
            randomIndex = Numbers.randomInteger(0, len(self.__shufflePlaylist.toList()) - 1)
            songs.insert(randomIndex, song)

        self.__shufflePlaylist.setSongs(songs)

    def __getPlaylist(self) -> Playlist.Songs:
        return self.__shufflePlaylist or self.__playlist

    def clone(self) -> 'Playlist.Songs':
        return self

    def setSongs(self, songs: list[Song]) -> None:
        pass

    def toList(self) -> list[Song]:
        return self.__getPlaylist().toList()

    def hasAnySong(self) -> bool:
        return self.__playlist.hasAnySong()

    def hasSong(self, song: Song) -> bool:
        return self.__playlist.hasSong(song)

    def size(self) -> int:
        return self.__playlist.size()

    def indexOf(self, song: Song) -> int:
        return self.__getPlaylist().indexOf(song)

    def getSongAt(self, index: int) -> Song:
        return self.__getPlaylist().getSongAt(index)

    def insert(self, song: Song) -> None:
        pass

    def insertAll(self, songs: list[Song]) -> None:
        pass

    def remove(self, song: Song) -> None:
        pass

    def removeAll(self, songs: list[Song]) -> None:
        pass

    def moveSong(self, fromIndex: int, toIndex: int) -> None:
        pass
