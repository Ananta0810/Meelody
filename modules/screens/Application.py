from modules.helpers import LibraryHelper
from modules.models.Playlist import Playlist
from modules.models.PlaylistSongs import PlaylistSongs
from modules.screens.windows.MainWindowControl import MainWindowControl
from modules.statics.view import Material


class Application:
    def __init__(self):
        Material.Cursors.init_value()
        Material.Icons.init_value()

        self.window = MainWindowControl()
        self.window.apply_light_mode()
        self.load_playlist()

    def run(self) -> None:
        self.window.show()

    def load_playlist(self):
        songs: PlaylistSongs = LibraryHelper.load_songs_from_dir("library", with_extension="mp3")
        self.window.load_library(Playlist.create(name="Library", songs=songs))
        self.window.load_playlists(LibraryHelper.load_playlists())
