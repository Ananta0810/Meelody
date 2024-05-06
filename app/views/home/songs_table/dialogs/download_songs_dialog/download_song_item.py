import io
import os
from contextlib import suppress
from datetime import datetime
from typing import Callable
from typing import Optional

import pytube.request
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from pytube import YouTube, Stream

from app.common.exceptions import ResourceException
from app.common.models import Song
from app.components.base import Cover, LabelWithDefaultText, Factory, CoverProps
from app.components.base.gif import Gif
from app.components.sliders import ProgressBar
from app.components.widgets import ExtendableStyleWidget, Box, FlexBox
from app.helpers.base import Strings
from app.helpers.builders import AudioEditor
from app.helpers.others import Times, Files, Logger
from app.helpers.stylesheets import Paddings, Colors
from app.resource.qt import Images, Icons
from app.views.threads import UpdateUIThread


class DownloadSongItem(ExtendableStyleWidget):
    songDownloaded = pyqtSignal(Song)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._initComponent()

        self._dot: float = 0
        self.setProgress(0)

    def _createUI(self) -> None:
        self.setContentsMargins(0, 0, 0, 0)

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

        self._infoLayout = Box()
        self._infoLayout.setSpacing(4)
        self._infoLayout.addStretch(0)
        self._infoLayout.addWidget(self._titleLabel)
        self._infoLayout.addWidget(self._descriptionLabel)
        self._infoLayout.addWidget(self._progressBar)
        self._infoLayout.addStretch(0)

        self._successIcon = Factory.createIconButton(size=Icons.SMALL, padding=Paddings.RELATIVE_25)
        self._successIcon.setLightModeIcon(Icons.APPLY.withColor(Colors.WHITE))
        self._successIcon.setClassName("rounded-full bg-success")
        self._successIcon.hide()

        self._failedIcon = Factory.createIconButton(size=Icons.SMALL, padding=Paddings.RELATIVE_25)
        self._failedIcon.setLightModeIcon(Icons.CLOSE.withColor(Colors.WHITE))
        self._failedIcon.setClassName("rounded-full bg-danger")
        self._failedIcon.hide()

        self._downloadLabel = Gif("app/resource/images/defaults/downloading.gif")
        self._downloadLabel.setFixedSize(48, 48)
        self._downloadLabel.setGifSize(32)
        self._downloadLabel.hide()

        self._convertingLabel = Gif("app/resource/images/defaults/loading-bubble.gif")
        self._convertingLabel.setFixedSize(48, 48)
        self._convertingLabel.hide()

        self._icons = QWidget()
        self._icons.setFixedWidth(48)

        self._iconsLayout = QHBoxLayout(self._icons)
        self._iconsLayout.setAlignment(Qt.AlignRight)
        self._iconsLayout.addWidget(self._downloadLabel)
        self._iconsLayout.addWidget(self._convertingLabel)
        self._iconsLayout.addWidget(self._successIcon)
        self._iconsLayout.addWidget(self._failedIcon)

        self._mainLayout = FlexBox()
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

    def download(self, yt: YouTube, title: str, artist: str) -> None:
        self.setTitle(Strings.join(" | ", [title, artist if Strings.isNotBlank(artist) else None]))

        downloadSongThread = DownloadSongThread(yt, onDownloading=self.__onDownloading)
        loadingAnimationThread = UpdateUIThread(action=lambda: self.__onLoading(), interval=250)

        downloadSongThread.loaded.connect(lambda: loadingAnimationThread.quit())
        downloadSongThread.loaded.connect(lambda: self._downloadLabel.show())
        downloadSongThread.loaded.connect(lambda: self._downloadLabel.start())

        downloadSongThread.succeed.connect(lambda data: self.setProgress(100))
        downloadSongThread.succeed.connect(lambda data: self._downloadLabel.hide())
        downloadSongThread.succeed.connect(lambda data: loadingAnimationThread.quit())
        downloadSongThread.succeed.connect(lambda data: self._downloadLabel.stop())
        downloadSongThread.succeed.connect(lambda data: self.__createSong(data, title, artist))

        downloadSongThread.failed.connect(lambda data: self._downloadLabel.hide())
        downloadSongThread.failed.connect(lambda exception: loadingAnimationThread.quit())
        downloadSongThread.failed.connect(lambda exception: self._downloadLabel.stop())
        downloadSongThread.failed.connect(lambda exception: self.__markDownloadFailed(exception))

        downloadSongThread.start()
        loadingAnimationThread.start()

    def __createSong(self, data: io.BytesIO, title: str, artist: str) -> None:
        self._dot = 0
        self._convertingLabel.show()

        textAnimationThread = UpdateUIThread(action=lambda: self.__onConverting(), interval=250)

        self._convertingLabel.start()
        textAnimationThread.start()

        thread = ConvertSongThread(data, title, artist)

        thread.succeed.connect(lambda: self._convertingLabel.stop())
        thread.succeed.connect(lambda: textAnimationThread.quit())
        thread.succeed.connect(lambda: self.__markSucceed())
        thread.succeed.connect(lambda song: self.__notifySongDownloaded(song))

        thread.failed.connect(lambda: self._convertingLabel.stop())
        thread.failed.connect(lambda: textAnimationThread.quit())
        thread.failed.connect(lambda e: self.__markConvertFailed(e))

        thread.start()

    def __notifySongDownloaded(self, song: Song) -> None:
        # Somehow, I need to add this method to work.
        return self.songDownloaded.emit(song)

    def __updateConvertingAnimation(self) -> None:
        if self._convertingLabel.isVisible():
            self._convertingLabel.movie().jumpToNextFrame()

    def __onLoading(self) -> None:
        self._descriptionLabel.setText(f"Loading{int(self._dot) * '.'}")
        self._dot = (self._dot + 1) % 4

    def __onConverting(self) -> None:
        self._descriptionLabel.setText(f"Converting{int(self._dot) * '.'}")
        self._dot = (self._dot + 1) % 4

    def __onDownloading(self, bytesDownloaded: int, totalSize: int, estimateTime: int) -> None:
        percentage = bytesDownloaded * 100 / totalSize
        downloadedStr = Strings.convertBytes(bytesDownloaded)
        totalStr = Strings.convertBytes(totalSize)

        description = f"{int(percentage)}%  |  {downloadedStr}/{totalStr}  |  estimate: {Times.toString(estimateTime)}"
        self.setProgress(percentage)
        self.setDescription(description)

    def __markSucceed(self) -> None:
        self._downloadLabel.hide()
        self._convertingLabel.hide()
        self._successIcon.show()
        self._descriptionLabel.setText("Download Succeed.")

    def __markDownloadFailed(self, exception: Exception) -> None:
        self._downloadLabel.hide()
        self._convertingLabel.hide()
        self._failedIcon.show()
        if isinstance(exception, FileExistsError):
            self._descriptionLabel.setText("Download failed. Song is already existed.")
        else:
            self._descriptionLabel.setText("Download failed.")

    def __markConvertFailed(self, exception: Exception) -> None:
        self._downloadLabel.hide()
        self._convertingLabel.hide()
        self._failedIcon.show()

        if isinstance(exception, FileExistsError):
            self._descriptionLabel.setText("Convert failed. Song is already existed.")
            return

        if isinstance(exception, ResourceException):
            self._descriptionLabel.setText("Convert failed. Song is broken.")
            return

        self._descriptionLabel.setText("Convert failed. Please try again.")


