import random

from modules.helpers.types.Decorators import override
from modules.helpers.types.Lists import Lists
from modules.models.Song import Song


class PlaylistSongs:
    __songs: list[Song]
    __backup_songs: list[Song]
    __order_by: str
    __is_sorted: bool

    def __init__(self, order_by: str = "title"):
        self.__songs = []
        self.__backup_songs = []
        self.__order_by = order_by
        self.__is_sorted = True

    @staticmethod
    def create_empty() -> 'PlaylistSongs':
        return PlaylistSongs()

    @override
    def __str__(self):
        string = ""
        for index, song in enumerate(self.__songs):
            string += f"{index}. {str(song)}\n"
        return string

    def get_songs(self) -> list[Song]:
        return self.__songs

    def is_sorted(self):
        return self.__is_sorted

    def has_any_song(self) -> bool:
        return len(self.__songs) > 0

    def move_song(self, from_index: int, to_index: int) -> None:
        Lists.move_element(self.__songs, from_index, to_index)

    def size(self) -> int:
        """
        return the number of songs in the list
        """
        return len(self.__songs)

    def set_order_by(self, prop: str) -> None:
        self.__order_by = prop

    def get_song(self, index: int) -> Song:
        """
        Get the song at the given index
        """
        if self.size() == 0:
            raise Exception("Playlist has no song.")
        return self.__songs[index]

    def insert(self, song: Song) -> int:
        """
        Add song to the list of songs. If added successfully, it will return the position of the song in the playlist
        """
        # TODO: Refactor this
        if self.__is_sorted and self.__order_by == "title":
            position: int = Lists.string_binary_search(
                self.__songs,
                search_value=song.get_title(),
                key_provider=lambda s: s.get_title(),
                find_nearest=True
            )
            self.__songs.insert(position, song)
            return position
        self.__songs.append(song)
        return len(self.__songs) - 1

    def shuffle(self):
        self.__backup_songs = self.__songs.copy()
        self.__is_sorted = False
        random.shuffle(self.__songs)

    def unshuffle(self):
        if len(self.__songs) == len(self.__backup_songs):
            self.__songs = self.__backup_songs.copy()
        self.__is_sorted = True
        self.__backup_songs.clear()

    def find_song_index_by_title(self, title) -> int:
        if self.__is_sorted and self.__order_by == "title":
            return Lists.string_binary_search(self.__songs, search_value=title, key_provider=lambda s: s.get_title())
        return Lists.string_linear_search(self.__songs, search_value=title, key_provider=lambda s: s.get_title())

    def find_nearest_song_index_by_title(self, title) -> int:
        if self.__is_sorted and self.__order_by == "title":
            return Lists.string_binary_search(
                self.__songs, search_value=title, key_provider=lambda s: s.get_title(), find_nearest=True
            )
        return Lists.string_nearest_linear_search(self.__songs, search_value=title, key_provider=lambda s: s.get_title())

    def find(self, song: Song) -> int:
        """
        Find the index Of song in the list
        """
        if not self.__is_sorted:
            return Lists.string_linear_search(
                self.__songs,
                search_value=song.get_title(),
                key_provider=lambda s: s.get_title()
            )

        if self.__order_by == "title":
            return Lists.string_binary_search(
                self.__songs,
                search_value=song.get_title(),
                key_provider=lambda s: s.get_title()
            )

        if self.__order_by == "artist":
            return Lists.string_binary_search(
                self.__songs,
                search_value=song.get_artist(),
                key_provider=lambda s: s.get_artist()
            )

        raise Exception("Sorting not supported.")
