from app.helpers.base import Bytes


class Images:
    timer: bytes = Bytes.fromFile("resource/images/defaults/timer.png")
    download: bytes = Bytes.fromFile("resource/images/defaults/download.png")
    importSongs: bytes = Bytes.fromFile("resource/images/defaults/import-songs.png")
    success: bytes = Bytes.fromFile("resource/images/defaults/succeed.png")
    edit: bytes = Bytes.fromFile("resource/images/defaults/edit.png")
    warning: bytes = Bytes.fromFile("resource/images/defaults/warning.png")
    defaultSongCover: bytes = Bytes.fromFile("resource/images/defaults/song_cover.jpg")
    defaultPlaylistCover: bytes = Bytes.fromFile("resource/images/defaults/playlist_cover.jpg")
    systemMode: bytes = Bytes.fromFile("resource/images/defaults/light-dark-mode.png")
    lightMode: bytes = Bytes.fromFile("resource/images/defaults/light-mode.png")
    darkMode: bytes = Bytes.fromFile("resource/images/defaults/dark-mode.png")
