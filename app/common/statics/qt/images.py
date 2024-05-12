from app.helpers.base import Bytes


class Images:
    errorPlaylist: bytes = Bytes.fromFile("app/resource/images/defaults/oops.png")
    timer: bytes = Bytes.fromFile("app/resource/images/defaults/timer.png")
    download: bytes = Bytes.fromFile("app/resource/images/defaults/download.png")
    importSongs: bytes = Bytes.fromFile("app/resource/images/defaults/import-songs.png")
    success: bytes = Bytes.fromFile("app/resource/images/defaults/succeed.png")
    edit: bytes = Bytes.fromFile("app/resource/images/defaults/edit.png")
    delete: bytes = Bytes.fromFile("app/resource/images/defaults/delete.png")
    warning: bytes = Bytes.fromFile("app/resource/images/defaults/warning.png")
    defaultSongCover: bytes = Bytes.fromFile("app/resource/images/defaults/song_cover.jpg")
    defaultPlaylistCover: bytes = Bytes.fromFile("app/resource/images/defaults/playlist_cover.jpg")
    favouritesPlaylistCover: bytes = Bytes.fromFile("app/resource/images/defaults/playlist_favourite_cover.jpg")
    nullImage: bytes = Bytes.fromFile("app/resource/images/defaults/playlist_cover.jpg")
    systemMode: bytes = Bytes.fromFile("app/resource/images/defaults/light-dark-mode.png")
    lightMode: bytes = Bytes.fromFile("app/resource/images/defaults/light-mode.png")
    darkMode: bytes = Bytes.fromFile("app/resource/images/defaults/dark-mode.png")
