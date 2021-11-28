from sys import path

path.append(".")
from lib.utils.helpers.my_bytes import MyBytes


class ApplicationImage:
    errorPlaylist = MyBytes.get_bytes_from_file("assets\images\defaults\oops.png")
    defaultSongCover = MyBytes.get_bytes_from_file(
        "assets\images\defaults\song_cover.jpg"
    )
    defaultPlaylistCover = MyBytes.get_bytes_from_file(
        "assets\images\defaults\playlist_cover.jpg"
    )
