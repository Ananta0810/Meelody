from sys import path

path.append("./lib")

from modules.entities.playlist_info import PlaylistInfo


class PlaylistSelector:
    def __init__(self, ui) -> None:
        self.ui = ui
        self.playlists = []

    def setPlaylists(self, playlists: list[PlaylistInfo]) -> None:
        self.playlists = playlists

    def handleSelectedLibrary(self) -> None:
        self.ui.playlist_info.setInfo(None, "Library", 100)

    def handleSelectedFavourites(self) -> None:
        self.ui.playlist_info.setInfo(None, "Favourites", 50)

    def handleSelectedPlaylist(self, index: int) -> None:
        playlist: PlaylistInfo = self.playlists[index]
        self.ui.playlist_info.setInfo(playlist.cover, playlist.cover, 50)
