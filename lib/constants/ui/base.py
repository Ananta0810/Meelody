from sys import path
from typing import Final

from .metaclass import MetaConst

path.append("./lib")
from utils.helpers.my_bytes import MyBytes


class ApplicationImage(metaclass=MetaConst):
    __slots__ = ()
    errorPlaylist: Final = MyBytes.get_bytes_from_file(
        "assets\images\defaults\oops.png"
    )
    defaultSongCover: Final = MyBytes.get_bytes_from_file(
        "assets\images\defaults\song_cover.jpg"
    )
    defaultPlaylistCover: Final = MyBytes.get_bytes_from_file(
        "assets\images\defaults\playlist_cover.jpg"
    )
