from typing import Optional, Union, Callable

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout

from modules.helpers.types.Decorators import override
from modules.helpers.types.Strings import Strings
from modules.models.view.Background import Background
from modules.models.view.Border import Border
from modules.models.view.ColorBox import ColorBox
from modules.models.view.builder.BackgroundThemeBuilder import BackgroundThemeBuilder
from modules.models.view.builder.FontBuilder import FontBuilder
from modules.models.view.builder.IconButtonStyle import IconButtonStyle
from modules.models.view.builder.TextStyle import TextStyle
from modules.screens.AbstractScreen import BaseView
from modules.statics.view.Material import Icons, Paddings, Colors, Backgrounds, ColorBoxes, Cursors
from modules.widgets import Observers, Dialogs
from modules.widgets.Buttons import ToggleIconButton, IconButton
from modules.widgets.Cover import Cover, CoverProp
from modules.widgets.Icons import AppIcon
from modules.widgets.Labels import LabelWithDefaultText, Input
from modules.widgets.Widgets import BackgroundWidget


class RenameSongDialog(Dialogs.ConfirmDialog):
    def __init__(self, header: str, msg: str | None = None, accept_text: str = "Confirm", reject_text: str = "Cancel",
                 onclick_accept_fn: Callable[[str], str] = None, onclick_reject_fn: callable = None,
                 dark_mode: bool = False,
                 parent: Optional["QWidget"] = None):
        super().__init__(header, msg, accept_text, reject_text, onclick_accept_fn, onclick_reject_fn, dark_mode, parent)

    def _init_content(self, content: QWidget) -> None:
        layout = QVBoxLayout(content)
        self.__input = Input.build(
            font=FontBuilder.build(size=12),
            light_mode_style=TextStyle(text_color=ColorBoxes.PRIMARY,
                                       background=Background(
                                           border_radius=8,
                                           color=ColorBox(normal=Colors.PRIMARY.with_opacity(10)),
                                           border=Border(size=2, color=Colors.PRIMARY))
                                       ),
            padding=8
        )
        self.__input.set_onpressed(self._on_accepted)
        self.__input.setFixedHeight(48)
        layout.addWidget(self.__input)

    @override
    def _get_onclick_accept_fn(self) -> callable:
        return lambda: self._onclick_accept_fn(self.__input.text())

    @override
    def apply_dark_mode(self) -> None:
        super().apply_dark_mode()
        self.__input.apply_dark_mode()

    @override
    def apply_light_mode(self) -> None:
        super().apply_light_mode()
        self.__input.apply_light_mode()


