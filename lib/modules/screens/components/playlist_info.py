from constants.ui.qss import ColorBoxes
from modules.screens.components.font_builder import FontBuilder
from modules.screens.components.labels import StandardLabel
from modules.screens.themes.theme_builders import LabelThemeBuilder, ThemeData
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from utils.ui.application_utils import UiUtils
from widgets.image_displayer import ImageDisplayer


class PlaylistInfo(QVBoxLayout):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.themeItems = {}
        fontBuilder = FontBuilder()
        labelFont: QFont = fontBuilder.withSize(20).withWeight("bold").build()
        totalSongFont: QFont = fontBuilder.withSize(10).withWeight("normal").build()
        textTheme: ThemeData = (
            LabelThemeBuilder().addLightModeTextColor(ColorBoxes.BLACK).addDarkModeTextColor(ColorBoxes.WHITE).build()
        )

        self.setSpacing(12)
        self.cover = ImageDisplayer()
        self.cover.setFixedSize(320, 320)

        self.text_area = QVBoxLayout()
        self.text_area.setSpacing(0)
        self.label = StandardLabel.render(labelFont)
        self.total_song = StandardLabel.render(totalSongFont)

        self.text_area.addWidget(self.label)
        self.text_area.addWidget(self.total_song)

        self.addWidget(self.cover)
        self.addLayout(self.text_area)
        self.addStretch()

        self.setLabel("Library")
        self.setTotalSong(0)
        self.__addThemeForItem(self.label, textTheme)
        self.__addThemeForItem(self.total_song, textTheme)

    def setInfo(self, cover: bytes, label: str, songCount: int) -> None:
        self.setCover(cover)
        self.setLabel(label)
        self.setTotalSong(songCount)

    def setCover(self, cover: bytes) -> None:
        self.cover.setPixmap(self.__getCoverPixmap(cover))

    def setDefaultCover(self, cover: bytes) -> None:
        self.cover.setDefaultPixmap(self.__getCoverPixmap(cover))

    def setLabel(self, name: str) -> None:
        self.label.setText(name)

    def setTotalSong(self, songCount: str) -> None:
        self.total_song.setText(f"{str(songCount)} TRACKS")

    def setCover(self, pixmap) -> None:
        self.cover.setPixmap(self, pixmap)

    def __getCoverPixmap(self, coverAsByte: bytes) -> QPixmap:
        if coverAsByte is None:
            return None
        return UiUtils.getEditedPixmapFromBytes(coverAsByte, width=320, height=320, radius=24)

    def darkMode(self) -> None:
        for item in self.themeItems:
            darkModeStyleSheet = self.themeItems.get(item).darkMode
            if darkModeStyleSheet is None or darkModeStyleSheet.strip() == "":
                continue
            item.setStyleSheet(darkModeStyleSheet)

    def lightMode(self) -> None:
        for item in self.themeItems:
            lightModeStyleSheet = self.themeItems.get(item).lightMode
            if lightModeStyleSheet is None or lightModeStyleSheet.strip() == "":
                continue
            item.setStyleSheet(lightModeStyleSheet)

    def __addThemeForItem(self, item: QWidget, theme: ThemeData) -> None:
        self.themeItems[item] = theme
