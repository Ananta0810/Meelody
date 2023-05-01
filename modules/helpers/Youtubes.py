from threading import Thread
from typing import Callable

from yt_dlp import YoutubeDL, DownloadError

from modules.helpers import Printers
from modules.helpers.types import Strings


def _clean_youtube_url(url: str) -> str:
    index = url.find("&list")
    if index != -1:
        url = url[:index]
    return url


class YoutubeDownloader:
    __on_download_success_fn: Callable[[str], None] = None
    __on_download_failed_fn: Callable[[str], None] = None

    def __init__(self, url: str):
        self.__url: str = _clean_youtube_url(url)
        self.__is_downloading: bool = False
        self.__percentage: float = 0
        self.__size: int = 0
        self.__downloaded_size: int = 0
        self.__remain_sec: int = 0
        self.__title: str = ""

    def is_downloading(self) -> bool:
        return self.__is_downloading

    def get_percentage(self) -> float:
        return self.__percentage

    def get_video_title(self) -> str:
        return self.__title

    def get_size(self) -> int:
        return self.__size

    def get_remain_seconds(self) -> int:
        return self.__remain_sec

    def get_downloaded_size(self) -> int:
        return self.__downloaded_size

    def extract_info(self) -> None:
        ydl_opts = {
            'quiet': True,
        }
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(self.__url, download=False)
                self.__title = info_dict.get("title", None)
        except DownloadError:
            raise ValueError("Your url is invalid. Please use a valid one.")

    def on_download_success(self, fn: Callable[[str], None]) -> None:
        self.__on_download_success_fn = fn

    def on_download_failed(self, fn: Callable[[str], None]) -> None:
        self.__on_download_failed_fn = fn

    def download_to(self, directory: str):
        ydl_opts = {
            'format': 'bestaudio/best',
            'progress_hooks': [self.__track_percentage],
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'outtmpl': directory + '/%(title)s.%(ext)s',
        }

        with YoutubeDL(ydl_opts) as ydl:
            self.__is_downloading = True
            Thread(target=lambda: self.__start_download(ydl, directory)).start()

    def __start_download(self, ydl: YoutubeDL, directory) -> None:
        try:
            ydl.extract_info(self.__url)
            self.__is_downloading = False
        except Exception as e:
            Printers.error(e)
            self.__is_downloading = False
            self.__on_download_failed_fn("Some error had occurred.\n Please retry again.")
            return
        path = Strings.get_full_path(directory.replace("\\", "/"), self.__title, ".mp3")
        self.__on_download_success_fn(path)

    def __track_percentage(self, info: dict) -> None:
        status = info['status']
        if status == 'downloading':
            self.__percentage = float(info['_percent_str'].replace('%', ''))
            self.__downloaded_size = info['downloaded_bytes']
            self.__size = info['total_bytes']
            self.__remain_sec = info['eta']
