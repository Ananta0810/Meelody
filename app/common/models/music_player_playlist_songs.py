from app.helpers.base import Lists, Numbers
from .common_playlist import CommonPlaylist
from .playlist import Playlist
from .song import Song


class MusicPlayerPlaylistSongs(Playlist.Songs):
    """
    This playlist songs will be used inside music player.
    """

    def __init__(self, playlist: Playlist.Songs):
        super().__init__()
        self.__playlist = playlist
        self.__shufflePlaylist = None

    def setShuffle(self, shuffle: bool) -> None:
        if shuffle:
            songs = Lists.shuffle(self.__playlist.getSongs())
            self.__shufflePlaylist = CommonPlaylist.Songs(songs, isSorted=False)
            self.__playlist.updated.connect(lambda: self.__updateShufflePlaylistSongs())
        else:
            try:
                self.__playlist.updated.disconnect(lambda: self.__updateShufflePlaylistSongs())
            except TypeError:
                pass
            self.__shufflePlaylist = None

    def __updateShufflePlaylistSongs(self):
        addedSongs = Lists.itemsInLeftOnly(self.__playlist.getSongs(), self.__shufflePlaylist.getSongs())
        removedSongs = set(Lists.itemsInLeftOnly(self.__playlist.getSongs(), self.__shufflePlaylist.getSongs()))

        songs = [song for song in self.__shufflePlaylist.getSongs() if song not in removedSongs]

        for song in addedSongs:
            randomIndex = Numbers.randomInteger(0, len(self.__shufflePlaylist.getSongs()) - 1)
            songs.insert(randomIndex, song)

        self.__shufflePlaylist.setSongs(songs)

    def __getPlaylist(self) -> Playlist.Songs:
        return self.__shufflePlaylist or self.__playlist

    def clone(self) -> 'Playlist.Songs':
        return self.__playlist.clone()

    def setSongs(self, songs: list[Song]) -> None:
        self.__playlist.setSongs(songs)

    def getSongs(self) -> list[Song]:
        return self.__getPlaylist().getSongs()

    def hasAnySong(self) -> bool:
        return self.__playlist.hasAnySong()

    def hasSong(self, song: Song) -> bool:
        return self.__playlist.hasSong(song)

    def moveSong(self, fromIndex: int, toIndex: int) -> None:
        pass

    def size(self) -> int:
        return self.__playlist.size()

    def indexOf(self, song: Song) -> int:
        return self.__getPlaylist().indexOf(song)

    def getSongAt(self, index: int) -> Song:
        return self.__getPlaylist().getSongAt(index)

    def getSongIndexWithId(self, songId: str) -> int:
        return self.__playlist.getSongIndexWithId(songId)

    def insert(self, song: Song) -> None:
        self.__playlist.insert(song)

    def insertAll(self, songs: list[Song]):
        return self.__playlist.insertAll(songs)

    def remove(self, song: Song) -> None:
        self.__playlist.remove(song)

    def removeAll(self, songs: list[Song]) -> None:
        self.__playlist.removeAll(songs)
