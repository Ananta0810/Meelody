from typing import Optional, Union, Any

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QResizeEvent
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from modules.helpers.PixmapHelper import PixmapHelper
from modules.helpers.types.Strings import Strings
from modules.models.view.builder.BackgroundThemeBuilder import BackgroundThemeBuilder
from modules.models.view.builder.FontBuilder import FontBuilder
from modules.models.view.builder.IconButtonStyle import IconButtonStyle
from modules.models.view.builder.TextStyle import TextStyle
from modules.statics.view.Material import Icons, Paddings, Colors, Backgrounds, ColorBoxes
from modules.widgets.IconButton import IconButton
from modules.widgets.ImageViewer import ImageViewer
from modules.widgets.LabelWithDefaultText import LabelWithDefaultText
from modules.widgets.ToggleIconButton import ToggleIconButton


class SongTableRow(QWidget):
    background: QWidget
    main_layout: QHBoxLayout
    info: QHBoxLayout
    buttons: QWidget
    buttons_layout: QHBoxLayout
    extra_buttons: QWidget
    extra_buttons_layout: QHBoxLayout
    cover: ImageViewer
    title: LabelWithDefaultText
    artist: LabelWithDefaultText
    length: LabelWithDefaultText
    btn_more: IconButton
    btn_love: ToggleIconButton
    btn_play: IconButton
    btn_edit: IconButton
    btn_add_to_playlist: IconButton
    btn_delete: IconButton
    btn_close: IconButton

    def __init__(self, parent: Optional["QWidget"] = None):
        super(SongTableRow, self).__init__(parent)
        self.default_artist = ""
        self.setupUi()

    def setupUi(self) -> None:
        font = FontBuilder.build(size=10)

        self.background = QWidget(self)

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(20, 12, 20, 12)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignLeft)
        self.setLayout(self.main_layout)

        self.info = QHBoxLayout()
        self.info.setSpacing(24)
        self.info.setContentsMargins(0, 8, 0, 8)

        self.buttons = QWidget()
        self.buttons_layout = QHBoxLayout(self.buttons)
        self.buttons_layout.setContentsMargins(8, 8, 8, 8)
        self.buttons_layout.setSpacing(8)

        self.extra_buttons = QWidget()
        self.extra_buttons_layout = QHBoxLayout(self.extra_buttons)
        self.extra_buttons_layout.setSpacing(8)
        self.extra_buttons_layout.setContentsMargins(8, 8, 8, 8)

        self.cover = ImageViewer(self)
        self.cover.setFixedSize(64, 64)

        self.title = LabelWithDefaultText.build(
            font,
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            dark_mode_style=TextStyle(text_color=ColorBoxes.WHITE)
        )
        self.title.setFixedWidth(188)

        self.artist = LabelWithDefaultText.build(
            font,
            light_mode_style=TextStyle(text_color=ColorBoxes.GRAY),
            dark_mode_style=TextStyle(text_color=ColorBoxes.WHITE)
        )
        self.artist.setFixedWidth(128)

        self.length = LabelWithDefaultText.build(
            font,
            light_mode_style=TextStyle(text_color=ColorBoxes.GRAY),
            dark_mode_style=TextStyle(text_color=ColorBoxes.WHITE)
        )
        self.length.setFixedWidth(64)
        self.length.setAlignment(Qt.AlignCenter)

        self.btn_more = IconButton.build(
            size=Icons.LARGE,
            padding=Paddings.RELATIVE_50,
            style=IconButtonStyle(
                light_mode_icon=Icons.MORE.with_color(Colors.PRIMARY),
                light_mode_background=Backgrounds.CIRCLE_HIDDEN_PRIMARY_25,
            ),
        )
        self.btn_more.clicked.connect(lambda: self.show_more())

        self.btn_love = ToggleIconButton.build(
            size=Icons.LARGE,
            padding=Paddings.RELATIVE_50,
            active_btn=IconButtonStyle(
                light_mode_icon=Icons.LOVE.with_color(Colors.PRIMARY),
                light_mode_background=Backgrounds.CIRCLE_HIDDEN_PRIMARY_25,
            ),
            inactive_btn=IconButtonStyle(
                light_mode_icon=Icons.LOVE.with_color(Colors.DANGER),
                light_mode_background=Backgrounds.CIRCLE_HIDDEN_DANGER_25,
            )
        )

        self.btn_play = IconButton.build(
            size=Icons.LARGE,
            padding=Paddings.RELATIVE_50,
            style=IconButtonStyle(
                light_mode_icon=Icons.PLAY.with_color(Colors.PRIMARY),
                dark_mode_icon=Icons.PLAY.with_color(Colors.WHITE),
                light_mode_background=Backgrounds.CIRCLE_PRIMARY_10,
            ),
        )

        self.btn_add_to_playlist = IconButton.build(
            size=Icons.LARGE,
            padding=Paddings.RELATIVE_75,
            style=IconButtonStyle(
                light_mode_icon=Icons.ADD.with_color(Colors.PRIMARY),
                light_mode_background=Backgrounds.CIRCLE_HIDDEN_PRIMARY_25,
            ),
        )

        self.btn_edit = IconButton.build(
            size=Icons.LARGE,
            padding=Paddings.RELATIVE_50,
            style=IconButtonStyle(
                light_mode_icon=Icons.EDIT.with_color(Colors.PRIMARY),
                light_mode_background=Backgrounds.CIRCLE_HIDDEN_PRIMARY_25,
            ),
        )

        self.btn_delete = IconButton.build(
            size=Icons.LARGE,
            padding=Paddings.RELATIVE_50,
            style=IconButtonStyle(
                light_mode_icon=Icons.DELETE.with_color(Colors.PRIMARY),
                light_mode_background=Backgrounds.CIRCLE_HIDDEN_PRIMARY_25,
            ),
        )

        self.btn_close = IconButton.build(
            size=Icons.MEDIUM,
            padding=Paddings.RELATIVE_50,
            style=IconButtonStyle(
                light_mode_icon=Icons.CLOSE.with_color(Colors.WHITE),
                light_mode_background=Backgrounds.CIRCLE_DANGER,
            ),
            parent=self,
        )
        self.btn_close.move(
            self.sizeHint().width() - Icons.MEDIUM.width() // 2,
            self.extra_buttons.rect().top() + 4,
            )
        self.btn_close.clicked.connect(lambda: self.show_less())

        self.main_layout.addLayout(self.info)
        self.main_layout.addWidget(self.buttons)
        self.main_layout.addWidget(self.extra_buttons)

        self.info.addWidget(self.cover)
        self.info.addWidget(self.title, 1)
        self.info.addWidget(self.artist, 1)
        self.info.addWidget(self.length)

        self.buttons_layout.addWidget(self.btn_more)
        self.buttons_layout.addWidget(self.btn_love)
        self.buttons_layout.addWidget(self.btn_play)

        self.extra_buttons_layout.addWidget(self.btn_add_to_playlist)
        self.extra_buttons_layout.addWidget(self.btn_edit)
        self.extra_buttons_layout.addWidget(self.btn_delete)

        self.show_less()

    def apply_light_mode(self) -> None:
        style = BackgroundThemeBuilder.build("QWidget", 16, Backgrounds.CIRCLE_HIDDEN_GRAY_10.with_border_radius(1))
        self.background.setStyleSheet(style)
        self.title.apply_light_mode()
        self.artist.apply_light_mode()
        self.length.apply_light_mode()
        self.btn_more.apply_light_mode()
        self.btn_love.apply_light_mode()
        self.btn_play.apply_light_mode()
        self.btn_edit.apply_light_mode()
        self.btn_add_to_playlist.apply_light_mode()
        self.btn_delete.apply_light_mode()
        self.btn_close.apply_light_mode()

    def apply_dark_mode(self) -> None:
        style = BackgroundThemeBuilder.build("QWidget", 16, Backgrounds.CIRCLE_HIDDEN_GRAY_10.with_border_radius(1))
        self.background.setStyleSheet(style)
        self.title.apply_dark_mode()
        self.artist.apply_dark_mode()
        self.length.apply_dark_mode()
        self.btn_more.apply_dark_mode()
        self.btn_love.apply_dark_mode()
        self.btn_play.apply_dark_mode()
        self.btn_edit.apply_dark_mode()
        self.btn_add_to_playlist.apply_dark_mode()
        self.btn_delete.apply_dark_mode()
        self.btn_close.apply_dark_mode()

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.background.resize(self.size())
        return super().resizeEvent(a0)

    def show_more(self) -> None:
        self.buttons.hide()
        self.btn_close.show()
        self.extra_buttons.show()

    def show_less(self) -> None:
        self.buttons.show()
        self.btn_close.hide()
        self.extra_buttons.hide()

    def set_cover(self, cover: Union[bytes, None]) -> None:
        self.cover.setPixmap(self.__get_cover_from_bytes(cover))

    def set_title(self, title: str = "Song Title") -> None:
        self.title.setText(title)

    def set_artist(self, artist: str) -> None:
        self.artist.setText(artist or self.default_artist)

    def set_length(self, length: float = 0) -> None:
        self.length.setText(Strings.float_to_clock_time(length))

    def set_love_state(self, state: bool) -> None:
        self.btn_love.setChecked(state)

    def set_default_cover(self, cover: bytes) -> None:
        self.cover.set_default_pixmap(self.__get_cover_from_bytes(cover))

    def set_default_artist(self, artist: str) -> None:
        self.default_artist = artist

    def clear_info(self):
        self.set_cover(None)

    @staticmethod
    def __get_cover_from_bytes(cover_byte: bytes) -> Union[QPixmap, None]:
        if cover_byte is None:
            return None
        return PixmapHelper.get_edited_pixmap_from_bytes(cover_byte, width=64, height=64, radius=12)