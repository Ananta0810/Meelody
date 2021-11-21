from io import BytesIO
from os import path, scandir
from shutil import copyfile

from common_types.my_string import UnicodeString


class MyFile:
    @staticmethod
    def generate_path(dir: str, name: str, extension: str) -> str:
        return "".join([dir, "/", name, extension])

    @staticmethod
    def get_filename(your_path: str):
        return your_path.split("/")[-1]

    @staticmethod
    def get_dir_from(your_path: str) -> str:
        return your_path.replace(path.basename(your_path), "")

    @staticmethod
    def get_basename(your_path: str) -> str:
        return path.basename(your_path).split(".")[0]

    @staticmethod
    def get_file_extension(your_path: str) -> str:
        return path.splitext(your_path)[1]

    @staticmethod
    def get_files_from(dir: str, with_extension: str) -> list:
        while dir.endswith("/"):
            dir = dir[:-1]
        files = scandir(dir)
        files = sorted(
            files, key=lambda x: UnicodeString.to_lower(x.name.rsplit(".", 1)[0])
        )

        your_files = [
            "/".join([dir, file.name])
            for file in files
            if file.name.endswith(with_extension)
        ]
        return your_files

    @staticmethod
    def move_file(file: str, destiny_dir: str) -> str:
        new_file_path = "/".join([destiny_dir, MyFile.get_filename(file)])
        if path.exists(new_file_path):
            return
        copyfile(file, new_file_path)
        return new_file_path

    # @staticmethod
    # def download_audio(your_link, download_dir):
    #     print(your_link)

    #     if download_dir != "" and download_dir[-1] != "/":
    #         download_dir += "/"
    #     ydl_opts = {
    #         "format": "bestaudio/best",
    #         "postprocessors": [
    #             {
    #                 "key": "FFmpegExtractAudio",
    #                 "preferredcodec": "mp3",
    #                 "preferredquality": "192",
    #             }
    #         ],
    #         "outtmpl": download_dir + "%(title)s.%(ext)s",
    #     }

    #     with YoutubeDL(ydl_opts) as ydl:
    #         info_dict = ydl.extract_info(your_link, download=False)
    #         video_title = info_dict.get("title", None)

    #     video_title = sub(r"[^A-Za-z0-9 ]+", "", video_title)
    #     video_file = "".join([download_dir, video_title, ".mp3"])

    #     ydl_opts.update({"outtmpl": video_file})

    #     with YoutubeDL(ydl_opts) as ydl:
    #         info_dict = ydl.extract_info(your_link)
    #     print(f'Download "{video_title}"successfully')
    #     return video_file
