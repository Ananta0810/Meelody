from threading import Thread

from yt_dlp import YoutubeDL


def _clean_youtube_url(url: str) -> str:
    index = url.find("&list")
    if index != -1:
        url = url[:index]
    return url


class YoutubeDownloader:

    def __init__(self):
        self.__is_downloading: bool = False
        self.__percentage: float = 0

    def is_downloading(self) -> bool:
        return self.__is_downloading

    def get_percentage(self) -> float:
        return self.__percentage

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
            self.__is_downloading = True
            Thread(target=lambda: self.__start_download(ydl, download_url)).start()

    def __start_download(self, ydl: YoutubeDL, download_url: str) -> None:
        try:
            ydl.extract_info(download_url)
            self.__is_downloading = False
        except Exception as e:
            print(e)
            self.__is_downloading = False

    def __track_percentage(self, info: dict) -> None:
        if info['status'] == 'downloading':
            self.__percentage = float(info['_percent_str'].replace('%', ''))
