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

        songs = PlaylistSongs()
        songs.insert(Song.from_file("library/Abandoned Temple.mp3"))
        songs.insert(Song.from_file("library/Desire.mp3"))
        songs.insert(Song.from_file("library/Dragonmancer.mp3"))
        songs.insert(Song.from_file("library/Galadriel.mp3"))
        songs.insert(Song.from_file("library/Graze The Roof.mp3"))
        songs.insert(Song.from_file("library/Journey to the West.mp3"))
        songs.insert(Song.from_file("library/Ship Battle.mp3"))
        songs.insert(Song.from_file("library/The Call.mp3"))
        songs.insert(Song.from_file("library/Tom Tom.mp3"))

        playlist = Playlist.create(name="Library", songs=songs)
        self.window.load_playlist(playlist)

    def run(self) -> None:
        self.window.show()