pytube.request.default_range_size = 128000


class DownloadSongThread(QThread):
    loaded = pyqtSignal()
    succeed = pyqtSignal(io.BytesIO)
    failed = pyqtSignal(Exception)

    def __init__(self, ytb: YouTube, onDownloading: Callable[[int, int, int], None]) -> None:
        super().__init__()
        self.__ytb = ytb
        self.__onDownloading = onDownloading
        self.__loaded = False

    def run(self) -> None:
        try:
            downloadStartTime = datetime.now()

            self.__ytb.register_on_progress_callback(
                lambda stream, chunk, bytesRemaining: self.__onProgress(stream, bytesRemaining, downloadStartTime))

            audioBytes = io.BytesIO()
            self.__ytb.streams.get_audio_only().stream_to_buffer(audioBytes)
            self.succeed.emit(audioBytes)
        except Exception as e:
            self.failed.emit(e)

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


class ConvertSongThread(QThread):
    succeed = pyqtSignal(Song)
    failed = pyqtSignal(Exception)

    def __init__(self, songData: io.BytesIO, title: str, artist: str) -> None:
        super().__init__()
        self.__songData = songData
        self.__title = title
        self.__artist = artist

    def run(self) -> None:
        songLocation = f"library/{Strings.sanitizeFileName(self.__title)}.mp3"
        if os.path.exists(songLocation):
            self.failed.emit(FileExistsError())
            Logger.error(f"Can't convert song '{self.__title}' because it is already existed in library.")
            return
        try:
            editor = AudioEditor()
            editor.toMp3FileFromBytes(self.__songData, songLocation)
            song = Song.fromFile(songLocation, self.__title)

            if Strings.isNotBlank(self.__artist):
                try:
                    song.updateInfo(self.__title, self.__artist)
                except AttributeError:
                    raise ResourceException.brokenFile()

            Logger.info(f"Download song '{self.__title}' successfully")
            self.succeed.emit(song)

        except ResourceException as e:
            Logger.error(f"Can't convert song '{self.__title}' because it is broken.")
            Files.removeFile(songLocation)
            self.failed.emit(e)

        except Exception as e:
            Logger.error(f"Convert song '{self.__title}' failed  with following error: {e}")
            Files.removeFile(songLocation)
            self.failed.emit(e)

        # Clean up after downloaded, even if it is successfully.
        with suppress(Exception):
            self.__songData.close()
