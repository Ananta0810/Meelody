from sys import path

from .my_file import MyFile

path.append("./lib")
from logging import getLogger

from entities.song import Song
from modules.models.playlist_songs import PlaylistSongs


def getPlaylistFromDir(dir, withExtension):
    getLogger().setLevel("ERROR")
    playlist = PlaylistSongs()
    files = MyFile.getFilesFrom(dir, withExtension)
    for file in files:
        song = Song(location=file, title=MyFile.getFileBasename(file))
        song.loadInfo()
        playlist.insert(song)
    return playlist
