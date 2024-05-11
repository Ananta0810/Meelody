from app.helpers.base import Bytes


class Images:
    ERROR_PLAYLIST: bytes = Bytes.fromFile("app/resource/images/defaults/oops.png")
    TIMER: bytes = Bytes.fromFile("app/resource/images/defaults/timer.png")
    DOWNLOAD: bytes = Bytes.fromFile("app/resource/images/defaults/download.png")
    IMPORT_SONGS: bytes = Bytes.fromFile("app/resource/images/defaults/import-songs.png")
    SUCCESS: bytes = Bytes.fromFile("app/resource/images/defaults/succeed.png")
    EDIT: bytes = Bytes.fromFile("app/resource/images/defaults/edit.png")
    DELETE: bytes = Bytes.fromFile("app/resource/images/defaults/delete.png")
    WARNING: bytes = Bytes.fromFile("app/resource/images/defaults/warning.png")
    DEFAULT_SONG_COVER: bytes = Bytes.fromFile("app/resource/images/defaults/song_cover.jpg")
    DEFAULT_PLAYLIST_COVER: bytes = Bytes.fromFile("app/resource/images/defaults/playlist_cover.jpg")
    FAVOURITES_PLAYLIST_COVER: bytes = Bytes.fromFile("app/resource/images/defaults/playlist_favourite_cover.jpg")
    NULL_IMAGE: bytes = Bytes.fromFile("app/resource/images/defaults/playlist_cover.jpg")
    SYSTEM_MODE: bytes = Bytes.fromFile("app/resource/images/defaults/light-dark-mode.png")
    LIGHT_MODE: bytes = Bytes.fromFile("app/resource/images/defaults/light-mode.png")
    DARK_MODE: bytes = Bytes.fromFile("app/resource/images/defaults/dark-mode.png")
