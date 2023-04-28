from modules.helpers import DataSaver
from modules.models.AppSettings import AppSettings
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

    def load_playlist(self):
        """
        TODO:
            - Add alert when delete song and playlist.
            - Add alert when song already existed.
            - Add alert when update something failed.
            - Add alert when download youtube music failed.
            - Add progress bar to show which one is downloading.
            - Add sidebar.
            - Fix first time hear song.
            - Fix edit when shuffling is wrong.
            - Update UI for inputs.
            - Add button to edit favourite playlist cover.
            - Change icon for minimize button.
            - Only show icon on tray when hidden.
            - Add play buttons on taskbar.
            - Refactor structure.
        """
        songs: PlaylistSongs = DataSaver.load_songs_from_dir("library", with_extension="mp3")
        settings: AppSettings = DataSaver.load_settings()
        self.window.set_appsettings(settings)
        self.window.load_library(Playlist.create(name="Library", songs=songs, cover=Images.DEFAULT_PLAYLIST_COVER))
        self.window.load_playlists(DataSaver.load_playlists(songs.get_songs()))
