from sys import path

path.append("./lib")

from modules.models.playlist_songs import PlaylistSongs
from utils.helpers.my_bytes import MyBytes
from utils.helpers.my_string import UnicodeString


class PlaylistMenu:
    def __init__(self, ui):
        self.ui = ui
        self.playlist = None
        self.controllers = None

    def setControllers(self, controllers):
        self.controllers = controllers

    def setPlaylist(self, playlist: PlaylistSongs):
        self.playlist = playlist

    def updateUi(self, isDarkMode: bool) -> None:
        self.updatePlaylistToScreen()
        if isDarkMode:
            self.ui.darkMode()
        else:
            self.ui.lightMode()

    def updatePlaylistToScreen(self):
        songs = self.playlist.getSongs()
        self.ui.updateLayout(len(songs), controller=self)
        for index, song in enumerate(songs):
            self.ui.displaySongInfoAtIndex(index, song.cover, song.title, song.artist, song.length)

    def handleFindSongInsertIndexWithTitle(self, title) -> int:
        return self.playlist.findSongInsertPosition(title)

    def handleChangedLoveStateOfSongAtIndex(self, index: int, isLoved: bool) -> None:
        if self.playlist is None:
            return
        songs = self.playlist.getSongs()
        if not (0 <= index < len(songs)):
            return
        songs[index].loved = isLoved

        if self.__isPlayingSongAtIndex(index):
            self.controllers.get("musicPlayer").ui.setLoveState(isLoved)

    def handlePlayedSongAtIndex(self, index: int) -> None:
        if self.playlist is None:
            return
        songs = self.playlist.getSongs()
        if not (0 <= index < len(songs)):
            return
        if self.__isPlayingSongAtIndex(index):
            return
        musicPlayer = self.controllers.get("musicPlayer")
        musicPlayer.player.setCurrentSongIndex(index)
        musicPlayer.playSong()

    def handleAddSongToPlaylistAtIndex(self, index: int) -> None:
        pass

    def handleEditSongAtIndex(self, index: int) -> None:
        pass

    def handleDeleteSongAtIndex(self, index: int) -> None:
        if self.playlist is None:
            return
        songs = self.playlist.getSongs()
        if not (0 <= index < len(songs)):
            return
        if self.__isPlayingSongAtIndex(index):
            return
        songs.pop(index)
        self.updatePlaylistToScreen()

    def handleChangedSongTitle(self, index: int, newTitle: str):
        if self.playlist is None:
            return
        songs = self.playlist.getSongs()
        if not (0 <= index < len(songs)):
            return
        song = songs[index]
        if self.__isPlayingSongAtIndex(index):
            self.ui.setSongTitleAtIndex(index, song.title)
            return
        changedTitle: bool = (
            True if song.title is None else (len(newTitle) != 0 and UnicodeString.compare(song.title, newTitle) != 0)
        )
        if not changedTitle:
            self.ui.setSongTitleAtIndex(index, song.title)
            return
        changeSuccessfully = song.setTitle(newTitle)
        if not changeSuccessfully:
            self.ui.setSongTitleAtIndex(index, song.title)
            return
        songs.pop(index)
        newSongIndex: int = self.playlist.insert(song)
        self.updatePlaylistToScreen()
        self.ui.scrollToItem(newSongIndex)

    def handleChangedSongArtist(self, index: int, newArtist: str):
        if self.playlist is None:
            return
        songs = self.playlist.getSongs()
        if not (0 <= index < len(songs)):
            return

        song = songs[index]
        if self.__isPlayingSongAtIndex(index):
            self.ui.setSongArtistAtIndex(index, song.artist)
            return
        userChangedTitle: bool = (
            True
            if song.artist is None
            else (len(newArtist) != 0 and UnicodeString.compare(song.artist, newArtist) != 0)
        )
        if not userChangedTitle:
            self.ui.setSongArtistAtIndex(index, song.artist)
            return
        song.setArtist(newArtist)

    def handleChangedSongCover(self, index: int, coverPath: str):
        if self.playlist is None:
            return
        if self.__isPlayingSongAtIndex(index):
            return
        songs = self.playlist.getSongs()
        if not (0 <= index < len(songs)):
            return
        if len(coverPath) == 0:
            return

        cover: bytes = MyBytes.getBytesFromFile(coverPath)
        changeSuccessfully: bool = songs[index].setCover(cover)
        if not changeSuccessfully:
            return
        self.ui.setSongCoverAtIndex(index, cover)

    def __isPlayingSongAtIndex(self, index: int) -> bool:
        return self.controllers.get("musicPlayer").player.getCurrentSongIndex() == index
