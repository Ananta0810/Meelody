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
from modules.widgets.Buttons import IconButton
from modules.widgets.Cover import CoverProp
from modules.widgets.PlaylistCards import PlaylistCard, FavouritePlaylistCard, UserPlaylistCard, NewPlaylistDialog


class PlaylistCardData:
    __onclick: Callable[[], None] = None
    __ondelete: Callable[[], None] = None
    __onchange_cover: Callable[[str], None] = None
    __onchange_title: Callable[[str], bool] = None
    __default_cover: CoverProp = None

    def __init__(self, playlist: PlaylistInformation):
        self.__content: PlaylistInformation = playlist

    def content(self) -> PlaylistInformation:
        return self.__content

    def onchange_title(self) -> Callable[[str], bool]:
        return self.__onchange_title

    def onchange_cover(self) -> Callable[[str], None]:
        return self.__onchange_cover

    def ondelete(self) -> Callable[[], None]:
        return self.__ondelete

    def default_cover(self) -> CoverProp:
        return self.__default_cover

    def onclick(self) -> Callable[[], None]:
        return self.__onclick

    def set_onclick(self, fn: Callable[[], None]) -> None:
        self.__onclick = fn

    def set_ondelete(self, fn: Callable[[], None]) -> None:
        self.__ondelete = fn

    def set_onchange_title(self, fn: Callable[[str], bool]) -> None:
        self.__onchange_title = fn

    def set_onchange_cover(self, fn: Callable[[str], None]) -> None:
        self.__onchange_cover = fn


