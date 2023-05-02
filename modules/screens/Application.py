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

    def load_playlist(self):
        """
            - pip install yt-dlp==2023.2.17
            - pip install Pillow==9.0.0
        """

        """
        TODO:
            - Add alert when delete song and playlist. | DONE
            - Add alert when song already existed.
            - Add alert when update something failed. | DONE
            - Add alert when download youtube music failed. | DONE
            - Add progress bar to show which one is downloading. | DONE
            - Add sidebar.
            - Fix first time hear song. | DONE
            - Fix edit when shuffling is wrong.
            - Update UI for inputs. | DONE
            - Add button to edit favourite playlist cover.
            - Change icon for minimize button.
            - Only show icon on tray when hidden.
            - Add play buttons on taskbar.
            - Sort by title, length, artist.
            - Refactor structure.
        """

        Database().settings.set_path("configuration/settings.json")
        Database().songs.set_path("library/library.json")
        Database().playlists.set_path("library/playlists.json")

        songs: PlaylistSongs = Database().songs.load("library", with_extension="mp3")
        self.window.set_appsettings(Database().settings.load())
        self.window.load_library(Playlist.create(name="Library", songs=songs, cover=Images.DEFAULT_PLAYLIST_COVER))
        self.window.load_playlists(Database().playlists.load(songs.get_songs()))
