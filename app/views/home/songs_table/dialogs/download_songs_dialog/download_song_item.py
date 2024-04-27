import os
from typing import Optional, Callable

import pytube.request
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QLabel
from pytube import YouTube, Stream

from app.components.base import Cover, LabelWithDefaultText, Factory, CoverProps
from app.components.sliders import ProgressBar
from app.components.widgets import ExtendableStyleWidget
from app.helpers.others import Times
from app.resource.qt import Images


class DownloadSongItem(ExtendableStyleWidget):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._initComponent()

        self._dot: float = 0
        self._frame: int = 0
        self.setProgress(0)

    def _createUI(self) -> None:
        self._cover = Cover()
        self._cover.setFixedSize(48, 48)
        self._cover.setCover(CoverProps.fromBytes(Images.DEFAULT_SONG_COVER, width=48, height=48, radius=8))

        self._titleLabel = LabelWithDefaultText()
        self._titleLabel.setFont(Factory.createFont(size=10, bold=True))
        self._titleLabel.setClassName("text-black dark:text-white")

        self._descriptionLabel = LabelWithDefaultText()
        self._descriptionLabel.setFont(Factory.createFont(size=9))
        self._descriptionLabel.setClassName("text-black dark:text-white")

        self._progressBar = ProgressBar()
        self._progressBar.setFixedHeight(2)
        self._progressBar.setClassName("rounded-1 bg-primary")

        self._infoLayout = QVBoxLayout()
        self._infoLayout.setContentsMargins(0, 0, 0, 0)
        self._infoLayout.setSpacing(4)
        self._infoLayout.addStretch(0)
        self._infoLayout.addWidget(self._titleLabel)
        self._infoLayout.addWidget(self._descriptionLabel)
        self._infoLayout.addWidget(self._progressBar)
        self._infoLayout.addStretch(0)

        # self._resultIcon = Factory.createMultiStatesButton(size=Icons.SMALL, padding=Paddings.RELATIVE_25)
        # self._resultIcon.setIcons([StateIcon(Icons.APPLY.withColor(Colors.WHITE)), StateIcon(Icons.CLOSE.withColor(Colors.WHITE))])
        # self._resultIcon.keepSpaceWhenHiding()
        # self._resultIcon.hide()

        self._gif = QLabel()
        self._gif.setFixedSize(48, 48)
        movie = QMovie("app/resource/images/defaults/loading.gif")
        movie.setScaledSize(QSize(48, 48))
        self._gif.setMovie(movie)
        self._icons = QWidget()

        self._iconsLayout = QVBoxLayout(self._icons)
        self._iconsLayout.addWidget(self._gif)
        # self._iconsLayout.addWidget(self._resultIcon)

        self._mainLayout = QHBoxLayout()
        self._mainLayout.setSpacing(0)
        self._mainLayout.setSpacing(0)
        self._mainLayout.setAlignment(Qt.AlignLeft)

        self._mainLayout.addWidget(self._cover)
        self._mainLayout.addSpacing(12)
        self._mainLayout.addLayout(self._infoLayout, stretch=1)
        self._mainLayout.addWidget(self._icons)

        self.setLayout(self._mainLayout)

    def show(self) -> None:
        super().show()

    def setTitle(self, label: str) -> None:
        self._titleLabel.setText(label)

    def setDescription(self, value: str) -> None:
        self._descriptionLabel.setText(value)

    def setProgress(self, value: float) -> None:
        self._progressBar.setValue(value)

    def applyLightMode(self) -> None:
        super().applyLightMode()
        super().applyThemeToChildren()

    def applyDarkMode(self) -> None:
        super().applyDarkMode()
        super().applyThemeToChildren()

    def download(self, url: str) -> None:
        yt = YouTube(url)

        self.setTitle(yt.title)

        downloadSongThread = DownloadSongThread(yt, onDownloading=self.onDownloading)
        downloadSongThread.downloadSucceed.connect(lambda path: self.markSucceed())
        downloadSongThread.start()

    def onDownloading(self, bytesDownloaded: int, totalSize: int, estimateTime: int) -> None:
        percentage = bytesDownloaded / totalSize * 100
        description = f"{percentage}%   |   {bytesDownloaded}/{totalSize}MB   |  estimate: {Times.toString(estimateTime)}"

        self.setDescription(description)
        self._gif.movie().jumpToNextFrame()

    def markSucceed(self) -> None:
        # self._resultIcon.show()
        # self._resultIcon.setActiveState(0)
        self._gif.setFixedSize(0, 0)
        self._iconsLayout.addSpacing(24)
        self._gif.movie().stop()
        self._gif.hide()
        self._descriptionLabel.setText("Download Succeed.")


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
        self.__onDownloading(totalSize, bytesDownloaded, 0)
