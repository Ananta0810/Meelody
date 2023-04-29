from typing import Optional, Union, Callable

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QResizeEvent
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout

from modules.helpers import Times
from modules.helpers.types.Decorators import override
from modules.models.view.Background import Background
from modules.models.view.Border import Border
from modules.models.view.Color import Color
from modules.models.view.ColorBox import ColorBox
from modules.models.view.builder.BackgroundThemeBuilder import BackgroundThemeBuilder
from modules.models.view.builder.FontBuilder import FontBuilder
from modules.models.view.builder.IconButtonStyle import IconButtonStyle
from modules.models.view.builder.TextStyle import TextStyle
from modules.screens.AbstractScreen import BaseView
from modules.statics.view.Material import Icons, Paddings, Colors, Backgrounds, ColorBoxes
from modules.widgets import Observers, Dialogs
from modules.widgets.Buttons import ToggleIconButton, IconButton
from modules.widgets.Cover import Cover, CoverProp
from modules.widgets.Icons import AppIcon
from modules.widgets.Labels import LabelWithDefaultText, Input
from modules.widgets.Widgets import BackgroundWidget


class RenameSongDialog(Dialogs.ConfirmDialog):
    def __init__(self, header: str, msg: str | None = None, accept_text: str = "Confirm", reject_text: str = "Cancel",
                 onclick_accept_fn: Callable[[str], bool] = None, onclick_reject_fn: callable = None,
                 dark_mode: bool = False,
                 parent: Optional["QWidget"] = None):
        super().__init__(header, msg, accept_text, reject_text, onclick_accept_fn, onclick_reject_fn, dark_mode, parent)

    def _init_content(self, content: QWidget) -> None:
        layout = QVBoxLayout(content)
        self.__title_input = self.__create_input()
        self.__title_input.set_onpressed(self._on_accepted)
        layout.addWidget(self.__title_input)

        self.__artist_input = self.__create_input()
        self.__artist_input.set_onpressed(self._on_accepted)
        layout.addWidget(self.__artist_input)

    @staticmethod
    def __create_input() -> Input:
        input_ = Input.build(
            font=FontBuilder.build(size=12),
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK,
                                       background=Background(
                                           border_radius=8,
                                           color=ColorBox(
                                               normal=Colors.GRAY.with_opacity(8)),
                                           border=Border(
                                               size=2,
                                               color=Color(192, 192, 192)
                                           ))),
            padding=8
        )
        input_.setFixedHeight(48)
        return input_

    def with_song_title(self, title: str) -> 'RenameSongDialog':
        self.__title_input.setText(title)
        return self

    def with_song_artist(self, artist: str) -> 'RenameSongDialog':
        self.__artist_input.setText(artist)
        return self

    @override
    def _get_onclick_accept_fn(self) -> callable:
        return lambda: self._onclick_accept_fn(self.__title_input.text(), self.__artist_input.text())

    @override
    def apply_dark_mode(self) -> None:
        super().apply_dark_mode()
        self.__title_input.apply_dark_mode()
        self.__artist_input.apply_dark_mode()

    @override
    def apply_light_mode(self) -> None:
        super().apply_light_mode()
        self.__title_input.apply_light_mode()
        self.__artist_input.apply_light_mode()


