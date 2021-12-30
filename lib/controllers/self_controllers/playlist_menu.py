from modules.models.playlist_songs import PlaylistSongs
from utils.helpers.my_bytes import MyBytes
from utils.helpers.my_string import UnicodeString
from views.body.current_playlist.current_playlist import CurrentPlaylist


class PlaylistMenu:
    def __init__(self, ui: CurrentPlaylist):
        self.ui = ui
        self.playlist = None

    def setPlaylist(self, playlist: PlaylistSongs):
        self.playlist = playlist

    def handleFindSongInsertIndexWithTitle(self, title) -> int:
        return self.playlist.findSongInsertPosition(title)

    def handleChangedLoveStateOfSongAtIndex(self, index: int, isLoved: bool) -> None:
        if self.playlist is None:
            return
        songs = self.playlist.getSongs()
        if not (0 <= index < len(songs)):
            return
        songs[index].loved = isLoved

    def handlePlayedSongAtIndex(self, index: int) -> None:
        if self.playlist is None:
            return
        songs = self.playlist.getSongs()
        if not (0 <= index < len(songs)):
            return

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
        songs.pop(index)
        self.updatePlaylistToScreen()

    def handleChangedSongTitle(self, index: int, newTitle: str) -> None:
        if self.playlist is None:
            return
        songs = self.playlist.getSongs()
        if not (0 <= index < len(songs)):
            return
        song = songs[index]
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

    def handleChangedSongArtist(self, index: int, newArtist: str) -> None:
        if self.playlist is None:
            return
        songs = self.playlist.getSongs()
        if not (0 <= index < len(songs)):
            return

        song = songs[index]
        userChangedTitle: bool = (
            True
            if song.artist is None
            else (len(newArtist) != 0 and UnicodeString.compare(song.artist, newArtist) != 0)
        )
        if not userChangedTitle:
            self.ui.setSongArtistAtIndex(index, song.artist)
            return
        song.setArtist(newArtist)

    def handleChangedSongCover(self, index: int, coverPath: str) -> None:
        if self.playlist is None:
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
