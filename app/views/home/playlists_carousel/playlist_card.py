from typing import Optional

from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from app.common.models import Playlist
from app.components.base import Cover, LabelWithDefaultText, Factory, CoverProps
from app.components.widgets import ExtendableStyleWidget
from app.resource.qt import Cursors, Images


class PlaylistCard(ExtendableStyleWidget):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

    def _createUI(self) -> None:
        self.setFixedSize(256, 320)
        self.setCursor(Cursors.HAND)

        self._mainLayout = QVBoxLayout(self)
        self._mainLayout.setContentsMargins(20, 20, 20, 20)
        self._cover = Cover(self)
        self._cover.setDefaultCover(self._toCoverProps(Images.DEFAULT_PLAYLIST_COVER))
        self._cover.setAnimation(duration=250, start=1.0, end=1.1, onValueChanged=self._cover.zoom)

        self._title = LabelWithDefaultText()
        self._title.enableEllipsis()
        self._title.setFixedWidth(320)
        self._title.setFont(Factory.createFont(size=16, bold=True))

        self._mainLayout.addStretch()
        self._mainLayout.addWidget(self._title)

    def setPlaylist(self, playlist: Playlist) -> None:
        info = playlist.getInfo()

        self._title.setText(info.getName())
        self._cover.setCover(self._toCoverProps(info.getCover()))

    def resizeEvent(self, event: QResizeEvent) -> None:
        self._cover.setFixedSize(self.size())
        return super().resizeEvent(event)

    def enterEvent(self, event: QEvent) -> None:
        super().enterEvent(event)
        self._cover.animationOnEnteredHover()

    def leaveEvent(self, event: QEvent) -> None:
        super().leaveEvent(event)
        self._cover.animationOnLeftHover()

    @staticmethod
    def _toCoverProps(cover: bytes) -> CoverProps:
        return CoverProps.fromBytes(cover, width=256, height=320, radius=24)


class LibraryPlaylistCard(PlaylistCard):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        super()._initComponent()
        self._title.setText("Library")
        self._cover.setCover(self._toCoverProps(Images.DEFAULT_PLAYLIST_COVER))
