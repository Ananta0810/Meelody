import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.common_types.my_bytes import MyBytes


class ApplicationImage:
    # errorPlaylist = MyBytes.get_bytes_from_file("src/oops.png")
    defaultSongCover = MyBytes.get_bytes_from_file("src/covers-default/song.jpg")
    defaultPlaylistCover = MyBytes.get_bytes_from_file(
        "src/covers-default/playlist.jpg"
    )
