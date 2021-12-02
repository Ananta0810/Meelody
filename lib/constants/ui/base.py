from sys import path

path.append("./lib")
from modules.models.color import Color
from utils.helpers.my_bytes import MyBytes


class Colors:
    PRIMARY = Color(128, 64, 255)
    PRIMARY_DARK = Color(0, 0, 255)
    PRIMARY_LIGHT = Color(160, 160, 255)

    SUCCESS = Color(50, 216, 100)
    SUCCESS_DARK = Color(0, 192, 100)
    DANGER = Color(255, 80, 80)
    DANGER_DARK = Color(255, 0, 0)
    WARNING = Color(255, 170, 28)
    WARNING_DARK = Color(255, 128, 0)

    DISABLED = Color(128, 128, 128)
    WHITE = Color(255, 255, 255)
    BLACK = Color(0, 0, 0)
    TRANSPARENT = Color(255, 255, 255, 0)


class ApplicationImage:
    errorPlaylist = MyBytes.get_bytes_from_file("assets\images\defaults\oops.png")
    defaultSongCover = MyBytes.get_bytes_from_file(
        "assets\images\defaults\song_cover.jpg"
    )
    defaultPlaylistCover = MyBytes.get_bytes_from_file(
        "assets\images\defaults\playlist_cover.jpg"
    )
