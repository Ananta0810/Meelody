from typing import Optional, Union, Callable

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QScrollArea, QWidget, QHBoxLayout

from modules.helpers.types.Decorators import override, connector
from modules.models.PlaylistInformation import PlaylistInformation
from modules.models.view.Animation import Animation
from modules.models.view.builder.FontBuilder import FontBuilder
from modules.models.view.builder.IconButtonStyle import IconButtonStyle
from modules.screens.AbstractScreen import BaseView
from modules.statics.view.Material import Icons, Colors, Cursors, Paddings, Backgrounds, Images
from modules.widgets.Cover import Cover
from modules.widgets.EditablePlaylistCard import EditablePlaylistCard
from modules.widgets.IconButton import IconButton
from modules.widgets.PlaylistCard import PlaylistCard


class PlaylistCardData:
    def __init__(self,
                 playlist: PlaylistInformation,
                 onclick: Callable[[], None],
                 ondelete: Callable[[], None],
                 onchange_title: Callable[[], None]
                 ):
        self.content: PlaylistInformation = playlist
        self.onclick: Callable[[], None] = onclick
        self.ondelete: Callable[[], None] = ondelete
        self.onchange_title: Callable[[], None] = onchange_title


class PlaylistCarouselView(QScrollArea, BaseView):
    __HOVER_ANIMATION: Animation = Animation(1.0, 1.1, 250)

    __inner: QWidget
    __main_layout: QHBoxLayout
    __user_playlists: QHBoxLayout
    __default_playlists: QHBoxLayout
    __playlist_library: PlaylistCard
    __playlist_favourites: PlaylistCard
    __add_playlist_card: QWidget
    __btn_add_playlist: IconButton

    def __init__(self, parent: Optional["QWidget"] = None):
        super(PlaylistCarouselView, self).__init__(parent)
        self.__playlists: list[PlaylistCardData] = []
        self.__init_ui()
        self.__playlist_library.set_label_text("Library")
        self.__playlist_favourites.set_label_text("Favourites")

    def __init_ui(self):
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.__inner = QWidget()
        self.setWidget(self.__inner)

        self.__main_layout = QHBoxLayout(self.__inner)
        self.__main_layout.setAlignment(Qt.AlignLeft)
        self.__main_layout.setSpacing(32)

        # =================Library=================
        self.__playlist_library = self.__create_default_playlist_with_cover(Images.DEFAULT_PLAYLIST_COVER)
        self.__playlist_favourites = self.__create_default_playlist_with_cover(Images.FAVOURITES_PLAYLIST_COVER)

        self.__default_playlists = QHBoxLayout()
        self.__default_playlists.setAlignment(Qt.AlignLeft)
        self.__default_playlists.addWidget(self.__playlist_library)
        self.__default_playlists.addWidget(self.__playlist_favourites)

        self.__user_playlists = QHBoxLayout()
        self.__user_playlists.setAlignment(Qt.AlignLeft)

        # =================New playlist=================
        self.__add_playlist_card = QWidget()
        self.__add_playlist_card.setFixedSize(256, 320)

        self.__btn_add_playlist = IconButton.build(
            padding=Paddings.RELATIVE_67,
            size=Icons.LARGE,
            style=IconButtonStyle(
                light_mode_icon=Icons.ADD.with_color(Colors.PRIMARY),
                light_mode_background=Backgrounds.CIRCLE_HIDDEN_PRIMARY_25,
            ),
            parent=self.__add_playlist_card,
        )
        self.__btn_add_playlist.setCursor(Cursors.HAND)
        self.__btn_add_playlist.move(self.__add_playlist_card.rect().center() - self.__btn_add_playlist.rect().center())

        self.__main_layout.addLayout(self.__default_playlists)
        self.__main_layout.addLayout(self.__user_playlists)
        self.__main_layout.addWidget(self.__add_playlist_card)
        self.__main_layout.addStretch()

    @override
    def setContentsMargins(self, left: int, top: int, right: int, bottom: int) -> None:
        self.__main_layout.setContentsMargins(left, top, right, bottom)

    @override
    def apply_light_mode(self) -> None:
        self.__btn_add_playlist.apply_light_mode()
        self.__add_playlist_card.setStyleSheet(Backgrounds.CIRCLE_PRIMARY_10.to_stylesheet(border_radius_size=48))

    @override
    def apply_dark_mode(self) -> None:
        self.__btn_add_playlist.apply_dark_mode()
        self.__add_playlist_card.setStyleSheet(Backgrounds.CIRCLE_WHITE_25.to_stylesheet(border_radius_size=48))

    @connector
    def set_onclick_library(self, fn: Callable[[], None]) -> None:
        self.__playlist_library.set_onclick_fn(fn)

    @connector
    def set_onclick_favourites(self, fn: Callable[[], None]) -> None:
        self.__playlist_favourites.set_onclick_fn(fn)

    @connector
    def set_onclick_add_playlist(self, fn: Callable[[], None]) -> None:
        self.__btn_add_playlist.clicked.connect(lambda: fn())

    def load_playlists(self, playlists: list[PlaylistCardData]) -> None:
        self.__clear_playlists()
        for playlist in playlists:
            self.add_playlist(playlist)

    def __clear_playlists(self):
        for index in range(0, len(self.__playlists)):
            self.__user_playlists.itemAt(index).widget().deleteLater()
        self.__playlists.clear()

    def add_playlist(self, playlist: PlaylistCardData) -> None:
        self.__playlists.append(playlist)
        playlist_view = self.__create_user_playlist_with_cover(playlist.content.cover)
        playlist_view.set_label_default_text(playlist.content.name)
        playlist_view.set_label_text(playlist.content.name)
        playlist_view.set_onclick_fn(playlist.onclick)
        self.__user_playlists.addWidget(playlist_view)

    @staticmethod
    def __create_default_playlist_with_cover(cover_byte: bytes) -> PlaylistCard:
        playlist = PlaylistCard(FontBuilder.build(size=16, bold=True))
        playlist.setFixedSize(256, 320)
        playlist.setCursor(Cursors.HAND)
        playlist.set_animation(PlaylistCarouselView.__HOVER_ANIMATION)
        playlist.set_cover(PlaylistCarouselView.__get_pixmap_for_playlist_cover(cover_byte))
        return playlist

    @staticmethod
    def __create_user_playlist_with_cover(cover_byte: bytes) -> PlaylistCard:
        playlist = EditablePlaylistCard(FontBuilder.build(size=16, bold=True))
        playlist.setFixedSize(256, 320)
        playlist.setCursor(Cursors.HAND)
        playlist.set_animation(PlaylistCarouselView.__HOVER_ANIMATION)
        playlist.set_cover(PlaylistCarouselView.__get_pixmap_for_playlist_cover(cover_byte))
        return playlist

    @staticmethod
    def __get_pixmap_for_playlist_cover(cover_byte: bytes) -> Union[Cover, None]:
        if cover_byte is None:
            return None
        return Cover.from_bytes(cover_byte, width=256, height=320, radius=24)
