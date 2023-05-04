import random
from typing import Callable

from modules.helpers.types import Lists
from modules.helpers.types.Decorators import override
from modules.models.Song import Song


class PlaylistSongs:
    __songs: list[Song]
    __backup_songs: list[Song]
    __order_by: str
    __is_sorted: bool

    __key_map: dict[str, Callable[[Song], any]] = {
        'title': lambda song: song.get_title(),
        'artist': lambda song: song.get_artist(),
        'length': lambda song: song.get_artist(),
    }

    def __init__(self, songs=None, order_by: str = "title"):
        self.__songs = []
        self.__backup_songs = []
        self.__order_by = order_by
        self.__is_sorted = True
        if songs is not None:
            self.insertAll(songs)

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
        return [song for song in self.__songs]

    def get_original_songs(self) -> list[Song]:
        return self.__backup_songs if len(self.__backup_songs) > 0 else self.__songs

    def is_sorted(self):
        return self.__is_sorted

    def has_any_song(self) -> bool:
        return len(self.__songs) > 0

    def has_song(self, song: Song) -> bool:
        return any(song.get_title() == song_.get_title() for song_ in self.__songs)

    def move_song(self, from_index: int, to_index: int) -> None:
        Lists.move_element(self.__songs, from_index, to_index)

    def size(self) -> int:
        """
        return the number of songs in the list
        """
        return len(self.__songs)

    def set_order_by(self, prop: str) -> None:
        self.__order_by = prop

    def get_song_at(self, index: int) -> Song:
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

        position = self.__find_insert_position(song)

        if self.is_sorted():
            self.__songs.insert(position, song)
            return position
        self.__songs.append(song)
        self.__backup_songs.insert(position, song)
        return len(self.__songs) - 1

    def __find_insert_position(self, song) -> int:
        return Lists.string_binary_search(
            self.__songs,
            search_value=song.get_title(),
            key_provider=PlaylistSongs.__key_map[self.__order_by],
            find_nearest=True
        )

    def insertAll(self, songs: list[Song]):
        if songs is not None:
            for song in songs:
                self.insert(song)

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
        if self.__is_sorted:
            return Lists.string_binary_search(self.__songs, search_value=title, key_provider=self.__key_provider())
        return Lists.string_linear_search(self.__songs, search_value=title, key_provider=self.__key_provider())

    def find_nearest_song_index_by_title(self, title) -> int:
        if self.__is_sorted:
            return Lists.string_binary_search(self.__songs, search_value=title, key_provider=self.__key_provider(),
                                              find_nearest=True)
        return Lists.string_nearest_linear_search(self.__songs, search_value=title, key_provider=self.__key_provider())

    def remove_song(self, song: Song) -> None:
        if self.is_sorted():
            index_to_remove_on_backup_songs = Lists.string_binary_search(self.__songs,
                                                                         search_value=song.get_title(),
                                                                         key_provider=PlaylistSongs.__key_map[
                                                                             self.__order_by])
            self.remove_song(self.__songs[index_to_remove_on_backup_songs])
            return

        index_to_remove_on_backup_songs = Lists.string_binary_search(
            self.__backup_songs, search_value=song.get_title(), key_provider=self.__key_provider()
        )
        self.__backup_songs.remove(self.__backup_songs[index_to_remove_on_backup_songs])

        index_to_remove_on_display_songs = Lists.string_linear_search(self.__songs, song.get_title(),
                                                                      self.__key_provider())

        self.__songs.remove(self.__songs[index_to_remove_on_display_songs])

    def index_of(self, song: Song) -> int:
        """
        Find the index Of song in the list
        """
        return (
            Lists.string_binary_search(self.__songs, song.get_title(), self.__key_provider())
            if self.__is_sorted
            else Lists.string_linear_search(self.__songs, song.get_title(), self.__key_provider())
        )

    def __key_provider(self):
        return PlaylistSongs.__key_map[self.__order_by]
