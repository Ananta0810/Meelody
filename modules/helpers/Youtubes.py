from threading import Thread
from typing import Callable

from yt_dlp import YoutubeDL, DownloadError

from modules.helpers import Printers
from modules.helpers.types import Strings, Numbers


def _clean_youtube_url(url: str) -> str:
    index = url.find("&list")
    if index != -1:
        url = url[:index]
    return url


_init = 0
_downloading = 1
_processing = 2
_succeed = 3
_failed = 4


class YoutubeDownloader:
    __on_succeed_fn: Callable[[str], None] = None
    __on_failed_fn: Callable[[str], None] = None

    def __init__(self, url: str):
        self.__url: str = _clean_youtube_url(url)
        self.__state: int = _init
        self.__percentage: float = 0
        self.__size: int = 0
        self.__downloaded_size: int = 0
        self.__remain_sec: int = 0
        self.__title: str = ""

    def is_downloading(self) -> bool:
        return self.__state == _downloading

    def is_processing(self) -> bool:
        return self.__state == _processing

    def is_finished(self) -> bool:
        return self.__state == _succeed or self.__state == _failed

    def is_started(self) -> bool:
        return self.__state == _init

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
                self.__title = Strings.clean_name(info_dict.get("title", None))
        except DownloadError:
            raise ValueError("Your url is invalid. Please use a valid one.")

    def on_succeed(self, fn: Callable[[str], None]) -> None:
        self.__on_succeed_fn = fn

    def on_failed(self, fn: Callable[[str], None]) -> None:
        self.__on_failed_fn = fn

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
            'outtmpl': "".join([directory, '/', self.__title]),
        }

        with YoutubeDL(ydl_opts) as ydl:
            Thread(target=lambda: self.__start_download(ydl, directory)).start()

    def __start_download(self, ydl: YoutubeDL, directory) -> None:
        try:
            self.__state = _downloading
            ydl.extract_info(self.__url)
        except Exception as e:
            Printers.error(e)
            self.__state = _failed
            self.__on_failed_fn("Some error had occurred.\n Please retry again.")
            return

        path = Strings.get_full_path(directory.replace("\\", "/"), self.__title, ".mp3")
        self.__on_succeed_fn(path)
        self.__state = _succeed

    def __track_percentage(self, info: dict) -> None:
        status = info['status']
        if status == 'downloading':
            try:
                self.__state = _downloading
                self.__downloaded_size = info['downloaded_bytes']
                self.__size = info['total_bytes']
                self.__remain_sec = info['eta']
                self.__percentage = Numbers.clamp(self.__downloaded_size / self.__size * 100, 0, 100)
            except:
                pass
            return
        if status == 'finished':
            self.__state = _processing
