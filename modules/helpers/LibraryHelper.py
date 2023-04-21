import os.path
from logging import getLogger

from modules.helpers.Files import Files
from modules.helpers.Jsons import Jsons
from modules.models.PlaylistSongs import PlaylistSongs
from modules.models.Song import Song

library_path: str = "library/library.json"
favourite_path: str = "library/favourites.json"


def load_songs_from_dir(directory: str, with_extension: str) -> PlaylistSongs:
    return get_songs_from_json(library_path) \
        if os.path.exists(library_path) \
        else get_songs_from_files(directory, library_path, with_extension)


def load_favourite_songs(library_songs: PlaylistSongs) -> PlaylistSongs:
    favourite_ids: set[str] = set(__get_favourite_ids())
    favourite_songs: list[Song] = list(filter(lambda song_: song_.get_id() in favourite_ids, library_songs.get_songs()))
    playlist = PlaylistSongs()
    playlist.insertAll(favourite_songs)
    return playlist


def __get_favourite_ids() -> list[str]:
    if os.path.exists(favourite_path):
        return Jsons.read_from_file(favourite_path) or []
    Jsons.write_to_file(favourite_path, [])
    return []


def get_songs_from_files(directory, file_path, with_extension):
    playlist = PlaylistSongs()
    getLogger().setLevel("ERROR")
    files: set = Files.get_files_from(directory, with_extension)
    for file in files:
        playlist.insert(Song.from_file(location=file))
    songs: list[Song] = playlist.get_songs()
    write_songs_to_file(file_path, songs)
    return playlist


def write_songs_to_file(file_path, songs):
    Jsons.write_to_file(file_path, [dict_of(song) for song in songs])


def dict_of(obj: any) -> dict:
    return dict((key, value) for key, value in obj.__dict__.items() if
                not callable(value) and
                not key.startswith('__') and
                not isinstance(value, bytes))


def get_songs_from_json(file_path) -> PlaylistSongs:
    playlist = PlaylistSongs()
    songs: list[dict] = Jsons.read_from_file(file_path) or []
    for song in songs:
        playlist.insert(Song.from_json(song))
    return playlist


def like_song(song: Song) -> None:
    love_ids = __get_favourite_ids()
    if song.get_id() in love_ids:
        raise Exception("You have already liked this song.")
    love_ids.append(song.get_id())
    Jsons.write_to_file(favourite_path, love_ids)


def dislike_song(song: Song) -> None:
    love_ids = __get_favourite_ids()
    if song.get_id() not in love_ids:
        raise Exception("You haven't like this song.")
    love_ids.remove(song.get_id())
    Jsons.write_to_file(favourite_path, love_ids)
