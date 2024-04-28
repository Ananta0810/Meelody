from typing import Optional

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QWidget, QLabel
from pytube import YouTube

from app.components.base import Cover, LabelWithDefaultText, Factory, CoverProps
from app.components.sliders import ProgressBar
from app.components.widgets import ExtendableStyleWidget, Box, FlexBox
from app.helpers.base import Strings
from app.helpers.others import Times
from app.helpers.stylesheets import Paddings, Colors
from app.resource.qt import Images, Icons
from app.views.threads import UpdateUIThread, DownloadSongThread


class DownloadSongItem(ExtendableStyleWidget):

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

        self._gif = QLabel()
        self._gif.setFixedSize(48, 48)
        movie = QMovie("app/resource/images/defaults/loading.gif")
        movie.setScaledSize(QSize(48, 48))
        self._gif.setMovie(movie)

        self._icons = QWidget()
        self._icons.setFixedWidth(48)

        self._iconsLayout = Box(self._icons)
        self._iconsLayout.setAlignment(Qt.AlignRight)
        self._iconsLayout.addWidget(self._gif)
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

    def download(self, url: str) -> None:
        yt = YouTube(url)

        self.setTitle(yt.title)

        downloadSongThread = DownloadSongThread(yt, onDownloading=self.__onDownloading)
        loadingAnimationThread = UpdateUIThread(action=lambda: self.__onLoading(), interval=250)
        downloadingAnimationThread = UpdateUIThread(action=lambda: self.__updateDownloadingAnimation(), interval=1000 / 24)

        downloadSongThread.loaded.connect(loadingAnimationThread.quit)
        downloadSongThread.loaded.connect(downloadingAnimationThread.start)
        downloadSongThread.downloadSucceed.connect(lambda path: self.__markSucceed())
        downloadSongThread.downloadSucceed.connect(lambda path: downloadingAnimationThread.quit())
        downloadSongThread.downloadFailed.connect(lambda exception: self.__markFailed(exception))
        downloadSongThread.downloadFailed.connect(lambda exception: loadingAnimationThread.quit())
        downloadSongThread.downloadFailed.connect(lambda exception: downloadingAnimationThread.quit())

        loadingAnimationThread.start()
        downloadSongThread.start()

    def __updateDownloadingAnimation(self):
        if self._gif.isVisible():
            self._gif.movie().jumpToNextFrame()

    def __onLoading(self) -> None:
        self._descriptionLabel.setText(f"Loading{int(self._dot) * '.'}")
        self._dot = (self._dot + 1) % 4

    def __onDownloading(self, bytesDownloaded: int, totalSize: int, estimateTime: int) -> None:
        percentage = bytesDownloaded * 100 / totalSize
        downloadedStr = Strings.convertBytes(bytesDownloaded)
        totalStr = Strings.convertBytes(totalSize)

        description = f"{int(percentage)}%  |  {downloadedStr}/{totalStr}  |  estimate: {Times.toString(estimateTime)}"
        self.setProgress(percentage)
        self.setDescription(description)

    def __markSucceed(self) -> None:
        self._gif.hide()
        self._successIcon.show()
        self._descriptionLabel.setText("Download Succeed.")

    def __markFailed(self, exception: Exception) -> None:
        self._gif.hide()
        self._failedIcon.show()
        if isinstance(exception, FileExistsError):
            self._descriptionLabel.setText("Download Failed. Song is already existed.")
        else:
            self._descriptionLabel.setText("Download Failed.")
