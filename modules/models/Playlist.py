from modules.models.PlaylistInformation import PlaylistInformation
from modules.models.PlaylistSongs import PlaylistSongs
from modules.models.Song import Song


class Playlist:
    __info: PlaylistInformation
    __songs: PlaylistSongs

    def __init__(self, info: PlaylistInformation, songs: PlaylistSongs):
        self.__info = info
        self.__songs = songs

    @staticmethod
    def create(name: str, cover: bytes = None, songs: PlaylistSongs = None) -> 'Playlist':
        return Playlist(PlaylistInformation(name, cover), songs or PlaylistSongs.create_empty())

    def get_info(self) -> PlaylistInformation:
        return self.__info

    def get_songs(self) -> PlaylistSongs:
        return self.__songs

    def size(self) -> int:
        """
        :return: total songs of this playlist. 0 if playlist has no songs.
        :rtype: int
        """
        return 0 if self.__songs is None else self.__songs.size()

    def equals(self, other) -> bool:
        """
        Check if two playlists are the same one
        """
        return self.__info == other.__info


class PlaylistJson:
    __info: PlaylistInformation
    __ids: list[str]

    def __init__(self, info: PlaylistInformation, ids: list[str]):
        self.__info = info
        self.__ids = ids

    @staticmethod
    def from_playlist(playlist: Playlist) -> 'PlaylistJson':
        ids: list[str] = [song.get_id() for song in playlist.get_songs().get_songs()]
        return PlaylistJson(info=playlist.get_info(), ids=ids)

    @staticmethod
    def from_json(json: dict) -> 'PlaylistJson':
        info = PlaylistInformation(name=json['__info']['name'])
        info.id = json['__info']['id']
        return PlaylistJson(info, json['__ids'])

    def to_playlist(self, songs: list[Song]) -> Playlist:
        ids = set(self.__ids)
        return Playlist(info=self.__info, songs=PlaylistSongs(songs=[song for song in songs if song.get_id() in ids]))

    def to_json(self) -> dict:
        return {
            '__info': {
                'name': self.__info.name,
                'id': self.__info.id,
            },
            '__ids': self.__ids
        }
