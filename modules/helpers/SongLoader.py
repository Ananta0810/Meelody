import os
import tempfile
from threading import Thread

from modules.helpers import Commands
from modules.helpers.Files import Files
from modules.helpers.types.Metas import SingletonMeta
from modules.helpers.types.Strings import Strings
from modules.models.Song import Song


class SongLoader(metaclass=SingletonMeta):
    __songs: list[Song] = []
    __STANDARD_SAMPLE_RATE: float = 48000

    def add_song(self, song: Song) -> None:
        if song.get_sample_rate() == SongLoader.__STANDARD_SAMPLE_RATE:
            return

        if os.path.exists(self.__temp_audio_of(song)):
            return

        self.__songs.append(song)

    def resolve_load_locations(self) -> None:
        Thread(target=lambda: self.__resolve()).start()

    def __resolve(self):
        if len(self.__songs) == 0:
            return

        with tempfile.TemporaryDirectory() as temp_dir:
            for song in self.__songs:
                print(f"Resolving load location for song {song.get_title()}")
                try:
                    if not Strings.is_ascii(song.get_title()):
                        self.__create_temp_file_and_change_its_sample_rate(song, temp_dir)
                        return
                    self.__create_changed_sample_rate_song(song)
                except Commands.CommandFailedError:
                    print("Some error occurred.")

    def __create_changed_sample_rate_song(self, song):
        original_location = song.get_location()
        target_location = self.__temp_audio_of(song)
        self.__create_file_with_standard_sample_rate(song, original_location, target_location)

    def __create_temp_file_and_change_its_sample_rate(self, song: Song, temp_dir: str) -> None:
        """
            When we run command, sometimes file name will be changed because shell can not write punctuation.
            Therefore, we have to create a file in which name has no punctuation.
        """
        new_name = Strings.clear_non_ascii(song.get_title())
        temp_file_without_punctuation_in_name = Strings.get_full_path(
            directory=temp_dir,
            name=new_name,
            extension="." + Strings.extension_of(song.get_location())
        )

        try:
            Files.copy(src=song.get_location(), destiny=temp_file_without_punctuation_in_name)
        except FileExistsError:
            pass

        audio_location = self.__temp_audio_of(song)
        self.__create_file_with_standard_sample_rate(song, temp_file_without_punctuation_in_name, audio_location)

    @staticmethod
    def __create_file_with_standard_sample_rate(song, original_location: str, audio_location: str) -> None:
        if os.path.exists(audio_location):
            song.set_audio_location(audio_location)
            return
        Commands.run_commands(['cd tools/sox',
                               f'sox "{os.path.abspath(original_location)}" -r 48000 "{os.path.abspath(audio_location)}"'])
        song.set_audio_location(audio_location)
        print(f"Created temp song at {audio_location}.")

    @staticmethod
    def __temp_audio_of(song: Song) -> str:
        return Strings.rename_file(song.get_location(), 'temp/' + Strings.clear_non_ascii(song.get_title()))
