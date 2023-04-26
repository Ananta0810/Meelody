class AppSettings:
    __playing_song_id: str = None
    __is_looping: bool
    __is_shuffle: bool

    def __init__(self,
                 playing_song_id: str = None,
                 is_looping: bool = False,
                 is_shuffle: bool = False):
        self.__playing_song_id = playing_song_id
        self.__is_looping = is_looping
        self.__is_shuffle = is_shuffle

    def to_json(self) -> dict:
        return {
            'playing_song_id': self.__playing_song_id,
            'is_looping': self.__is_looping,
            'is_shuffle': self.__is_shuffle,
        }

    @staticmethod
    def from_json(json: dict) -> 'AppSettings':
        return AppSettings(json['playing_song_id'], json['is_looping'], json['is_shuffle'])

    @property
    def playing_song_id(self) -> str:
        return self.__playing_song_id

    @property
    def is_looping(self) -> bool:
        return self.__is_looping

    @property
    def is_shuffle(self) -> bool:
        return self.__is_shuffle

    def set_playing_song_id(self, playing_song_id: str) -> None:
        self.__playing_song_id = playing_song_id

    def set_is_looping(self, is_looping: bool) -> None:
        self.__is_looping = is_looping

    def set_is_shuffle(self, is_shuffle: bool) -> None:
        self.__is_shuffle = is_shuffle