class SongTableRowView(BackgroundWidget, BaseView):
    __main_layout: QHBoxLayout
    __info: QHBoxLayout
    __buttons: QWidget
    __buttons_layout: QHBoxLayout
    __cover: Cover
    __label_title: LabelWithDefaultText
    __label_artist: LabelWithDefaultText
    __label_length: LabelWithDefaultText
    __btn_more: IconButton
    __btn_love: ToggleIconButton
    __btn_play: IconButton
    __btn_edit: IconButton
    __btn_add_to_playlist: IconButton
    __btn_delete: IconButton
    __btn_close: IconButton
    __cover_observer: Observers.ClickObserver

    __editable: bool = False

    def __init__(self, parent: Optional["QWidget"] = None):
        super(SongTableRowView, self).__init__(parent)
        self.default_artist = ""
        self.__init_ui()

    def __init_ui(self) -> None:
        font = FontBuilder.build(size=10)

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.__main_layout = QHBoxLayout()
        self.__main_layout.setContentsMargins(20, 12, 20, 12)
        self.__main_layout.setSpacing(0)
        self.__main_layout.setAlignment(Qt.AlignLeft)
        self.setLayout(self.__main_layout)

        self.__info = QHBoxLayout()
        self.__info.setSpacing(24)
        self.__info.setContentsMargins(0, 8, 0, 8)

        self.__buttons = QWidget()
        self.__buttons_layout = QHBoxLayout(self.__buttons)
        self.__buttons_layout.setContentsMargins(8, 8, 8, 8)
        self.__buttons_layout.setSpacing(8)

        self.__choosing_playlist_buttons = QWidget()
        self.__choosing_playlist_buttons_layout = QHBoxLayout(self.__choosing_playlist_buttons)
        self.__choosing_playlist_buttons_layout.setSpacing(8)
        self.__choosing_playlist_buttons_layout.setContentsMargins(8, 8, 8, 8)

        self.__cover = Cover(self)
        self.__cover.setFixedSize(64, 64)
        self.__cover_observer = Observers.observe_click_of(self.__cover)

        self.__label_title = self.__create_label(with_font=font, light_mode_text_color=ColorBoxes.BLACK)
        self.__label_title.setFixedWidth(188)
        self.__title_observer = Observers.observe_click_of(self.__label_title)

        self.__label_artist = self.__create_label(with_font=font)
        self.__label_artist.setFixedWidth(128)

        self.__label_length = self.__create_label(with_font=font)
        self.__label_length.setFixedWidth(64)
        self.__label_length.setAlignment(Qt.AlignCenter)

        self.__btn_more = self.__create_button(with_icon=Icons.MORE)
        # self.__btn_more.clicked.connect(lambda: self.show_more())

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

        self.__btn_add_to_playlist = self.__create_button(with_icon=Icons.ADD, padding=Paddings.RELATIVE_75)
        self.__btn_add_to_playlist = self.__create_button(with_icon=Icons.ADD, padding=Paddings.RELATIVE_67)
        self.__btn_remove_from_playlist = self.__create_button(with_icon=Icons.MINUS,
                                                               padding=Paddings.RELATIVE_33,
                                                               color=Colors.DANGER,
                                                               background=Backgrounds.CIRCLE_HIDDEN_DANGER_10)
        self.__btn_remove_from_playlist.hide()

        self.__main_layout.addLayout(self.__info)
        self.__main_layout.addWidget(self.__buttons)
        self.__main_layout.addWidget(self.__choosing_playlist_buttons)

        self.__info.addWidget(self.__cover)
        self.__info.addWidget(self.__label_title, 1)
        self.__info.addWidget(self.__label_artist, 1)
        self.__info.addWidget(self.__label_length)

        self.__buttons_layout.addWidget(self.__btn_more)
        self.__buttons_layout.addWidget(self.__btn_love)
        self.__buttons_layout.addWidget(self.__btn_play)

        self.__choosing_playlist_buttons_layout.addStretch(0)
        self.__choosing_playlist_buttons_layout.addWidget(self.__btn_add_to_playlist)
        self.__choosing_playlist_buttons_layout.addWidget(self.__btn_remove_from_playlist)

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
        self.__btn_add_to_playlist.apply_light_mode()
        self.__btn_remove_from_playlist.apply_light_mode()

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
        self.__btn_add_to_playlist.apply_dark_mode()
        self.__btn_remove_from_playlist.apply_dark_mode()

    def set_onclick_play(self, fn: callable) -> None:
        self.__btn_play.clicked.connect(fn)

    def set_onclick_love(self, fn: callable) -> None:
        self.__btn_love.clicked.connect(fn)

    def set_onclick_add_to_playlist(self, fn: callable) -> None:
        self.__btn_add_to_playlist.clicked.connect(lambda: self.__clicked_add_btn(fn))

    def set_onclick_remove_from_playlist(self, fn: callable) -> None:
        self.__btn_remove_from_playlist.clicked.connect(lambda: self.__clicked_remove_btn(fn))

    def set_on_doubleclick_cover(self, fn: callable) -> None:
        self.__cover_observer.set_on_doubleclick_fn(lambda: fn() if self.__editable else None)

    def set_on_edit_title(self, fn: callable) -> None:
        self.__btn_more.clicked.connect(lambda: fn() if self.__editable else None)

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
        self.__cover.setCursor(Cursors.HAND if self.__editable else Cursors.DEFAULT)

    def set_cover(self, cover: Union[bytes, None]) -> None:
        self.__cover.set_cover(self.__get_cover_from_bytes(cover))

    def set_title(self, title: str = "Song Title") -> None:
        self.__label_title.setText(title)

    def set_artist(self, artist: str) -> None:
        self.__label_artist.setText(artist or self.default_artist)

    def set_length(self, length: float = 0) -> None:
        self.__label_length.setText(Strings.float_to_clock_time(length))

    def set_love_state(self, state: bool) -> None:
        self.__btn_love.set_active(state)

    def set_default_cover(self, cover: bytes) -> None:
        self.__cover.set_default_cover(self.__get_cover_from_bytes(cover))

    def set_default_artist(self, artist: str) -> None:
        self.default_artist = artist

    def clear_info(self):
        self.set_cover(None)

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
