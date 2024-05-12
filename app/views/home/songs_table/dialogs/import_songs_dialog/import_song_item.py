import os
from typing import Optional

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QWidget, QShortcut, QVBoxLayout

from app.common.exceptions import ResourceException
from app.common.models import Song
from app.common.models.song import SongReader
from app.common.others import translator
from app.common.statics.qt import Images
from app.components.base import Cover, CoverProps, Label, Factory, EllipsisLabel, ActionButton, Input, CoverWithPlaceHolder, AutoTranslateLabel
from app.components.dialogs import BaseDialog
from app.components.widgets import ExtendableStyleWidget, Box, FlexBox
from app.helpers.base import Strings
from app.helpers.others import Logger, Files


class ImportSongItem(ExtendableStyleWidget):
    succeed = pyqtSignal(str)
    failed = pyqtSignal(Exception)
    imported = pyqtSignal()
    reImported = pyqtSignal(str)

    def __init__(self, path: str):
        super().__init__()
        self._initComponent()
        self._translateUI()

        self._path = path
        self.__artist: Optional[str] = None

        self.__displaySongInfo()

    def _createUI(self) -> None:
        self.setContentsMargins(0, 0, 0, 0)

        self._cover = CoverWithPlaceHolder()
        self._cover.setFixedSize(48, 48)
        self._cover.setPlaceHolderCover(CoverProps.fromBytes(Images.defaultSongCover, width=48, height=48, radius=8))

        self._titleLabel = EllipsisLabel()
        self._titleLabel.setFont(Factory.createFont(size=10))
        self._titleLabel.setClassName("text-black dark:text-white")

        self._descriptionLabel = AutoTranslateLabel()
        self._descriptionLabel.setFont(Factory.createFont(size=9))
        self._descriptionLabel.setClassName("text-black dark:text-white")

        self._infoLayout = Box()
        self._infoLayout.setSpacing(4)
        self._infoLayout.addStretch(0)
        self._infoLayout.addWidget(self._titleLabel)
        self._infoLayout.addWidget(self._descriptionLabel)
        self._infoLayout.addStretch(0)

        self._updateBtn = ActionButton()
        self._updateBtn.setFont(Factory.createFont(family="Segoe UI Semibold", size=10))
        self._updateBtn.setClassName("text-white rounded-4 bg-primary hover:bg-primary-[w120] py-8")
        self._updateBtn.hide()

        self._result = QWidget()
        self._result.setFixedWidth(96)

        self._resultLayout = FlexBox(self._result)
        self._resultLayout.addWidget(self._updateBtn)

        self._mainLayout = FlexBox()
        self._mainLayout.setSpacing(0)
        self._mainLayout.setAlignment(Qt.AlignLeft)

        self._mainLayout.addWidget(self._cover)
        self._mainLayout.addSpacing(12)
        self._mainLayout.addLayout(self._infoLayout, stretch=1)
        self._mainLayout.addWidget(self._result, alignment=Qt.AlignRight)

        self.setLayout(self._mainLayout)

        self.setFixedHeight(self.sizeHint().height())
        self.setMinimumHeight(self.sizeHint().height())

    def _translateUI(self) -> None:
        self._updateBtn.setText(translator.translate("IMPORT_SONGS_DIALOG.CHANGE_TITLE_BTN"))

    def path(self) -> str:
        return self._path

    def applyLightMode(self) -> None:
        super().applyLightMode()
        super().applyThemeToChildren()

    def applyDarkMode(self) -> None:
        super().applyDarkMode()
        super().applyThemeToChildren()

    def _connectSignalSlots(self) -> None:
        self.succeed.connect(lambda path: self.__markSucceed())
        self.failed.connect(lambda exception: self.__markFailed(exception))
        self._updateBtn.clicked.connect(lambda: self.__openUpdateDialog())

    def __displaySongInfo(self) -> None:
        song = Song.fromFile(self._path, Strings.getFileBasename(self._path))
        song.loadCover()

        self.__artist = song.getArtist()

        self._cover.setCover(CoverProps.fromBytes(song.getCover(), width=48, height=48, radius=9))
        self._titleLabel.setText(Strings.join("   |   ", [song.getTitle(), song.getArtist()]))

    def startImport(self) -> None:
        try:
            reader = SongReader(self._path)

            if not reader.isValid():
                Logger.error("Invalid mp3 file song.")
                raise ResourceException.brokenFile()

            title = reader.getTitle() or Strings.getFileBasename(self._path)
            songPath = self.__moveFileToLibrary(title)
            self.succeed.emit(songPath)
            self.__markSucceed()
        except ResourceException as e:
            self.failed.emit(e)
        except Exception as e:
            Logger.error(e)
            self.failed.emit(e)

        self.imported.emit()

    def __moveFileToLibrary(self, title: str) -> str:
        songPath = f"library/{Strings.sanitizeFileName(title)}.mp3"
        Files.copyFile(self._path, songPath)
        Logger.info(f"Import song from '{self._path}' to library successfully.")
        return songPath

    def __markSucceed(self) -> None:
        self._descriptionLabel.setClassName("text-black dark:text-white")
        self._descriptionLabel.applyTheme()
        self._descriptionLabel.setTranslateText("IMPORT_SONGS_DIALOG.IMPORT_SUCCESS")

    def __markFailed(self, exception: Exception) -> None:
        self._descriptionLabel.setClassName("text-danger bg-none")
        self._descriptionLabel.applyTheme()

        if isinstance(exception, FileExistsError):
            self._descriptionLabel.setTranslateText("IMPORT_SONGS_DIALOG.IMPORT_FAILED_EXISTED")
            self._updateBtn.show()
            return

        if isinstance(exception, ResourceException):
            self._descriptionLabel.setTranslateText("IMPORT_SONGS_DIALOG.IMPORT_FAILED_BROKEN")
            return

        self._descriptionLabel.setTranslateText("IMPORT_SONGS_DIALOG.IMPORT_FAILED")

    def __openUpdateDialog(self) -> None:
        dialog = UpdateImportSongDialog(self._path)
        dialog.accepted.connect(lambda title: self.__importAgain(title))
        dialog.show()

    def __importAgain(self, title: str) -> None:
        try:
            self._titleLabel.setText(Strings.join("   |   ", [title, self.__artist]))
            songPath = self.__moveFileToLibrary(title)
            self.reImported.emit(songPath)
            self.__markSucceed()
        except ResourceException as e:
            self.failed.emit(e)
        except Exception as e:
            Logger.error(e)
            self.failed.emit(e)