class SongTableRowView(BackgroundWidget, BaseView):
    __main_layout: QHBoxLayout
    __info: QHBoxLayout
    __buttons: QWidget
    __buttons_layout: QHBoxLayout
    __more_buttons: QWidget
    __more_buttons_layout: QHBoxLayout
    __cover: Cover
    __label_title: LabelWithDefaultText
    __label_artist: LabelWithDefaultText
    __label_length: LabelWithDefaultText
    __btn_more: IconButton
    __btn_love: ToggleIconButton
    __btn_play: IconButton
    __btn_edit_title: IconButton
    __btn_add_to_playlist: IconButton
    __btn_delete: IconButton
    __btn_close: IconButton

    __editable: bool = False
    __removeable: bool = False

    def __init__(self, parent: Optional["QWidget"] = None):
        super(SongTableRowView, self).__init__(parent)
        self.default_artist = ""
        self.__init_ui()
        self.show_less()

    def __init_ui(self) -> None:
        font = FontBuilder.build(size=10)

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.__main_layout = QHBoxLayout()
        self.__main_layout.setContentsMargins(20, 12, 20, 12)
        self.__main_layout.setSpacing(0)
        self.__main_layout.setAlignment(Qt.AlignLeft)
        self.setLayout(self.__main_layout)

        # ================================================= INFO # =================================================
        self.__cover = Cover(self)
        self.__cover.setFixedSize(64, 64)

        self.__label_title = self.__create_label(with_font=font, light_mode_text_color=ColorBoxes.BLACK)
        self.__label_title.setFixedWidth(188)
        self.__title_observer = Observers.observe_click_of(self.__label_title)

        self.__label_artist = self.__create_label(with_font=font)
        self.__label_artist.setFixedWidth(128)

        self.__label_length = self.__create_label(with_font=font)
        self.__label_length.setFixedWidth(64)
        self.__label_length.setAlignment(Qt.AlignCenter)

        self.__info = QHBoxLayout()
        self.__info.setSpacing(24)
        self.__info.setContentsMargins(0, 8, 0, 8)
        self.__info.addWidget(self.__cover)
        self.__info.addWidget(self.__label_title, 1)
        self.__info.addWidget(self.__label_artist, 1)
        self.__info.addWidget(self.__label_length)
        self.__main_layout.addLayout(self.__info)

        # ============================================ REACT BUTTONS # ============================================
        self.__btn_more = self.__create_button(with_icon=Icons.MORE)
        self.__btn_more.clicked.connect(lambda: self.show_more())
        self.__btn_love = ToggleIconButton.build(
            size=Icons.LARGE,
            padding=Paddings.RELATIVE_50,
            active_btn=IconButtonStyle(
                light_mode_icon=Icons.LOVE.with_color(Colors.DANGER),
                light_mode_background=Backgrounds.CIRCLE_HIDDEN_DANGER_10,
            ),
            inactive_btn=IconButtonStyle(
                light_mode_icon=Icons.LOVE.with_color(Colors.GRAY),
                light_mode_background=Backgrounds.CIRCLE_HIDDEN_GRAY_10,
            )
        )
        self.__btn_play = IconButton.build(
            size=Icons.LARGE,
            padding=Paddings.RELATIVE_50,
            style=IconButtonStyle(
                light_mode_icon=Icons.PLAY.with_color(Colors.PRIMARY),
                dark_mode_icon=Icons.PLAY.with_color(Colors.WHITE),
                light_mode_background=Backgrounds.CIRCLE_PRIMARY_10,
            ),
        )

        self.__buttons = QWidget()
        self.__buttons_layout = QHBoxLayout(self.__buttons)
        self.__buttons_layout.setContentsMargins(8, 8, 8, 8)
        self.__buttons_layout.setSpacing(8)
        self.__buttons_layout.addWidget(self.__btn_more)
        self.__buttons_layout.addWidget(self.__btn_love)
        self.__buttons_layout.addWidget(self.__btn_play)
        self.__main_layout.addWidget(self.__buttons)

        # ============================================ MORE BUTTONS # ============================================
        self.__btn_edit_title = self.__create_button(with_icon=Icons.EDIT)
        self.__btn_edit_title.keep_space_when_hiding()

        self.__btn_edit_cover = self.__create_button(with_icon=Icons.IMAGE)
        self.__btn_edit_cover.keep_space_when_hiding()

        self.__btn_delete = self.__create_button(with_icon=Icons.DELETE)
        self.__btn_delete.keep_space_when_hiding()

        self.__more_buttons = BackgroundWidget()
        self.__more_buttons_layout = QHBoxLayout(self.__more_buttons)
        self.__more_buttons_layout.setSpacing(8)
        self.__more_buttons_layout.setContentsMargins(8, 8, 8, 8)

        self.__more_buttons_layout.addWidget(self.__btn_edit_title)
        self.__more_buttons_layout.addWidget(self.__btn_edit_cover)
        self.__more_buttons_layout.addWidget(self.__btn_delete)
        self.__main_layout.addWidget(self.__more_buttons)

        # ======================================== SELECT SONG BUTTONS # ========================================
        self.__btn_add_to_playlist = self.__create_button(with_icon=Icons.ADD, padding=Paddings.RELATIVE_67)
        self.__btn_remove_from_playlist = self.__create_button(with_icon=Icons.MINUS,
                                                               padding=Paddings.RELATIVE_33,
                                                               color=Colors.DANGER,
                                                               background=Backgrounds.CIRCLE_HIDDEN_DANGER_10)
        self.__btn_remove_from_playlist.hide()

        self.__choosing_playlist_buttons = QWidget()
        self.__choosing_playlist_buttons_layout = QHBoxLayout(self.__choosing_playlist_buttons)
        self.__choosing_playlist_buttons_layout.setSpacing(8)
        self.__choosing_playlist_buttons_layout.setContentsMargins(8, 8, 8, 8)
        self.__choosing_playlist_buttons_layout.addStretch(0)
        self.__choosing_playlist_buttons_layout.addWidget(self.__btn_add_to_playlist)
        self.__choosing_playlist_buttons_layout.addWidget(self.__btn_remove_from_playlist)
        self.__main_layout.addWidget(self.__choosing_playlist_buttons)

        self.__btn_close = IconButton.build(
            size=Icons.MEDIUM,
            padding=Paddings.RELATIVE_50,
            style=IconButtonStyle(
                light_mode_icon=Icons.CLOSE.with_color(Colors.WHITE),
                light_mode_background=Backgrounds.CIRCLE_DANGER,
            ),
            parent=self,
        )

        self.__btn_close.clicked.connect(lambda: self.show_less())

    @override
    def resizeEvent(self, event: QResizeEvent) -> None:
        self.__btn_close.move(
            self.sizeHint().width() - Icons.MEDIUM.width() // 2,
            self.__more_buttons.rect().top() + 4,
        )
        return super().resizeEvent(event)

    @override
    def apply_light_mode(self) -> None:
        style = BackgroundThemeBuilder.build("QWidget", 16, Backgrounds.CIRCLE_HIDDEN_GRAY_10.with_border_radius(1))
        self.setStyleSheet(style)
        self.__label_title.apply_light_mode()
        self.__label_artist.apply_light_mode()
        self.__label_length.apply_light_mode()
        self.__btn_more.apply_light_mode()
        self.__btn_love.apply_light_mode()
        self.__btn_play.apply_light_mode()
        self.__btn_close.apply_light_mode()
        self.__btn_edit_title.apply_light_mode()
        self.__btn_edit_cover.apply_light_mode()
        self.__btn_delete.apply_light_mode()
        self.__btn_add_to_playlist.apply_light_mode()
        self.__btn_remove_from_playlist.apply_light_mode()
        more_btn_bg = Background(border_radius=0.5, color=ColorBox(Colors.GRAY.with_opacity(8))).with_border_radius(1)
        self.__more_buttons.setStyleSheet(BackgroundThemeBuilder.build("QWidget", 16, more_btn_bg))

    @override
    def apply_dark_mode(self) -> None:
        style = BackgroundThemeBuilder.build("QWidget", 16, Backgrounds.CIRCLE_HIDDEN_GRAY_10.with_border_radius(1))
        self.setStyleSheet(style)
        self.__label_title.apply_dark_mode()
        self.__label_artist.apply_dark_mode()
        self.__label_length.apply_dark_mode()
        self.__btn_more.apply_dark_mode()
        self.__btn_love.apply_dark_mode()
        self.__btn_play.apply_dark_mode()
        self.__btn_close.apply_dark_mode()
        self.__btn_edit_title.apply_dark_mode()
        self.__btn_edit_cover.apply_dark_mode()
        self.__btn_delete.apply_dark_mode()
        self.__btn_add_to_playlist.apply_dark_mode()
        self.__btn_remove_from_playlist.apply_dark_mode()
        more_btn_bg = Background(border_radius=0.5, color=ColorBox(Colors.GRAY.with_opacity(8))).with_border_radius(1)
        self.__more_buttons.setStyleSheet(BackgroundThemeBuilder.build("QWidget", 16, more_btn_bg))

    def show_more(self) -> None:
        self.__buttons.hide()
        self.__btn_close.show()
        self.__more_buttons.show()

    def show_less(self) -> None:
        self.__buttons.show()
        self.__btn_close.hide()
        self.__more_buttons.hide()

    def set_onclick_play(self, fn: callable) -> None:
        self.__btn_play.clicked.connect(fn)

    def set_onclick_love(self, fn: callable) -> None:
        self.__btn_love.clicked.connect(fn)

    def set_onclick_add_to_playlist(self, fn: callable) -> None:
        self.__btn_add_to_playlist.clicked.connect(lambda: self.__clicked_add_btn(fn))

    def set_onclick_remove_from_playlist(self, fn: callable) -> None:
        self.__btn_remove_from_playlist.clicked.connect(lambda: self.__clicked_remove_btn(fn))

    def set_on_edit_cover(self, fn: callable) -> None:
        self.__btn_edit_cover.clicked.connect(lambda: fn() if self.__editable else None)

    def set_on_edit_title(self, fn: callable) -> None:
        self.__btn_edit_title.clicked.connect(lambda: fn() if self.__editable else None)

    def set_on_delete(self, fn: callable) -> None:
        self.__btn_delete.clicked.connect(lambda: fn() if self.__removeable else None)

    def __clicked_add_btn(self, fn: callable) -> None:
        self.__btn_remove_from_playlist.show()
        self.__btn_add_to_playlist.hide()
        fn()

    def __clicked_remove_btn(self, fn: callable) -> None:
        self.__btn_add_to_playlist.show()
        self.__btn_remove_from_playlist.hide()
        fn()

    def enable_edit(self, value: bool) -> None:
        self.__editable = value
        self.__btn_edit_title.setVisible(value)
        self.__btn_edit_cover.setVisible(value)

    def enable_delete(self, value: bool) -> None:
        self.__removeable = value
        self.__btn_delete.setVisible(value)

    def set_cover(self, cover: Union[bytes, None]) -> None:
        self.__cover.set_cover(self.__get_cover_from_bytes(cover))

    def set_title(self, title: str = "Song Title") -> None:
        self.__label_title.setText(title)

    def set_artist(self, artist: str) -> None:
        self.__label_artist.setText(artist or self.default_artist)

    def set_length(self, length: float = 0) -> None:
        self.__label_length.setText(Times.string_of(length))

    def set_love_state(self, state: bool) -> None:
        self.__btn_love.set_active(state)

    def set_default_cover(self, cover: bytes) -> None:
        self.__cover.set_default_cover(self.__get_cover_from_bytes(cover))

    def set_default_artist(self, artist: str) -> None:
        self.default_artist = artist

    def clear_info(self):
        self.set_cover(None)

    def get_title(self):
        return self.__label_title.text()

    def get_artist(self):
        return self.__label_artist.text()

    def set_is_choosing(self, is_choosing: bool) -> None:
        if is_choosing:
            self.__btn_remove_from_playlist.show()
            self.__btn_add_to_playlist.hide()
        else:
            self.__btn_remove_from_playlist.hide()
            self.__btn_add_to_playlist.show()

    def enable_choosing(self, is_choosing: bool) -> None:
        if is_choosing:
            self.__choosing_playlist_buttons.show()
            self.__buttons.hide()
        else:
            self.__choosing_playlist_buttons.hide()
            self.__buttons.show()

    @staticmethod
    def __create_button(with_icon: AppIcon,
                        padding=Paddings.RELATIVE_50,
                        color=Colors.PRIMARY,
                        background=Backgrounds.CIRCLE_HIDDEN_PRIMARY_10) -> IconButton:
        return IconButton.build(
            size=Icons.LARGE,
            padding=padding,
            style=IconButtonStyle(
                light_mode_icon=with_icon.with_color(color),
                light_mode_background=background,
            ),
        )

    @staticmethod
    def __create_label(
        with_font: QFont,
        light_mode_text_color=ColorBoxes.GRAY,
        dark_mode_text_color=ColorBoxes.WHITE
    ) -> LabelWithDefaultText:
        return LabelWithDefaultText.build(
            with_font,
            light_mode_style=TextStyle(text_color=light_mode_text_color),
            dark_mode_style=TextStyle(text_color=dark_mode_text_color)
        )

    @staticmethod
    def __get_cover_from_bytes(cover_byte: bytes) -> Union[CoverProp, None]:
        if cover_byte is None:
            return None
        return CoverProp.from_bytes(cover_byte, width=64, height=64, radius=12)
