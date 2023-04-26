import logging
import os.path
from logging import getLogger

from modules.helpers.Files import Files
from modules.helpers.Jsons import Jsons
from modules.models.Playlist import Playlist, PlaylistJson
from modules.models.PlaylistSongs import PlaylistSongs
from modules.models.Song import Song

library_path: str = "library/library.json"
playlists_path: str = "library/playlists.json"


def load_songs_from_dir(directory: str, with_extension: str) -> PlaylistSongs:
    return get_library_songs_from_json(library_path) \
        if os.path.exists(library_path) \
        else get_songs_from_files(directory, library_path, with_extension)


def get_songs_from_files(directory: str, file_path: str, with_extension: str) -> PlaylistSongs:
    playlist = PlaylistSongs()
    getLogger().setLevel("ERROR")
    files: set = Files.get_files_from(directory, with_extension)
    for file in files:
        playlist.insert(Song.from_file(location=file))
    songs: list[Song] = playlist.get_songs()
    write_songs_to_file(file_path, songs)
    return playlist


def write_songs_to_file(file_path: str, songs: list[Song]) -> None:
    Jsons.write_to_file(file_path, [song.to_dict() for song in songs])


def get_library_songs_from_json(file_path: str) -> PlaylistSongs:
    playlist = PlaylistSongs()
    songs: list[dict] = Jsons.read_from_file(file_path) or []
    for song in songs:
        try:
            playlist.insert(Song.from_json(song))
        except KeyError:
            print("Extract song from json failed.")
            pass
    return playlist


def update_love_state_of(song: Song) -> None:
    playlist = get_library_songs_from_json(library_path)
    saved_song = playlist.get_song_at(playlist.index_of(song))
    saved_song.set_love_state(song.is_loved())
    write_songs_to_file(library_path, playlist.get_songs())


def load_playlists(songs: list[Song]) -> list[Playlist]:
    return get_library_playlists_from_json(playlists_path, songs) \
        if os.path.exists(playlists_path) \
        else _create_empty_playlist(playlists_path)


def _create_empty_playlist(file_path: str) -> list[Playlist]:
    write_playlists_to_file([], file_path)
    return []


def write_playlists_to_file(playlists: list[Playlist], file_path: str) -> None:
    playlist_jsons: list[PlaylistJson] = [PlaylistJson.from_playlist(playlist) for playlist in playlists]
    data = [playlist.to_json() for playlist in playlist_jsons]
    Jsons.write_to_file(file_path, data)


def save_playlists(playlists: list[Playlist]) -> None:
    write_playlists_to_file(playlists, playlists_path)


def get_library_playlists_from_json(file_path: str, songs: list[Song]) -> list[Playlist]:
    playlists: list[dict] = Jsons.read_from_file(file_path) or []
    try:
        return [PlaylistJson.from_json(playlist).to_playlist(songs) for playlist in playlists]
    except KeyError:
        print("Extract song from json failed.")
        return []
