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
from app.common.others import translator
from app.common.statics.qt import Images, Icons, Cursors
from app.common.statics.styles import Colors
from app.common.statics.styles import Paddings
from app.components.base import FontFactory
from app.components.buttons import ButtonFactory
from app.components.images import Cover
from app.components.images.gif import Gif
from app.components.labels import AutoTranslateLabel
from app.components.labels.ellipsis_label import EllipsisLabel
from app.components.sliders import ProgressBar
from app.components.threads import UpdateUIThread
from app.components.widgets import ExtendableStyleWidget, Box, FlexBox
from app.helpers.base import Strings
from app.helpers.builders import AudioEditor
from app.helpers.others import Times, Files, Logger


class DownloadSongItem(ExtendableStyleWidget):
    songDownloaded = pyqtSignal(str)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._initComponent()

        self._dot: float = 0
        self.setProgress(0)

    def _createUI(self) -> None:
        self.setContentsMargins(0, 0, 0, 0)

        self._cover = Cover()
        self._cover.setFixedSize(48, 48)
        self._cover.setCover(Cover.Props.fromBytes(Images.defaultSongCover, width=48, height=48, radius=8))

        self._titleLabel = EllipsisLabel()
        self._titleLabel.setFont(FontFactory.create(size=10, bold=True))
        self._titleLabel.setClassName("text-black dark:text-white")

        self._descriptionLabel = AutoTranslateLabel()
        self._descriptionLabel.setFont(FontFactory.create(size=9))
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

        self._successIcon = ButtonFactory.createIconButton(size=Icons.small, padding=Paddings.RELATIVE_25)
        self._successIcon.setLightModeIcon(Icons.apply.withColor(Colors.white))
        self._successIcon.setClassName("rounded-full bg-success")
        self._successIcon.setCursor(Cursors.base)
        self._successIcon.hide()

        self._failedIcon = ButtonFactory.createIconButton(size=Icons.small, padding=Paddings.RELATIVE_25)
        self._failedIcon.setLightModeIcon(Icons.close.withColor(Colors.white))
        self._failedIcon.setClassName("rounded-full bg-danger")
        self._failedIcon.setCursor(Cursors.base)
        self._failedIcon.hide()

        self._downloadLabel = Gif("resource/images/defaults/downloading.gif")
        self._downloadLabel.setFixedSize(48, 48)
        self._downloadLabel.setGifSize(32)
        self._downloadLabel.setCursor(Cursors.base)
        self._downloadLabel.hide()

        self._convertingLabel = Gif("resource/images/defaults/loading-bubble.gif")
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

    def setProgress(self, value: float) -> None:
        self._progressBar.setValue(value)

    def applyLightMode(self) -> None:
        super().applyLightMode()
        super().applyThemeToChildren()

    def applyDarkMode(self) -> None:
        super().applyDarkMode()
        super().applyThemeToChildren()

    def download(self, yt: YouTube, title: str, artist: str) -> None:
        self._titleLabel.setText(Strings.join(" | ", [title, artist if Strings.isNotBlank(artist) else None]))

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
        thread.succeed.connect(lambda path: self.songDownloaded.emit(path))

        thread.failed.connect(lambda: self._convertingLabel.stop())
        thread.failed.connect(lambda: textAnimationThread.quit())
        thread.failed.connect(lambda e: self.__markConvertFailed(e))

        thread.start()

    def __updateConvertingAnimation(self) -> None:
        if self._convertingLabel.isVisible():
            self._convertingLabel.movie().jumpToNextFrame()

    def __onLoading(self) -> None:
        self._descriptionLabel.setText(f"{translator.translate('DOWNLOAD_DIALOG.LOADING')}{int(self._dot) * '.'}")
        self._dot = (self._dot + 1) % 4

    def __onConverting(self) -> None:
        self._descriptionLabel.setText(f"{translator.translate('DOWNLOAD_DIALOG.CONVERTING')}{int(self._dot) * '.'}")
        self._dot = (self._dot + 1) % 4

    def __onDownloading(self, bytesDownloaded: int, totalSize: int, estimateTime: int) -> None:
        percentage = bytesDownloaded * 100 / totalSize
        downloadedStr = Strings.convertBytes(bytesDownloaded)
        totalStr = Strings.convertBytes(totalSize)

        estimateText = translator.translate('DOWNLOAD_DIALOG.ESTIMATE')
        description = f"{int(percentage)}%  |  {downloadedStr}/{totalStr}  |  {estimateText}: {Times.toString(estimateTime)}"
        self.setProgress(percentage)
        self._descriptionLabel.setText(description)

    def __markSucceed(self) -> None:
        self._downloadLabel.hide()
        self._convertingLabel.hide()
        self._successIcon.show()

        self._descriptionLabel.setTranslateText("DOWNLOAD_DIALOG.DOWNLOAD_SUCCEED")

    def __markDownloadFailed(self, exception: Exception) -> None:
        self._downloadLabel.hide()
        self._convertingLabel.hide()
        self._failedIcon.show()
        if isinstance(exception, FileExistsError):
            self._descriptionLabel.setTranslateText("DOWNLOAD_DIALOG.DOWNLOAD_FAILED_EXISTED")
        else:
            self._descriptionLabel.setTranslateText("DOWNLOAD_DIALOG.DOWNLOAD_FAILED")

    def __markConvertFailed(self, exception: Exception) -> None:
        self._downloadLabel.hide()
        self._convertingLabel.hide()
        self._failedIcon.show()

        if isinstance(exception, FileExistsError):
            self._descriptionLabel.setTranslateText("DOWNLOAD_DIALOG.CONVERT_FAILED_EXISTED")
            return

        if isinstance(exception, ResourceException):
            if exception.isExisted():
                self._descriptionLabel.setTranslateText("DOWNLOAD_DIALOG.CONVERT_FAILED_EXISTED")
                return

            if exception.isBroken():
                self._descriptionLabel.setTranslateText("DOWNLOAD_DIALOG.CONVERT_FAILED_BROKEN")
                return

        self._descriptionLabel.setTranslateText("DOWNLOAD_DIALOG.CONVERT_FAILED")


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
            Logger.error(e)
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
    succeed = pyqtSignal(str)
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
            self.succeed.emit(song.getLocation())

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
