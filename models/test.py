import os
from sys import path

path.append(".")

from entities.song import Song

path.append(".")
import pygame
from utils.my_file import MyFile

from models.mixer import Mixer
from models.playlist_songs import PlaylistSongs

songs = PlaylistSongs()
files = MyFile.getFilesFrom("Library", withExtension="mp3")
for file in files:
    song = Song(
        id=0, location=file, title=None, artist=None, cover=None, length=0, loved=False
    )
    song.title = MyFile.getFileBasename(file)
    song.loadInfo()
    songs.insert(song)
print(songs)
pygame.mixer.init()
pygame.mixer.music.load(open(songs.getSong(7).location, "rb"))
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    pass
