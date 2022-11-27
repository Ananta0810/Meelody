from modules.models.PlaylistInformation import PlaylistInformation
from modules.models.PlaylistSongs import PlaylistSongs


class Playlist:
    info: PlaylistInformation
    songs: PlaylistSongs

    def __init__(self, info: PlaylistInformation, songs: PlaylistSongs):
        self.info = info
        self.songs = songs

    def equals(self, other):
        """
        Check if two playlists are the same one
        """
        return self.info == other.info