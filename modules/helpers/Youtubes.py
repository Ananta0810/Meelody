from threading import Thread

from yt_dlp import YoutubeDL

from modules.helpers import Printers


def _clean_youtube_url(url: str) -> str:
    index = url.find("&list")
    if index != -1:
        url = url[:index]
    return url


class YoutubeDownloader:

    def __init__(self):
        self.__is_downloading: bool = False
        self.__download_success: bool = False
        self.__percentage: float = 0
        self.__size: int = 0
        self.__downloaded_size: int = 0
        self.__remain_sec: int = 0
        self.__title: str = ""
        self.__error_message: str = ""

    def is_downloading(self) -> bool:
        return self.__is_downloading

    def is_success(self) -> bool:
        return self.__download_success

    def get_error_message(self) -> str:
        return self.__error_message

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

    def download_from(self, youtube_url: str, to_directory: str):
        download_url = _clean_youtube_url(youtube_url)
        ydl_opts = {
            'format': 'bestaudio/best',
            'progress_hooks': [self.__track_percentage],
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'outtmpl': to_directory + '/%(title)s.%(ext)s',
        }

        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(download_url, download=False)
            self.__title = info_dict.get("title", None)
            self.__is_downloading = True
            Thread(target=lambda: self.__start_download(ydl, download_url)).start()

    def __start_download(self, ydl: YoutubeDL, download_url: str) -> None:
        try:
            ydl.extract_info(download_url)
            self.__is_downloading = False
            self.__download_success = True
        except Exception as e:
            Printers.error(e)
            self.__download_success = False
            self.__is_downloading = False
            error = str(e)
            if 'is not a valid URL' in error:
                self.__error_message = f"Your url is invalid. Please use a valid one."
            else:
                self.__error_message = "Some error had occurred.\n Please retry again."

    def __track_percentage(self, info: dict) -> None:
        status = info['status']
        if status == 'downloading':
            self.__percentage = float(info['_percent_str'].replace('%', ''))
            self.__downloaded_size = info['downloaded_bytes']
            self.__size = info['total_bytes']
            self.__remain_sec = info['eta']
