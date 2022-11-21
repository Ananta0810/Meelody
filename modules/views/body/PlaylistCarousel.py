from typing import Optional, Union

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QScrollArea, QWidget, QHBoxLayout

from modules.helpers.PixmapHelper import PixmapHelper
from modules.models.view.Animation import Animation
from modules.models.view.builder.FontBuilder import FontBuilder
from modules.models.view.builder.IconButtonStyle import IconButtonStyle
from modules.statics.view.Material import Icons, Colors, Cursors, Paddings, Backgrounds, Images
from modules.widgets.DefaultPlaylistCard import DefaultPlaylistCard
from modules.widgets.IconButton import IconButton


class PlaylistCarousel(QScrollArea):
    HOVER_ANIMATION: Animation = Animation(1.0, 1.1, 250)

    inner: QWidget
    main_layout: QHBoxLayout
    user_playlists: QHBoxLayout
    default_playlists: QHBoxLayout
    playlist_library: DefaultPlaylistCard
    playlist_favourites: DefaultPlaylistCard
    add_playlist_card: QWidget
    btn_add_playlist: IconButton

    def __init__(self, parent: Optional["QWidget"] = None):
        super(PlaylistCarousel, self).__init__(parent)
        self.setup_ui()
        self.playlist_library.set_label_text("Library")
        self.playlist_favourites.set_label_text("Favourites")

    def setup_ui(self):
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.inner = QWidget()
        self.setWidget(self.inner)

        self.main_layout = QHBoxLayout(self.inner)
        self.main_layout.setAlignment(Qt.AlignLeft)
        self.main_layout.setSpacing(32)

        # =================Library=================
        self.playlist_library = self.create_default_playlist_with_cover(Images.DEFAULT_PLAYLIST_COVER)
        self.playlist_favourites = self.create_default_playlist_with_cover(Images.FAVOURITES_PLAYLIST_COVER)

        self.default_playlists = QHBoxLayout()
        self.default_playlists.setAlignment(Qt.AlignLeft)
        self.default_playlists.addWidget(self.playlist_library)
        self.default_playlists.addWidget(self.playlist_favourites)

        self.user_playlists = QHBoxLayout()
        self.user_playlists.setAlignment(Qt.AlignLeft)

        # =================New playlist=================
        self.add_playlist_card = QWidget()
        self.add_playlist_card.setFixedSize(256, 320)

        self.btn_add_playlist = IconButton.build(
            padding=Paddings.RELATIVE_67,
            size=Icons.LARGE,
            style=IconButtonStyle(
                light_mode_icon=Icons.ADD.with_color(Colors.PRIMARY),
                light_mode_background=Backgrounds.CIRCLE_HIDDEN_PRIMARY_25,
            ),
            parent=self.add_playlist_card,
        )
        self.btn_add_playlist.setCursor(Cursors.HAND)
        self.btn_add_playlist.move(self.add_playlist_card.rect().center() - self.btn_add_playlist.rect().center())

        self.main_layout.addLayout(self.default_playlists)
        self.main_layout.addLayout(self.user_playlists)
        self.main_layout.addWidget(self.add_playlist_card)
        self.main_layout.addStretch()

    def apply_light_mode(self) -> None:
        self.btn_add_playlist.apply_light_mode()
        self.add_playlist_card.setStyleSheet(Backgrounds.CIRCLE_PRIMARY_10.to_stylesheet(border_radius_size=48))

    def apply_dark_mode(self) -> None:
        self.btn_add_playlist.apply_dark_mode()
        self.add_playlist_card.setStyleSheet(Backgrounds.CIRCLE_WHITE_25.to_stylesheet(border_radius_size=48))

    @staticmethod
    def create_default_playlist_with_cover(cover_byte: bytes) -> DefaultPlaylistCard:
        playlist = DefaultPlaylistCard(FontBuilder.build(size=16, bold=True))
        playlist.setFixedSize(256, 320)
        playlist.setCursor(Cursors.HAND)
        playlist.set_animation(PlaylistCarousel.HOVER_ANIMATION)
        playlist.set_cover(PlaylistCarousel.__get_pixmap_for_playlist_cover(cover_byte))
        return playlist

    @staticmethod
    def __get_pixmap_for_playlist_cover(cover_byte: bytes) -> Union[QPixmap, None]:
        if cover_byte is None:
            return None
        return PixmapHelper.get_edited_pixmap_from_bytes(cover_byte, width=256, height=320, radius=24)

    # =================Qt Override methods=================
    def setContentsMargins(self, left: int, top: int, right: int, bottom: int) -> None:
        self.main_layout.setContentsMargins(left, top, right, bottom)