class PlaylistCarousel(QScrollArea, BaseView):
    __HOVER_ANIMATION: Animation = Animation(1.0, 1.1, 250)

    __inner: QWidget
    __main_layout: QHBoxLayout
    __user_playlists: QHBoxLayout
    __default_playlists: QHBoxLayout
    __playlist_library: PlaylistCard
    __playlist_favourites: FavouritePlaylistCard
    __add_playlist_card: QWidget
    __btn_add_playlist: IconButton

    __default_cover: CoverProp = None
    __playlists: list[PlaylistCardData] = []
    __playlist_view_map_to_playlist: dict[PlaylistCardData, UserPlaylistCard] = {}

    __on_add_playlist_fn: Callable[[str, bytes], bool] = None

    def __init__(self, parent: Optional["QWidget"] = None):
        super(PlaylistCarousel, self).__init__(parent)
        self.__init_ui()
        self.__playlist_library.set_label_text("Library")
        self.__playlist_favourites.set_label_text("Favourites")

    def __init_ui(self):
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.__inner = QWidget()
        self.setWidget(self.__inner)

        # =================Library=================
        self.__playlist_library = self.__create_library_playlist()
        self.__playlist_favourites = self.__create_favourite_playlist()

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
        self.__btn_add_playlist.clicked.connect(lambda: self.__open_dialog())

        self.__main_layout = QHBoxLayout(self.__inner)
        self.__main_layout.setAlignment(Qt.AlignLeft)
        self.__main_layout.setSpacing(32)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

        self.__main_layout.addLayout(self.__default_playlists)
        self.__main_layout.addLayout(self.__user_playlists)
        self.__main_layout.addWidget(self.__add_playlist_card)
        self.__main_layout.addStretch()

        self.__add_playlist_dialog = NewPlaylistDialog()

    @override
    def wheelEvent(self, event):
        delta = event.angleDelta().y()

        x = self.horizontalScrollBar().value()
        self.horizontalScrollBar().setValue(x - delta)

    @override
    def setContentsMargins(self, left: int, top: int, right: int, bottom: int) -> None:
        self.__main_layout.setContentsMargins(left, top, right, bottom)

    @override
    def apply_light_mode(self) -> None:
        self.__add_playlist_card.setStyleSheet(Backgrounds.CIRCLE_PRIMARY_10.to_stylesheet(border_radius_size=48))
        self.__add_playlist_dialog.apply_light_mode()
        self.__btn_add_playlist.apply_light_mode()

    @override
    def apply_dark_mode(self) -> None:
        self.__add_playlist_card.setStyleSheet(Backgrounds.CIRCLE_WHITE_25.to_stylesheet(border_radius_size=48))
        self.__add_playlist_dialog.apply_dark_mode()
        self.__btn_add_playlist.apply_dark_mode()

    @connector
    def set_onclick_library(self, fn: Callable[[], None]) -> None:
        self.__playlist_library.set_onclick_fn(fn)

    @connector
    def set_onclick_favourites(self, fn: Callable[[], None]) -> None:
        self.__playlist_favourites.set_onclick_fn(fn)

    @connector
    def set_on_add_playlist(self, fn: Callable[[str, bytes], bool]) -> None:
        self.__on_add_playlist_fn = fn

    def __open_dialog(self) -> None:
        self.__add_playlist_dialog.set_title("Untitled")
        self.__add_playlist_dialog.set_cover(Images.DEFAULT_PLAYLIST_COVER)
        self.__add_playlist_dialog.on_apply_change(self.__on_add_playlist_fn)
        self.__add_playlist_dialog.show()

    def set_default_playlist_cover(self, cover: bytes) -> None:
        self.__default_cover = self.__create_cover(cover)
        try:
            self.__playlist_library.set_default_cover(self.__default_cover)
            self.__playlist_library.set_cover(self.__default_cover)
            for playlist in self.__playlist_view_map_to_playlist.values():
                playlist.set_default_cover(self.__default_cover)
                playlist.set_cover(self.__default_cover)
        except AttributeError:
            pass

    def load_playlists(self, playlists: list[PlaylistCardData]) -> None:
        self.__clear_playlists()
        for playlist in playlists:
            self.add_playlist(playlist)

    def __clear_playlists(self):
        for index in range(0, len(self.__playlists)):
            self.__user_playlists.itemAt(index).widget().deleteLater()
        self.__playlists.clear()
        self.__playlist_view_map_to_playlist.clear()

    def add_playlist(self, data: PlaylistCardData) -> None:
        playlist_view = self.__create_user_playlist_with_cover()
        self.__attach_data_to(playlist_view, src=data)
        self.__user_playlists.addWidget(playlist_view)

        self.__playlists.append(data)
        self.__playlist_view_map_to_playlist[data] = playlist_view

    @staticmethod
    def __attach_data_to(playlist_view: UserPlaylistCard, src: PlaylistCardData) -> None:
        content = src.content()
        playlist_view.set_label_default_text(content.name)
        playlist_view.set_label_text(content.name)
        playlist_view.set_onclick_fn(src.onclick())
        playlist_view.set_onchange_title(src.onchange_title())
        playlist_view.set_onchange_cover(src.onchange_cover())
        playlist_view.set_ondelete(src.ondelete())
        playlist_view.set_cover(
            src.default_cover()
            if content.cover is None
            else PlaylistCarousel.__create_cover(content.cover)
        )

    def set_on_change_favourites_cover(self, fn: Callable[[str], bytes]) -> None:
        self.__playlist_favourites.set_onchange_cover(fn)

    def set_favourites_cover(self, cover: bytes) -> None:
        self.__playlist_favourites.set_favourites_cover(cover)

    def delete_playlist(self, playlist: PlaylistCardData) -> None:
        index = self.__playlists.index(playlist)
        self.__user_playlists.itemAt(index).widget().deleteLater()
        self.__playlists.remove(self.__playlists[index])
        self.__playlist_view_map_to_playlist.pop(playlist)

    def update_playlist(self, playlist: PlaylistCardData) -> None:
        playlist_view = self.__playlist_view_map_to_playlist[playlist]
        self.__attach_data_to(playlist_view, src=playlist)

    @staticmethod
    def __create_library_playlist() -> PlaylistCard:
        playlist = PlaylistCard(FontBuilder.build(size=16, bold=True))
        playlist.setFixedSize(256, 320)
        playlist.setCursor(Cursors.HAND)
        playlist.set_default_cover(PlaylistCarousel.__create_cover(Images.NULL_IMAGE))
        playlist.set_animation(PlaylistCarousel.__HOVER_ANIMATION)
        return playlist

    @staticmethod
    def __create_favourite_playlist() -> FavouritePlaylistCard:
        playlist = FavouritePlaylistCard(FontBuilder.build(size=16, bold=True))
        playlist.setFixedSize(256, 320)
        playlist.setCursor(Cursors.HAND)
        playlist.set_default_cover(PlaylistCarousel.__create_cover(Images.NULL_IMAGE))
        playlist.set_animation(PlaylistCarousel.__HOVER_ANIMATION)
        return playlist

    @staticmethod
    def __create_user_playlist_with_cover() -> UserPlaylistCard:
        playlist = UserPlaylistCard(FontBuilder.build(size=16, bold=True))
        playlist.setFixedSize(256, 320)
        playlist.setCursor(Cursors.HAND)
        playlist.set_default_cover(PlaylistCarousel.__create_cover(Images.NULL_IMAGE))
        playlist.set_animation(PlaylistCarousel.__HOVER_ANIMATION)
        return playlist

    @staticmethod
    def __create_cover(cover_byte: bytes) -> Union[CoverProp, None]:
        if cover_byte is None:
            return None
        return CoverProp.from_bytes(cover_byte, width=256, height=320, radius=24)
