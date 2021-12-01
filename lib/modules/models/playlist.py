from sys import path

from .playlist_songs import PlaylistSongs

path.append(".lib/modules/")
from modules.entities.playlist_info import PlaylistInfo


class Playlist:
    info: PlaylistInfo
    songs: PlaylistSongs

    def __init__(self, info: PlaylistInfo, songs: PlaylistSongs):
        self.info = info
        self.songs = songs

    def equals(self, other):
        """
        Check if two playlists are the same one
        """
        return self.info.equals(other.info)
