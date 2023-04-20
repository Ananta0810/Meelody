from logging import getLogger

from modules.helpers.Files import Files
from modules.models.Playlist import Playlist
from modules.models.PlaylistSongs import PlaylistSongs
from modules.models.Song import Song
from modules.screens.windows.MainWindowControl import MainWindowControl
from modules.statics.view import Material


class Application:
    def __init__(self):
        Material.Cursors.init_value()
        Material.Icons.init_value()

        self.window = MainWindowControl()
        self.window.apply_light_mode()

        songs: PlaylistSongs = Application.get_playlist_from_dir("library", with_extension="mp3")
        playlist = Playlist.create(name="Library", songs=songs)
        self.window.load_playlist(playlist)

    def run(self) -> None:
        self.window.show()

    @staticmethod
    def get_playlist_from_dir(directory: str, with_extension: str) -> PlaylistSongs:
        getLogger().setLevel("ERROR")
        playlist = PlaylistSongs()
        files: set = Files.get_files_from(directory, with_extension)
        for file in files:
            playlist.insert(Song.from_file(location=file))
        return playlist
