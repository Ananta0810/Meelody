import os
from datetime import datetime
from typing import Callable

import pytube.request
from PyQt5.QtCore import pyqtSignal, QThread
from pytube import YouTube, Stream

pytube.request.default_range_size = 128000


class DownloadSongThread(QThread):
    downloadSucceed = pyqtSignal(str)
    loaded = pyqtSignal()

    def __init__(self, ytb: YouTube, onDownloading: Callable[[int, int, int], None]) -> None:
        super().__init__()
        self.__ytb = ytb
        self.__onDownloading = onDownloading
        self.__loaded = False

    def run(self) -> None:
        downloadStartTime = datetime.now()

        self.__ytb.register_on_progress_callback(lambda stream, chunk, bytesRemaining: self.__onProgress(stream, bytesRemaining, downloadStartTime))
        downloadedFile = self.__ytb.streams.filter(abr='160kbps', only_audio=True).last().download("library/download")

        base, ext = os.path.splitext(downloadedFile)
        newFile = base + '.mp3'
        os.rename(downloadedFile, newFile)
        self.downloadSucceed.emit(newFile)

    def __onProgress(self, stream: Stream, bytesRemaining: int, downloadStartTime: datetime) -> None:
        if not self.__loaded:
            self.__loaded = True
            self.loaded.emit()
            
        totalSize = stream.filesize
        bytesDownloaded = totalSize - bytesRemaining

        secondsSinceDownloadStart = (datetime.now() - downloadStartTime).total_seconds()
        speed = round(((bytesDownloaded / 1024) / 1024) / secondsSinceDownloadStart, 2)
        secondsLeft = int(round(((bytesRemaining / 1024) / 1024) / float(speed), 2))
        self.__onDownloading(bytesDownloaded, totalSize, secondsLeft)
