from constants.ui.qss import Paddings
from modules.screens.components.icon_buttons import IconButton
from modules.screens.components.labels import DoubleClickedEditableLabel
from modules.screens.others.animation import Animation
from modules.screens.themes.theme_builders import ThemeData
from PyQt5.QtCore import QEvent, QRect, Qt, pyqtSignal
from PyQt5.QtGui import QCursor, QFont, QIcon, QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget
from utils.ui.pixmap_utils import PixmapUtils
from widgets.image_displayer import ImageDisplayer


class EditablePlaylistCard(QWidget):
    clicked = pyqtSignal()

    def __init__(
        self,
        labelFont: QFont,
        buttonTheme: ThemeData,
        icons: dict[str, QIcon],
        iconSize: int,
        parent=None,
    ):
        super().__init__(parent)
        self._defaultText = None
        self._buttonTheme = buttonTheme
        self.setupUi(labelFont, icons, iconSize)

    def setupUi(
        self,
        labelFont: QFont,
        icons: dict[str, QIcon],
        iconSize: int,
    ) -> None:
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 10, 10, 20)

        self.editBtn = IconButton.render(
            padding=Paddings.RELATIVE_50,
            size=iconSize,
            lightModeIcon=icons.get("lightModeEditBtn"),
            darkModeIcon=icons.get("darkModeEditBtn"),
        )
        self.deleteBtn = IconButton.render(
            padding=Paddings.RELATIVE_50,
            size=iconSize,
            lightModeIcon=icons.get("lightModeDeleteBtn"),
            darkModeIcon=icons.get("darkModeDeleteBtn"),
        )
        self.btns = QHBoxLayout()
        self.btns.setContentsMargins(0, 0, 0, 0)
        self.btns.addStretch()
        self.btns.addWidget(self.editBtn)
        self.btns.addWidget(self.deleteBtn)

        self.cover = ImageDisplayer(self)
        self.label = DoubleClickedEditableLabel.render(labelFont, parent=self)

        self.main_layout.addLayout(self.btns)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.label)

    def mousePressEvent(self, event: QEvent) -> None:
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.clicked.emit()

    def enterEvent(self, event: QEvent) -> None:
        super().enterEvent(event)
        self.cover.animationOnEnteredHover()

    def leaveEvent(self, event: QEvent) -> None:
        super().leaveEvent(event)
        self.cover.animationOnLeavedHover()

    def resizeEvent(self, event: QEvent) -> None:
        self.cover.setFixedSize(self.size())
        return super().resizeEvent(event)

    def getCover(self) -> QPixmap:
        return self.cover.pixmap()

    def setCover(self, pixmap: QPixmap) -> None:
        if pixmap is None:
            pixmap = self.cover._defaultPixmap
        if pixmap is None:
            return
        self.cover.setPixmap(pixmap)
        self.__adaptItemColorsBaseOnCover()

    def setButtonsCursor(self, cursor: QCursor) -> None:
        self.editBtn.setCursros(cursor)
        self.deleteBtn.setCursros(cursor)

    def setDefaultCover(self, pixmap: QPixmap):
        self.cover.setDefaultPixmap(pixmap)

    def setText(self, text: str) -> None:
        if text is None:
            text = self._defaultText
        self.label.setText(text)

    def setDefaultText(self, text: str) -> None:
        oldText: str = self._defaultText
        self._defaultText = text
        if self.label.text() == oldText:
            self.label.setText(text)

    def setAnimation(self, animation: Animation) -> None:
        if animation is None:
            return
        self.cover.setAnimation(
            duration=animation.durationInMs, start=animation.start, end=animation.end, type=self.cover.zoom
        )

    def __adaptItemColorsBaseOnCover(self) -> None:
        pixmap = self.getCover()
        self.__adaptButtonsBaseOnCover(pixmap)
        self.__adaptLabelBaseOnCover(pixmap)

    def __adaptButtonsBaseOnCover(self, coverPixmap: QPixmap) -> None:
        brightness = PixmapUtils.getPixmapBrightness(coverPixmap.copy(self.__getButtonsRect()))
        if brightness < 0.5:
            self.editBtn.setStyleSheet(self._buttonTheme.darkMode)
            self.deleteBtn.setStyleSheet(self._buttonTheme.darkMode)
            self.editBtn.setDarkMode(True)
            self.deleteBtn.setDarkMode(True)
        else:
            self.editBtn.setStyleSheet(self._buttonTheme.lightMode)
            self.deleteBtn.setStyleSheet(self._buttonTheme.lightMode)
            self.editBtn.setDarkMode(False)
            self.deleteBtn.setDarkMode(False)

    def __adaptLabelBaseOnCover(self, coverPixmap: QPixmap) -> None:
        brightness = PixmapUtils.getPixmapBrightness(coverPixmap.copy(self.label.rect()))
        if brightness < 0.5:
            self.label.setStyleSheet("color:white")
        else:
            self.label.setStyleSheet("color:black")

    def __getButtonsRect(self) -> QRect:
        buttonsStartRect = self.editBtn.rect()
        return QRect(
            buttonsStartRect.left(),
            buttonsStartRect.top(),
            buttonsStartRect.width() + self.editBtn.rect().width(),
            buttonsStartRect.height(),
        )
