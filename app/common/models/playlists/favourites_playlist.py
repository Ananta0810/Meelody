from contextlib import suppress

from app.common.models.playlist import Playlist
from app.common.models.song import Song
from app.common.others.data_location import DataLocation
from app.utils.base import Bytes, Lists
from app.utils.reflections import SingletonMeta
from .common_playlist import CommonPlaylist
from ...others.translator import Translator


class FavouritesPlaylist(Playlist, metaclass=SingletonMeta):
    class Info(CommonPlaylist.Info, metaclass=SingletonMeta):
        def __init__(self):
            translator = Translator()
            super().__init__(id="Favourites",
                             name=translator.translate("PLAYLIST_CAROUSEL.FAVOURITES"),
                             cover=Bytes.fromFile(f"{DataLocation().configuration}/playlists/favourite-cover.png"))

            Translator().changed.connect(lambda: self.__setName(translator.translate("PLAYLIST_CAROUSEL.FAVOURITES")))

        def setName(self, name: str) -> None:
            pass

        def __setName(self, name: str) -> None:
            self._name = name

        def setCover(self, cover: bytes) -> None:
            pass

    class Songs(CommonPlaylist.Songs):

        def __init__(self, library: Playlist):
            super().__init__(None, isSorted=True)
            self.__library = library

            library.getSongs().updated.connect(lambda: self.updated.emit())

        def load(self):
            for song in self._songs:
                self.__disconnectToSong(song)

            self._songs = [song for song in self.__library.getSongs().toList() if song.isLoved()]

            for song in self._songs:
                self.__connectToSong(song)

        def __connectToSong(self, song: Song) -> None:
            song.deleted.connect(lambda: self.remove(song))

        def __disconnectToSong(self, song: Song) -> None:
            with suppress(TypeError):
                song.deleted.disconnect(lambda: self.remove(song))

        def toList(self) -> list[Song]:
            return self._songs

        def hasAnySong(self) -> bool:
            return len(self._songs) > 0

        def hasSong(self, song: Song) -> bool:
            return song.isLoved()

        def size(self) -> int:
            return len(self._songs)

        def getSongAt(self, index: int) -> Song:
            return self._songs[index]

        def indexOf(self, song: Song) -> int:
            return Lists.linearSearch(self._songs, song)

        def setSongs(self, songs: list[Song]) -> None:
            pass

        def insert(self, song: Song) -> None:
            pass

        def insertAll(self, songs: list[Song]) -> None:
            pass

        def removeAll(self, songs: list[Song]) -> None:
            pass

        def remove(self, song: Song) -> None:
            pass

        def clone(self) -> Playlist.Songs:
            return self

    def __init__(self, library: Playlist):
        super().__init__(FavouritesPlaylist.Info(), FavouritesPlaylist.Songs(library))

    def load(self) -> None:
        self.getSongs().load()

    def clone(self) -> 'Playlist':
        return self
