import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.common_types.my_bytes import MyBytes


class ApplicationImage:
    error_playlist = MyBytes.get_bytes_from_file("images/oops.png")
    default_song_cover = MyBytes.get_bytes_from_file("images/covers-default/song.jpg")
    default_playlist_cover = MyBytes.get_bytes_from_file(
        "images/covers-default/playlist.jpg"
    )
