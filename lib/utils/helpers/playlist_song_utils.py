from logging import getLogger

from modules.entities.song import Song
from modules.models.playlist_songs import PlaylistSongs

from .my_file import MyFile


def getPlaylistFromDir(dir: str, withExtension: str) -> PlaylistSongs:
    getLogger().setLevel("ERROR")
    playlist = PlaylistSongs()
    files: set = MyFile.getFilesFrom(dir, withExtension)
    for file in files:
        song = Song(location=file, title=MyFile.getFileBasename(file))
        song.loadInfo()
        playlist.insert(song)
    return playlist
