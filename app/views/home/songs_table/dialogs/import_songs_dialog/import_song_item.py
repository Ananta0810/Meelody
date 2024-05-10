from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from app.common.exceptions import ResourceException
from app.common.models import Song
from app.common.models.song import SongReader
from app.components.base import Cover, CoverProps, Label, Factory, EllipsisLabel
from app.components.widgets import ExtendableStyleWidget, Box, FlexBox
from app.helpers.base import Strings
from app.helpers.others import Logger, Files
from app.helpers.stylesheets import Colors, Paddings
from app.resource.qt import Images, Icons


class ImportSongItem(ExtendableStyleWidget):
    succeed = pyqtSignal(str)
    failed = pyqtSignal(Exception)
    imported = pyqtSignal()

    def __init__(self, path: str):
        super().__init__()
        self._initComponent()

        self._path = path
        self._dot: float = 0

        self.__displaySongInfo()

    def _createUI(self) -> None:
        self.setContentsMargins(0, 0, 0, 0)

        self._cover = Cover()
        self._cover.setFixedSize(48, 48)
        self._cover.setDefaultCover(CoverProps.fromBytes(Images.DEFAULT_SONG_COVER, width=48, height=48, radius=8))

        self._titleLabel = EllipsisLabel()
        self._titleLabel.setFont(Factory.createFont(size=10))
        self._titleLabel.setClassName("text-black dark:text-white")

        self._descriptionLabel = Label()
        self._descriptionLabel.setFont(Factory.createFont(size=9))
        self._descriptionLabel.setClassName("text-black dark:text-white")

        self._infoLayout = Box()
        self._infoLayout.setSpacing(4)
        self._infoLayout.addStretch(0)
        self._infoLayout.addWidget(self._titleLabel)
        self._infoLayout.addWidget(self._descriptionLabel)
        self._infoLayout.addStretch(0)

        self._successIcon = Factory.createIconButton(size=Icons.SMALL, padding=Paddings.RELATIVE_25)
        self._successIcon.setLightModeIcon(Icons.APPLY.withColor(Colors.WHITE))
        self._successIcon.setClassName("rounded-full bg-success")
        self._successIcon.hide()

        self._failedIcon = Factory.createIconButton(size=Icons.SMALL, padding=Paddings.RELATIVE_25)
        self._failedIcon.setLightModeIcon(Icons.CLOSE.withColor(Colors.WHITE))
        self._failedIcon.setClassName("rounded-full bg-danger")
        self._failedIcon.hide()

        self._icons = QWidget()
        self._icons.setFixedWidth(48)

        self._iconsLayout = QHBoxLayout(self._icons)
        self._iconsLayout.setAlignment(Qt.AlignRight)
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

        self.setFixedHeight(self.sizeHint().height())
        self.setMinimumHeight(self.sizeHint().height())

    def show(self) -> None:
        super().show()

    def path(self) -> str:
        return self._path

    def setDescription(self, value: str) -> None:
        self._descriptionLabel.setText(value)

    def applyLightMode(self) -> None:
        super().applyLightMode()
        super().applyThemeToChildren()

    def applyDarkMode(self) -> None:
        super().applyDarkMode()
        super().applyThemeToChildren()

    def _connectSignalSlots(self) -> None:
        self.succeed.connect(lambda path: self.__markSucceed())
        self.failed.connect(lambda exception: self.__markFailed(exception))

    def __displaySongInfo(self) -> None:
        song = Song.fromFile(self._path, Strings.sanitizeFileName(Strings.getFileBasename(self._path)))
        song.loadCover()

        self._cover.setCover(CoverProps.fromBytes(song.getCover(), width=48, height=48, radius=9))
        self._titleLabel.setText(Strings.join("   |   ", [song.getTitle(), song.getArtist()]))

    def startImport(self) -> None:
        try:
            reader = SongReader(self._path)

            if not reader.isValid():
                Logger.error("Invalid mp3 file song.")
                raise ResourceException.brokenFile()

            title = Strings.sanitizeFileName(reader.getTitle() or Strings.getFileBasename(self._path))
            songPath = f"library/{title}.mp3"

            Files.copyFile(self._path, songPath)
            Logger.info(f"Import song from '{self._path}' to library successfully.")

            self.succeed.emit(songPath)
            self.__markSucceed()
        except ResourceException as e:
            self.failed.emit(e)
        except Exception as e:
            Logger.error(e)
            self.failed.emit(e)

        self.imported.emit()

    def __markSucceed(self) -> None:
        self._successIcon.show()
        self._descriptionLabel.setText("Import Succeed.")

    def __markFailed(self, exception: Exception) -> None:
        self._failedIcon.show()

        self._descriptionLabel.setClassName("text-danger bg-none")
        self._descriptionLabel.applyTheme()

        if isinstance(exception, FileExistsError):
            self._descriptionLabel.setText("Import failed. Song is already existed.")
            return

        if isinstance(exception, ResourceException):
            self._descriptionLabel.setText("Import failed. Song is broken.")
            return

        self._descriptionLabel.setText("Import failed. Please try again.")
