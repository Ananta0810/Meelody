from typing import Optional

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QShowEvent, QWheelEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QHBoxLayout

from app.common.others import translator
from app.common.statics.colors import Colors
from app.common.statics.paddings import Paddings
from app.components.base import Component, Factory
from app.components.widgets import StyleWidget
from app.resource.qt import Icons
from app.views.home.current_playlist import CurrentPlaylist
from app.views.home.playlists_carousel import PlaylistsCarousel
from app.views.home.settings import SettingsDialog


class HomeBody(QScrollArea, Component):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        super()._initComponent()
        self.setClassName("bg-none border-none")

    def _createUI(self) -> None:
        self._inner = StyleWidget()
        self._inner.setClassName("bg-none")
        self.setWidget(self._inner)

        self._mainLayout = QVBoxLayout(self._inner)
        self._mainLayout.setContentsMargins(0, 0, 0, 0)
        self._mainLayout.setSpacing(0)

        self._settingsArea = QWidget()
        self._settingsArea.setContentsMargins(0, 0, 0, 0)

        self._settingsAreaLayout = QHBoxLayout(self._settingsArea)
        self._settingsAreaLayout.setSpacing(0)
        self._settingsAreaLayout.setContentsMargins(0, 0, 0, 0)
        self._settingsAreaLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self._settingsBtn = Factory.createIconButton(QSize(40, 40), padding=Paddings.RELATIVE_33)
        self._settingsBtn.setLightModeIcon(Icons.settings.withColor(Colors.primary))
        self._settingsBtn.setDarkModeIcon(Icons.settings.withColor(Colors.white))
        self._settingsBtn.setClassName("bg-none border-none hover:bg-primary-10 rounded-full dark:hover:bg-white-12")

        self._settingsAreaLayout.addWidget(self._settingsBtn)

        self._playlistsCarousel = PlaylistsCarousel()
        self._currentPlaylist = CurrentPlaylist()

        self._mainLayout.addWidget(self._settingsArea)
        self._mainLayout.addSpacing(8)
        self._mainLayout.addWidget(self._playlistsCarousel)
        self._mainLayout.addSpacing(50)
        self._mainLayout.addWidget(self._currentPlaylist)

    def _translateUI(self) -> None:
        self._settingsBtn.setToolTip(translator.translate("SETTINGS.LABEL"))

    def wheelEvent(self, event: QWheelEvent) -> None:
        carouselTop = self._playlistsCarousel.mapToParent(self._inner.pos()).y()
        carouselBottom = carouselTop + self._playlistsCarousel.height()

        if carouselTop <= event.y() <= carouselBottom:
            return

        return super().wheelEvent(event)

    def setContentsMargins(self, left: int, top: int, right: int, bottom: int) -> None:
        self._inner.setContentsMargins(0, top, 0, bottom)
        self._settingsArea.setContentsMargins(left, 0, right, 0)
        self._playlistsCarousel.setContentsMargins(left, 0, right, 0)
        self._currentPlaylist.setContentsMargins(left, 0, right, 0)

    def showEvent(self, event: QShowEvent) -> None:
        self._playlistsCarousel.setFixedHeight(320)
        self._currentPlaylist.setFixedHeight(self.height())
        return super().showEvent(event)

    def _connectSignalSlots(self) -> None:
        super()._connectSignalSlots()
        self._settingsBtn.clicked.connect(lambda: self.__openDialog())

    @staticmethod
    def __openDialog() -> None:
        dialog = SettingsDialog()
        dialog.show()
