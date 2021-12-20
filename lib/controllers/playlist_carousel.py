from sys import path

path.append("./lib")

from modules.entities.playlist_info import PlaylistInfo
from utils.helpers.my_string import UnicodeString
from views.ui_playlist_carousel import UiPlaylistCarousel


class PlaylistCarousel:
    def __init__(self, ui: UiPlaylistCarousel):
        self.ui = ui
        self.playlists = None

    def setPlaylists(self, playlists: list[PlaylistInfo]):
        self.playlists = playlists

    def addPlaylistsToUi(self):
        for playlist in self.playlists:
            position = self.ui.addNewEmptyPlaylist(controller=self)
            self.ui.displayPlaylistInfoAtIndex(position, playlist.name, playlist.cover)

    def updatePlaylistsToUi(self):
        self.__refreshLayoutSoThatUiDisplayingEnoughNumberOfPlaylists()
        for index, playlist in enumerate(self.playlists):
            self.ui.showPlaylistAtIndex(index)
            self.ui.displayPlaylistInfoAtIndex(index, playlist.name, playlist.cover)

    def __refreshLayoutSoThatUiDisplayingEnoughNumberOfPlaylists(self):
        totalOfPlaylistsDisplayingOnUi = self.ui.getTotalPlaylistInLayout()
        currentTotalOfPlaylis = len(self.playlists)

        if currentTotalOfPlaylis < totalOfPlaylistsDisplayingOnUi:
            for index in range(currentTotalOfPlaylis, totalOfPlaylistsDisplayingOnUi):
                self.ui.hidePlaylistAtIndex(index)
                self.ui.displayPlaylistInfoAtIndex(index, name="Unknown", cover=None)

        if totalOfPlaylistsDisplayingOnUi < currentTotalOfPlaylis:
            for index in range(totalOfPlaylistsDisplayingOnUi, currentTotalOfPlaylis + 1):
                self.ui.addNewEmptyPlaylist(controller=self)

    def handleAddNewPlaylist(self):
        countOfPlaylistsDisplayingOnUi = self.ui.getTotalPlaylistDisplayingInLayout()
        currentTotalOfPlaylis = len(self.playlists)
        if countOfPlaylistsDisplayingOnUi < self.ui.getTotalPlaylistInLayout():
            self.ui.showPlaylistAtIndex(countOfPlaylistsDisplayingOnUi + 1)
            print(countOfPlaylistsDisplayingOnUi)
            return
        self.ui.addNewEmptyPlaylist(self)

    def handleSelectedLibrary(self):
        print("clicked library")

    def handleSelectedFavourites(self):
        print("clicked favourites")

    def handleSelectedPlaylist(self, playlistIndex: int):
        print(playlistIndex)

    def handleChangedPlaylistName(selfm, playlistIndex: int, playlistLabel):
        lastInput: str = playlistLabel.lastInput
        recentlyInput: str = playlistLabel.text()

        userHasChangedPlaylistName: bool = UnicodeString.compare(lastInput, recentlyInput) != 0
        if not userHasChangedPlaylistName:
            playlistLabel.setText(lastInput)
            return
        print("Change playlist name successfully")

    def handleDeletePlaylistAtIndex(self, index: int):
        if not (0 <= index < len(self.playlists)):
            return
        self.playlists.pop(index)
        self.updatePlaylistsToUi()
