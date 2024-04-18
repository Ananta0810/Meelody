from modules.helpers.Database import Database
from modules.models.Playlist import Playlist
from modules.models.PlaylistSongs import PlaylistSongs
from modules.screens.windows.MainWindowControl import MainWindowControl
from modules.statics.view import Material
from modules.statics.view.Material import Images


class Application:
    def __init__(self):
        Material.Cursors.init_value()
        Material.Icons.init_value()

        self.window = MainWindowControl()
        self.window.apply_light_mode()
        self.load_playlist()

    def run(self) -> None:
        self.window.show()
        self.window.apply_light_mode()

    def receiveMessage(self, msg: str) -> None:
        self.window.receiveMessage(msg)

    def load_playlist(self):
        """
            - pip install PyQt5
            - pip install pygame
            - pip install eyed3
            - pip install yt-dlp==2023.2.17
            - pip install Pillow==9.0.0
            - pip install pillow
        """

        Database().settings.set_path("configuration/settings.json")
        Database().songs.set_path("configuration/library.json")
        Database().playlists.set_path("configuration/playlists.json")
        Database().covers.set_path("configuration/covers.json")

        songs: PlaylistSongs = Database().songs.load("library", with_extension="mp3")
        self.window.set_appsettings(Database().settings.load())
        self.window.load_library(Playlist.create(name="Library", songs=songs, cover=Images.DEFAULT_PLAYLIST_COVER))
        self.window.load_playlists(Database().playlists.load(songs.get_songs()))
