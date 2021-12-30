from sys import path

path.append("./lib")

from modules.entities.playlist_info import PlaylistInfo
from utils.helpers.my_bytes import MyBytes
from utils.helpers.my_string import UnicodeString
from views.body.playlist_carousel.carousel import UIPlaylistCarousel


class PlaylistCarousel:
    def __init__(self, ui: UIPlaylistCarousel):
        self.ui = ui
        self.playlists = None

    def setPlaylists(self, playlists: list[PlaylistInfo]):
        self.playlists = playlists

    def handleAddNewPlaylist(self):
        playlistCount = len(self.playlists)
        if playlistCount > 0:
            lastPlaylist = self.playlists[playlistCount - 1]
            if lastPlaylist.isNull():
                return
        self.playlists.append(PlaylistInfo())

    def handleSelectedLibrary(self):
        pass

    def handleSelectedFavourites(self):
        pass

    def handleSelectedPlaylist(self, playlistIndex: int):
        pass

    def handleChangedPlaylistName(self, playlistIndex: int, newName: str):
        if not (0 <= playlistIndex < len(self.playlists)):
            return
        currentName = self.playlists[playlistIndex].name
        userHasChangedPlaylistName: bool = (
            True if currentName is None else UnicodeString.compare(currentName, newName) != 0
        )
        userTypedCorrectName: bool = userHasChangedPlaylistName and len(newName) != 0

        if not userTypedCorrectName:
            self.ui.changePlaylistNameAtIndex(playlistIndex, currentName)
            return
        self.playlists[playlistIndex].name = newName

    def handleChangedPlaylistCover(self, playlistIndex: int, coverPath: str):
        if not (0 <= playlistIndex < len(self.playlists)):
            return
        if len(coverPath) == 0:
            return
        cover: bytes = MyBytes.getBytesFromFile(coverPath)
        self.playlists[playlistIndex].cover = cover
        self.ui.changePlaylistCoverAtIndex(playlistIndex, cover)

    def handleDeletePlaylistAtIndex(self, index: int):
        if not (0 <= index < len(self.playlists)):
            return
        self.playlists.pop(index)
