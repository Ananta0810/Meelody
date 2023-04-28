from os import path, scandir
from shutil import copyfile

from yt_dlp import YoutubeDL

from modules.helpers.types.Strings import Strings


class Files:
    @staticmethod
    def get_files_from(directory: str, with_extension: str) -> set[str]:
        while directory.endswith("/"):
            directory = directory[:-1]
        scanned_files = scandir(directory)

        return {Strings.join_path(directory, file.name) for file in scanned_files if file.name.endswith(with_extension)}

    @staticmethod
    def copy_file(file: str, to_directory: str) -> str:
        destiny = "/".join([to_directory, Strings.get_filename(file)])
        if path.exists(destiny):
            raise FileExistsError(f"{destiny} already existed.")
        copyfile(file, destiny)
        return destiny


class Youtubes:
    @staticmethod
    def clean_youtube_url(url: str):
        index = url.find("&list")
        if index != -1:
            url = url[:index]
        return url

    @staticmethod
    def download_songs_from_youtube(youtube_url: str, to_directory: str):
        download_url = Youtubes.clean_youtube_url(youtube_url)
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': to_directory + '/%(title)s.%(ext)s',
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(download_url)
