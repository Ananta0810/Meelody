from contextlib import suppress

from app.common.models.playlist import Playlist
from app.common.models.song import Song
from app.helpers.base import Bytes, Strings
from .common_playlist import CommonPlaylist


class UserPlaylist(Playlist):
    class Info(CommonPlaylist.Info):
        pass

    class Songs(CommonPlaylist.Songs):

        def setSongs(self, songs: list[Song]) -> None:
            super().setSongs(songs)

            for song in songs:
                self.__connectToSong(song)

            self.updated.emit()

        def insert(self, song: Song) -> None:
            super().insert(song)
            self.__connectToSong(song)
            self.updated.emit()

        def insertAll(self, songs: list[Song]) -> None:
            super().insertAll(songs)

            if songs is None:
                return

            for song in songs:
                self.__connectToSong(song)

            self.updated.emit()

        def removeAll(self, songs: list[Song]) -> None:
            super().removeAll(songs)

            if songs is None:
                return

            for song in songs:
                self.__disconnectToSong(song)

            self.updated.emit()

        def remove(self, song: Song) -> None:
            super().remove(song)
            self.__disconnectToSong(song)
            self.updated.emit()

        def _onSongUpdated(self, song: Song, updatedField: str) -> None:
            if updatedField == "title":
                self._songs.remove(song)
                newPosition = self.__findInsertPosition(song)
                self._songs.insert(newPosition, song)
                self.updated.emit()

        def __connectToSong(self, song: Song) -> None:
            song.updated.connect(lambda updatedField: self._onSongUpdated(song, updatedField))
            song.deleted.connect(lambda: self.remove(song))

        def __disconnectToSong(self, song: Song) -> None:
            with suppress(TypeError):
                song.updated.disconnect(lambda updatedField: self._onSongUpdated(song, updatedField))
                song.deleted.disconnect(lambda: self.remove(song))

        def moveSong(self, fromIndex: int, toIndex: int) -> None:
            super().moveSong(fromIndex, toIndex)
            self.updated.emit()

        def clone(self) -> Playlist.Songs:
            return UserPlaylist.Songs(self.toList(), self._isSorted)

    def clone(self) -> 'Playlist':
        return UserPlaylist(self.getInfo(), self.getSongs())

    def toDict(self) -> dict:
        playlistInfo = self.getInfo()

        info = {"name": playlistInfo.getName(), "id": playlistInfo.getId(), "cover": playlistInfo.getCoverPath()}
        ids: list[str] = [song.getId() for song in self.getSongs().toList()]

        return {'info': info, 'ids': ids}

    @staticmethod
    def fromDict(json: dict, songs: list[Song]) -> 'UserPlaylist':
        jsonInfo = json['info']
        songIds = set(json['ids'])

        id_ = jsonInfo.get("id", Strings.randomId())
        name = jsonInfo.get("name", id_)
        path = jsonInfo.get("cover", None)
        cover = None if path is None else Bytes.fromFile(path)
        path = None if cover is None else path

        info = UserPlaylist.Info(id=id_, name=name, coverPath=path, cover=cover)
        songs = UserPlaylist.Songs([song for song in songs if song.getId() in songIds])

        return UserPlaylist(info, songs)
