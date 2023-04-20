import os.path
from logging import getLogger

from modules.helpers.Files import Files
from modules.helpers.Jsons import Jsons
from modules.models.PlaylistSongs import PlaylistSongs
from modules.models.Song import Song


def load_songs_from_dir(directory: str, with_extension: str) -> PlaylistSongs:
    file_path: str = "library/songs.json"

    return get_songs_from_json(file_path) if os.path.exists(file_path) else get_songs_from_files(directory, file_path,
                                                                                                 with_extension)


def get_songs_from_files(directory, file_path, with_extension):
    playlist = PlaylistSongs()
    getLogger().setLevel("ERROR")
    files: set = Files.get_files_from(directory, with_extension)
    for file in files:
        playlist.insert(Song.from_file(location=file))
    songs: list[Song] = playlist.get_songs()
    Jsons.write_to_file(file_path, [dict_of(song) for song in songs])
    return playlist


def dict_of(obj: any) -> dict:
    return dict((key, value) for key, value in obj.__dict__.items() if
                not callable(value) and
                not key.startswith('__') and
                not isinstance(value, bytes))


def get_songs_from_json(file_path):
    playlist = PlaylistSongs()
    songs: list[dict] = Jsons.read_from_file(file_path) or []
    for song in songs:
        playlist.insert(Song.from_json(song))
    return playlist