class UpdateImportSongDialog(BaseDialog):
    accepted = pyqtSignal(str)

    def __init__(self, path: str) -> None:
        self.__canUpdate = False
        self.__path = path

        super().__init__()
        super()._initComponent()

        reader = SongReader(path)

        self._titleInput.setText(reader.getTitle() or Strings.getFileBasename(path))
        self.__checkValid()

    def _createUI(self) -> None:
        super()._createUI()

        self._image = Cover()
        self._image.setAlignment(Qt.AlignHCenter)
        self._image.setCover(CoverProps.fromBytes(Images.importSongs, width=128))

        self._header = Label()
        self._header.setFont(Factory.createFont(family="Segoe UI Semibold", size=16, bold=True))
        self._header.setClassName("text-black dark:text-white bg-none")
        self._header.setAlignment(Qt.AlignCenter)

        self._titleLabel = Label()
        self._titleLabel.setFont(Factory.createFont(size=11))
        self._titleLabel.setClassName("text-black dark:text-white bg-none")

        self._titleErrorLabel = Label()
        self._titleErrorLabel.setFont(Factory.createFont(size=11))
        self._titleErrorLabel.setClassName("text-danger bg-none")
        self._titleErrorLabel.hide()

        self._titleInput = Input()
        self._titleInput.setFont(Factory.createFont(size=12))
        self._titleInput.setClassName(
            "px-12 py-8 rounded-4 border border-primary-12 bg-primary-4 disabled:bg-none disabled:border-none disabled:text-black",
            "dark:border-white-[b33] dark:bg-white-12 dark:text-white dark:disabled:text-white",
        )

        self._importBtn = ActionButton()
        self._importBtn.setFont(Factory.createFont(family="Segoe UI Semibold", size=11))
        self._importBtn.setClassName("text-white rounded-4 bg-primary-75 bg-primary py-8 disabled:bg-gray-10 disabled:text-gray")

        self._mainView = QWidget()
        self._mainView.setFixedWidth(480)
        self._mainView.setContentsMargins(12, 4, 12, 12)

        self._viewLayout = QVBoxLayout(self._mainView)
        self._viewLayout.setSpacing(8)
        self._viewLayout.setContentsMargins(0, 0, 0, 0)
        self._viewLayout.addWidget(self._image)
        self._viewLayout.addWidget(self._header)
        self._viewLayout.addWidget(self._titleLabel)
        self._viewLayout.addWidget(self._titleInput)
        self._viewLayout.addWidget(self._titleErrorLabel)
        self._viewLayout.addWidget(self._importBtn)

        self.addWidget(self._mainView)

    def _translateUI(self) -> None:
        self._header.setText(translator.translate("IMPORT_SONGS_DIALOG.LABEL"))
        self._importBtn.setText(translator.translate("IMPORT_SONGS_DIALOG.IMPORT_AGAIN_BTN"))
        self._titleLabel.setText(translator.translate("SONG.TITLE"))

    def _connectSignalSlots(self) -> None:
        super()._connectSignalSlots()

        self._titleInput.changed.connect(lambda text: self.__checkValid())
        self._importBtn.clicked.connect(lambda: self._importAgain())

    def _assignShortcuts(self) -> None:
        super()._assignShortcuts()
        acceptShortcut = QShortcut(QKeySequence(Qt.Key_Return), self._importBtn)
        acceptShortcut.activated.connect(lambda: self._importBtn.click())

    def __checkValid(self) -> None:
        self.__canUpdate = self.__validateTitle()
        self._importBtn.setDisabled(not self.__canUpdate)

    def __validateTitle(self) -> bool:
        title = self._titleInput.text().strip()

        if Strings.isBlank(title):
            self._titleErrorLabel.show()
            self._titleErrorLabel.setText(translator.translate("SONG.VALIDATE.TITLE_BLANK"))
            return False

        if len(title) > 128:
            self._titleErrorLabel.show()
            self._titleErrorLabel.setText(translator.translate("SONG.VALIDATE.TITLE_LENGTH"))
            return False

        if os.path.exists(f"library/{Strings.sanitizeFileName(title)}.mp3"):
            self._titleErrorLabel.show()
            self._titleErrorLabel.setText(translator.translate("SONG.VALIDATE.TITLE_EXISTED"))
            return False

        self._titleErrorLabel.hide()
        return True

    def _importAgain(self) -> None:
        self.__checkValid()
        if not self.__canUpdate:
            return

        title = self._titleInput.text().strip()

        self.accepted.emit(title)
        self.close()
