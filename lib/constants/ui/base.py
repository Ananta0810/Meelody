from sys import path
from typing import Final

from .metaclass import MetaConst

path.append("./lib")
from utils.helpers.my_bytes import MyBytes


class ApplicationImage(metaclass=MetaConst):
    __slots__ = ()
    errorPlaylist: Final = MyBytes.getBytesFromFile(
        "assets\images\defaults\oops.png"
    )
    defaultSongCover: Final = MyBytes.getBytesFromFile(
        "assets\images\defaults\song_cover.jpg"
    )
    defaultPlaylistCover: Final = MyBytes.getBytesFromFile(
        "assets\images\defaults\playlist_cover.jpg"
    )
    favouritesCover: Final = MyBytes.getBytesFromFile(
        "assets\images\defaults\playlist_favourite_cover.jpg"
    )
