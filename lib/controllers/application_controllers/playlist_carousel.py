from controllers.application_controllers.playlist_menu import PlaylistMenuController
from controllers.self_controllers.playlist_carousel import PlaylistCarousel


class PlaylistCarouselController:
    def setMainController(self, controller: PlaylistCarousel) -> None:
        self.carousel = controller
        self.carousel.ui.connectToController(self)
        self.library = None
        self.favourites = None
        self.currentPlaylist = "library"

    def setSecondController(self, controller: PlaylistMenuController) -> None:
        self.menu = controller

    def addPlaylistsToUi(self) -> None:
        for index, playlist in enumerate(self.carousel.playlists):
            self.carousel.ui.addNewEmptyPlaylist(controller=self)
            self.carousel.ui.displayPlaylistInfoAtIndex(index, playlist.name, playlist.cover)

    def updatePlaylistsToUi(self) -> None:
        self.carousel.ui.updateLayout(len(self.carousel.playlists), controller=self)
        for index, playlist in enumerate(self.carousel.playlists):
            self.carousel.ui.displayPlaylistInfoAtIndex(index, playlist.name, playlist.cover)

    def handleAddNewPlaylist(self) -> None:
        self.carousel.handleAddNewPlaylist()
        self.carousel.ui.updateLayout(len(self.carousel.playlists), controller=self)

    def handleSelectedLibrary(self) -> None:
        if self.currentPlaylist == "library":
            return
        self.currentPlaylist = "library"
        self.carousel.handleSelectedLibrary()
        self.menu.menu.playlist._songs = self.library
        self.menu.updatePlaylistToScreen()
        self.menu.menu.ui.setCurrentPlaylistInfo("Library", len(self.library))

    def handleSelectedFavourites(self) -> None:
        if self.currentPlaylist == "favourites":
            return
        self.currentPlaylist = "favourites"
        self.carousel.handleSelectedFavourites()

        if self.library is None:
            self.library = self.menu.menu.playlist.getSongs()

        self.favourites = [song for song in self.library if song.loved]
        self.menu.menu.playlist._songs = self.favourites
        self.menu.updatePlaylistToScreen()
        self.menu.menu.ui.setCurrentPlaylistInfo("Favourites", len(self.favourites))

    def handleSelectedPlaylist(self, index: int) -> None:
        self.carousel.handleSelectedPlaylist(index)
        playlist = self.carousel.playlists[index]
        if playlist.name is None:
            return
        if self.currentPlaylist == playlist.name:
            return
        self.menu.menu.playlist.shuffle()
        self.menu.updatePlaylistToScreen()
        self.menu.menu.ui.setCurrentPlaylistInfo(playlist.name, len(self.menu.menu.playlist._songs), playlist.cover)

    def handleChangedPlaylistName(self, playlistIndex: int, newName: str) -> None:
        self.carousel.handleChangedPlaylistName(playlistIndex, newName)

    def handleChangedPlaylistCover(self, playlistIndex: int, coverPath: str) -> None:
        self.carousel.handleChangedPlaylistCover(playlistIndex, coverPath)

    def handleDeletePlaylistAtIndex(self, index: int) -> None:
        self.carousel.handleDeletePlaylistAtIndex(index)
        self.updatePlaylistsToUi()
