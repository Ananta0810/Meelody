from modules.models.PlaylistInformation import PlaylistInformation
from modules.models.PlaylistSongs import PlaylistSongs


class Playlist:
    __info: PlaylistInformation
    __songs: PlaylistSongs

    def __init__(self, info: PlaylistInformation, songs: PlaylistSongs):
        self.__info = info
        self.__songs = songs

    @staticmethod
    def create(name: str, cover: bytes = None, songs: PlaylistSongs = None) -> 'Playlist':
        return Playlist(PlaylistInformation(name, cover), songs or PlaylistSongs.create_empty())

    def get_info(self) -> PlaylistInformation:
        return self.__info

    def get_songs(self) -> PlaylistSongs:
        return self.__songs

    def size(self) -> int:
        """
        :return: total songs of this playlist. 0 if playlist has no songs.
        :rtype: int
        """
        return 0 if self.__songs is None else self.__songs.size()

    def equals(self, other):
        """
        Check if two playlists are the same one
        """
        return self.__info == other.__info
