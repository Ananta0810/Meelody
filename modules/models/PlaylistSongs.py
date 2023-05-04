import random
from typing import Callable, TypeVar

from modules.helpers.types import Lists, Strings
from modules.helpers.types.Decorators import override
from modules.models.Song import Song

T = TypeVar('T')


class _SongComparator:
    def __init__(self, key_provider: Callable[[Song], T], comparator: Callable[[T, T], int]) -> None:
        self.__key_provider = key_provider
        self.__comparator = comparator

    def key_of(self, song: Song) -> T:
        return self.__key_provider(song)

    def comparator(self) -> Callable[[Song, Song], int]:
        return lambda s1, s2: self.__comparator(self.__key_provider(s1), self.__key_provider(s2))


_comparator_map: dict[Song.Order, _SongComparator] = {
    Song.Order.TITLE: _SongComparator(Song.get_title, Strings.compare),
    Song.Order.ARTIST: _SongComparator(Song.get_artist, Strings.compare),
    Song.Order.LENGTH: _SongComparator(Song.get_length, lambda x, y: x - y),
}


class PlaylistSongs:
    __songs: list[Song]
    __backup_songs: list[Song]
    __order_by: Song.Order
    __is_sorted: bool

    def __init__(self, songs=None, order_by: Song.Order = Song.Order.TITLE):
        self.__songs = []
        self.__backup_songs = []
        self.__order_by = order_by
        self.__is_sorted = True
        if songs is not None:
            self.insertAll(songs)

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
        return any(song == song_ for song_ in self.__songs)

    def move_song(self, from_index: int, to_index: int) -> None:
        Lists.move_element(self.__songs, from_index, to_index)

    def size(self) -> int:
        """
        return the number of songs in the list
        """
        return len(self.__songs)

    def set_order_by(self, prop: Song.Order.TITLE) -> None:
        self.__order_by = prop

    def get_song_at(self, index: int) -> Song:
        """
        Get the song at the given index
        """
        if self.size() == 0:
            raise ValueError("Playlist has no song.")
        return self.__songs[index]

    def insert(self, song: Song) -> int:
        """
        Add song to the list of songs. If added successfully, it will return the position of the song in the playlist
        """
        position = self.__find_insert_position(song)

        if self.is_sorted():
            self.__songs.insert(position, song)
            return position

        self.__songs.append(song)
        self.__backup_songs.insert(position, song)
        return len(self.__songs) - 1

    def __find_insert_position(self, song) -> int:
        return Lists.binary_search(self.__songs, song, comparator=self.__comparator(), find_nearest=True)

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

    def remove_song(self, song: Song) -> None:
        if self.is_sorted():
            index_to_remove_on_backup_songs = Lists.binary_search(self.__songs, song, self.__comparator())

            self.__songs.remove(self.__songs[index_to_remove_on_backup_songs])
            return

        index_to_remove_on_backup_songs = Lists.binary_search(self.__backup_songs, song, self.__comparator())
        self.__backup_songs.remove(self.__backup_songs[index_to_remove_on_backup_songs])

        index_to_remove_on_display_songs = Lists.linear_search(self.__songs, song, self.__comparator())

        self.__songs.remove(self.__songs[index_to_remove_on_display_songs])

    def index_of(self, song: Song) -> int:
        """
        Find the index Of song in the list
        """
        return (
            Lists.binary_search(self.__songs, song, self.__comparator())
            if self.__is_sorted
            else Lists.linear_search(self.__songs, song, self.__comparator())
        )

    def __comparator(self):
        return _comparator_map[self.__order_by].comparator()
