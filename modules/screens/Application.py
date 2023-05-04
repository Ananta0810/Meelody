from threading import Thread
from time import sleep

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
        self.__post_init()

    def load_playlist(self):
        """
            - pip install yt-dlp==2023.2.17
            - pip install Pillow==9.0.0
        """

        """
        TODO:
            - Add alert when delete song and playlist. | DONE
            - Add alert when song already existed. | DONE
            - Add alert when update something failed. | DONE
            - Add alert when download youtube music failed. | DONE
            - Add progress bar to show which one is downloading. | DONE
            - Add button to edit favourite playlist cover. | DONE
            - Add play buttons on taskbar. | DONE
            - Add shortcut to exit alert, dialog. | DONE
            - Add sidebar.
            - Sort by title, length, artist.
            - Allow to auto modify volume so that every song has same vibe.
            
            - Update UI for inputs. | DONE
            - Use shortcut to go to next song which start with key. | DONE
            - Change icon for minimize button. | CANCELED
            - Only show icon on tray when hidden. | DONE
            - Run thread when import songs.
            - Improve performance for menu.
            - Scroll wheel on playlist carousel to scroll. | DONE
            
            - Fix 3 alerts show up at the same time.
            - Fix edit when shuffling is wrong. | CANCELED
            - Fix first time hear song. | DONE
            - Fix color dominant in playlist. | DONE
            - Fix bug when choose songs for playlist. | DONE
            - Fix first time playing on other playlist failed. | DONE
            - Refactor structure.
        """

        Database().settings.set_path("configuration/settings.json")
        Database().songs.set_path("configuration/library.json")
        Database().playlists.set_path("configuration/playlists.json")
        Database().covers.set_path("configuration/covers.json")

        songs: PlaylistSongs = Database().songs.load("library", with_extension="mp3")
        self.window.set_appsettings(Database().settings.load())
        self.window.load_library(Playlist.create(name="Library", songs=songs, cover=Images.DEFAULT_PLAYLIST_COVER))
        self.window.load_playlists(Database().playlists.load(songs.get_songs()))

    def __post_init(self) -> None:
        Thread(target=lambda: self.__lazy_load_covers()).start()

    def __lazy_load_covers(self):
        sleep(0.5)
        covers = Database().covers.load()
        self.window.load_covers(covers)
