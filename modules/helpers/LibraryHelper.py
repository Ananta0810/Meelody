import os.path
from logging import getLogger

from modules.helpers.Files import Files
from modules.helpers.Jsons import Jsons
from modules.models.PlaylistInformation import PlaylistInformation
from modules.models.PlaylistSongs import PlaylistSongs
from modules.models.Song import Song

library_path: str = "library/library.json"
playlists_path: str = "library/playlists.json"


def load_songs_from_dir(directory: str, with_extension: str) -> PlaylistSongs:
    return get_library_songs_from_json(library_path) \
        if os.path.exists(library_path) \
        else get_songs_from_files(directory, library_path, with_extension)


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


def get_library_songs_from_json(file_path) -> PlaylistSongs:
    playlist = PlaylistSongs()
    songs: list[dict] = Jsons.read_from_file(file_path) or []
    for song in songs:
        playlist.insert(Song.from_json(song))
    return playlist


def dict_of(obj: any) -> dict:
    return dict((key, value) for key, value in obj.__dict__.items() if
                not callable(value) and
                not key.startswith('__') and
                not isinstance(value, bytes))


def update_love_state_of(song: Song) -> None:
    playlist = get_library_songs_from_json(library_path)
    saved_song = playlist.get_song_at(playlist.index_of(song))
    saved_song.set_love_state(song.is_loved())
    write_songs_to_file(library_path, playlist.get_songs())


def load_playlists() -> list[PlaylistInformation]:
    return get_library_playlists_from_json(playlists_path) \
        if os.path.exists(playlists_path) \
        else _create_empty_playlist(playlists_path)


def _create_empty_playlist(file_path: str) -> list[PlaylistInformation]:
    write_playlists_to_file([], file_path)
    return []


def write_playlists_to_file(playlists, file_path) -> None:
    data = [dict_of(playlist) for playlist in playlists]
    Jsons.write_to_file(file_path, data)


def save_playlists(playlists) -> None:
    write_playlists_to_file(playlists, playlists_path)


def get_library_playlists_from_json(file_path) -> list[PlaylistInformation]:
    playlists: list[dict] = Jsons.read_from_file(file_path) or []
    return [PlaylistInformation.from_json(playlist) for playlist in playlists]


def dict_of(obj: any) -> dict:
    return dict((key, value) for key, value in obj.__dict__.items() if
                not callable(value) and
                not key.startswith('__') and
                not isinstance(value, bytes) and
                not isinstance(value, bytearray)
                )
