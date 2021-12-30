from typing import Optional

from constants.ui.theme_builders import TextThemeBuilders
from modules.screens.components.font_builder import FontBuilder
from modules.screens.components.labels import LabelWithDefaultText
from modules.screens.themes.theme_builders import ThemeData
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from utils.ui.application_utils import UiUtils
from views.view import View
from widgets.image_displayer import ImageDisplayer


class PlaylistInfo(QVBoxLayout, View):
    def __init__(self, parent: Optional["QWidget"] = None) -> None:
        super(PlaylistInfo, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        fontBuilder = FontBuilder()
        textTheme: ThemeData = TextThemeBuilders.DEFAULT.build()

        self.setSpacing(12)
        self.cover = ImageDisplayer()
        self.cover.setFixedSize(320, 320)

        self.text_area = QVBoxLayout()
        self.text_area.setSpacing(0)
        self.label = LabelWithDefaultText.render(fontBuilder.withSize(20).withWeight("bold").build())
        self.total_song = LabelWithDefaultText.render(fontBuilder.withSize(10).withWeight("normal").build())

        self.text_area.addWidget(self.label)
        self.text_area.addWidget(self.total_song)

        self.addWidget(self.cover)
        self.addLayout(self.text_area)
        self.addStretch()

        self.setLabel("Library")
        self.setTotalSong(0)
        self._addThemeForItem(self.label, textTheme)
        self._addThemeForItem(self.total_song, textTheme)

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

    def __getCoverPixmap(self, coverAsByte: bytes) -> QPixmap:
        if coverAsByte is None:
            return None
        return UiUtils.getEditedPixmapFromBytes(coverAsByte, width=320, height=320, radius=24)
