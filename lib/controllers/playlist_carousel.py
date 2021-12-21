from sys import path

path.append("./lib")

from modules.entities.playlist_info import PlaylistInfo
from utils.helpers.my_bytes import MyBytes
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
        numberOfPlaylistDisplaying = self.ui.getTotalPlaylistInLayout()
        totalOfPlaylists = len(self.playlists)

        numberOfLackingPlaylists = totalOfPlaylists - numberOfPlaylistDisplaying
        if numberOfLackingPlaylists == 0:
            return

        isDisplayingMoreThanNumberOfPlaylists = numberOfLackingPlaylists < 0
        if isDisplayingMoreThanNumberOfPlaylists:
            self.ui.hidePlaylistInRange(totalOfPlaylists - 1, numberOfPlaylistDisplaying)
            return

        isDisplayingLessThanNumberOfPlaylists = numberOfLackingPlaylists > 0
        if isDisplayingLessThanNumberOfPlaylists:
            self.ui.addPlaylists(numberOfLackingPlaylists)

    def handleAddNewPlaylist(self):
        lastPlaylist = self.playlists[len(self.playlists) - 1]
        if lastPlaylist.isNull():
            return

        self.playlists.append(PlaylistInfo())
        countOfPlaylistsDisplaying = self.ui.getNumberOfPlaylistDisplaying()
        totalPlaylistAvailable = self.ui.getTotalPlaylistInLayout()

        isHiddingPlaylist: bool = countOfPlaylistsDisplaying < totalPlaylistAvailable
        if isHiddingPlaylist:
            newPlaylistIndex = countOfPlaylistsDisplaying
            self.ui.showPlaylistAtIndex(newPlaylistIndex)
            return

        self.ui.addNewEmptyPlaylist(self)

    def handleSelectedLibrary(self):
        print("clicked library")

    def handleSelectedFavourites(self):
        print("clicked favourites")

    def handleSelectedPlaylist(self, playlistIndex: int):
        print(playlistIndex)

    def handleChangedPlaylistName(self, playlistIndex: int, newName: str):
        currentName = self.playlists[playlistIndex].name
        userHasChangedPlaylistName: bool = UnicodeString.compare(currentName, newName) != 0
        if not userHasChangedPlaylistName:
            self.ui.changePlaylistNameAtIndex(playlistIndex, currentName)
            return
        self.playlists[playlistIndex].name = newName

    def handleChangedPlaylistCover(self, playlistIndex: int, coverPath: str):
        if len(coverPath) == 0:
            return
        cover: bytes = MyBytes.getBytesFromFile(coverPath)
        self.playlists[playlistIndex].cover = cover
        self.ui.changePlaylistCoverAtIndex(playlistIndex, cover)

    def handleDeletePlaylistAtIndex(self, index: int):
        if not (0 <= index < len(self.playlists)):
            return
        self.playlists.pop(index)
        self.updatePlaylistsToUi()
