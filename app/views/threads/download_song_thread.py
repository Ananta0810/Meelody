import os
from typing import Callable

import pytube.request
from PyQt5.QtCore import pyqtSignal, QThread
from pytube import YouTube, Stream

pytube.request.default_range_size = 128000


class DownloadSongThread(QThread):
    downloadSucceed = pyqtSignal(str)

    def __init__(self, ytb: YouTube, onDownloading: Callable[[int, int, int], None]) -> None:
        super().__init__()
        self.__ytb = ytb
        self.__onDownloading = onDownloading

    def run(self) -> None:
        self.__ytb.register_on_progress_callback(self.__onProgress)

        downloadedFile = self.__ytb.streams.filter(abr='160kbps', only_audio=True).last().download("library/download")
        base, ext = os.path.splitext(downloadedFile)
        newFile = base + '.mp3'
        os.rename(downloadedFile, newFile)
        self.downloadSucceed.emit(newFile)

    def __onProgress(self, stream: Stream, chunk: bytes, bytesRemaining: int) -> None:
        totalSize = stream.filesize
        bytesDownloaded = totalSize - bytesRemaining
        self.__onDownloading(bytesDownloaded, totalSize, 0)
