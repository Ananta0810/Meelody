from typing import Optional, Callable

from PyQt5.QtCore import pyqtSignal, QEvent, Qt, QRect, QSize
from PyQt5.QtGui import QFont, QCursor, QResizeEvent, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QFileDialog

from modules.helpers import Pixmaps
from modules.helpers.types.Decorators import override, connector
from modules.models.view.Animation import Animation
from modules.models.view.Background import Background
from modules.models.view.Border import Border
from modules.models.view.Color import Color
from modules.models.view.ColorBox import ColorBox
from modules.models.view.Padding import Padding
from modules.models.view.builder.FontBuilder import FontBuilder
from modules.models.view.builder.IconButtonStyle import IconButtonStyle
from modules.models.view.builder.TextStyle import TextStyle
from modules.statics import Properties
from modules.statics.view.Material import ColorBoxes, Paddings, Icons, Colors, Backgrounds, Images
from modules.widgets import Dialogs
from modules.widgets.Buttons import IconButton, ActionButton
from modules.widgets.Cover import Cover, CoverProp
from modules.widgets.Labels import LabelWithDefaultText, Input


class UpdatePlaylistWindow(Dialogs.Dialog):
    __on_accept_fn: Callable[[str], bool] = None
    __onclick_choose_cover: callable = None

    @override
    def _build_content(self):
        self.__cover = Cover()
        cover_edge = 360 - self.contentsMargins().left() - self.contentsMargins().right()
        self.__cover.setFixedSize(cover_edge, cover_edge)

        self.__label_title = LabelWithDefaultText.build(
            font=FontBuilder.build(size=11),
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            dark_mode_style=TextStyle(text_color=ColorBoxes.WHITE),
        )
        self.__input_title = Input.build(
            font=FontBuilder.build(size=12),
            light_mode_style=TextStyle(
                text_color=ColorBoxes.BLACK,
                background=(
                    Background(border_radius=8,
                               color=ColorBox(normal=Colors.GRAY.with_opacity(8)),
                               border=Border(size=2, color=ColorBox(Color(216, 216, 216)))
                               )
                )
            ),
            padding=8
        )
        self.__input_title.setFixedHeight(48)
        self.__input_title.set_onpressed(lambda title: self._on_accepted())

        self.__accept_btn = ActionButton.build(
            font=FontBuilder.build(family="Segoe UI Semibold", size=11),
            size=QSize(0, 48),
            light_mode=TextStyle(text_color=ColorBoxes.WHITE,
                                 background=Backgrounds.ROUNDED_PRIMARY_75.with_border_radius(8)),
            dark_mode=TextStyle(text_color=ColorBoxes.WHITE, background=Backgrounds.ROUNDED_WHITE_25)
        )

        self.__view_layout = QVBoxLayout(self)
        self.__view_layout.setContentsMargins(0, 12, 0, 0)
        self.__view_layout.setAlignment(Qt.AlignVCenter)
        self.__view_layout.addWidget(self.__cover)
        self.__view_layout.addWidget(self.__label_title)
        self.__view_layout.addWidget(self.__input_title)
        self.__view_layout.addSpacing(8)
        self.__view_layout.addWidget(self.__accept_btn)

        self.__edit_cover_btn = ActionButton.build(
            font=FontBuilder.build(family="Segoe UI Semibold", size=9),
            padding=Padding(12, 12),
            light_mode=TextStyle(text_color=ColorBoxes.WHITE,
                                 background=Backgrounds.ROUNDED_PRIMARY.with_border_radius(8)),
            dark_mode=TextStyle(text_color=ColorBoxes.WHITE, background=Backgrounds.ROUNDED_WHITE_25),
            parent=self
        )
        self.__edit_cover_btn.setText("Choose cover")
        self.__edit_cover_btn.apply_light_mode()

        self.__label_title.setText("Enter title")
        self.__accept_btn.setText("Apply")

        self.setFixedWidth(360)
        self.setFixedHeight(self.sizeHint().height())

        self.__accept_btn.clicked.connect(self._on_accepted)
        self.__edit_cover_btn.clicked.connect(lambda: self.__onclick_choose_cover())

    @override
    def apply_dark_mode(self) -> None:
        super().apply_dark_mode()
        self.__label_title.apply_dark_mode()
        self.__input_title.apply_dark_mode()
        self.__accept_btn.apply_dark_mode()

    @override
    def apply_light_mode(self) -> None:
        super().apply_light_mode()
        self.__label_title.apply_light_mode()
        self.__input_title.apply_light_mode()
        self.__accept_btn.apply_light_mode()

    @override
    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self.__input_title.setFixedWidth(self.__accept_btn.size().width())
        self.__edit_cover_btn.move(
            self.__cover.x() + self.__cover.width() - self.__edit_cover_btn.width() - 8,
            self.__cover.y() + 8,
        )

    @connector
    def on_apply_change(self, fn: Callable[[str], bool]) -> None:
        self.__on_accept_fn = fn

    @connector
    def onclick_choose_cover(self, fn: callable) -> None:
        self.__onclick_choose_cover = fn

    def set_cover(self, cover: bytes) -> None:
        self.__cover.set_cover(CoverProp.from_bytes(cover, self.__cover.width(), self.__cover.height(), radius=16))

    def set_song_title(self, title: str) -> None:
        self.__input_title.setText(title)

    def _on_accepted(self) -> None:
        if self.__on_accept_fn is None:
            super()._on_accepted()
            return

        can_close = self.__on_accept_fn(self.__input_title.text())
        if can_close:
            super()._on_accepted()

    def __onclick_select_cover(self) -> None:
        path = QFileDialog.getOpenFileName(self, filter=Properties.ImportType.IMAGE)[0]
        if path is not None and path != '':
            self.__onchange_cover_fn(path)


class PlaylistCard(QWidget):
    _main_layout: QVBoxLayout
    _label: LabelWithDefaultText
    _cover: Cover

    __onclick_fn: Callable[[], None] = None

    def __init__(self, font: QFont, parent: Optional["QWidget"] = None):
        super().__init__(parent)
        self.clicked: pyqtSignal = pyqtSignal()
        self._init_ui(font)
        self.installEventFilter(self)

    def _init_ui(self, font: QFont) -> None:
        self._main_layout = QVBoxLayout(self)
        self._main_layout.setContentsMargins(20, 20, 20, 20)
        self._cover = Cover(self)
        self._label = LabelWithDefaultText.build(
            font=font,
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            dark_mode_style=TextStyle(text_color=ColorBoxes.WHITE),
            parent=self,
        )
        self._label.setFixedSize(160, 32)
        self._main_layout.addStretch()
        self._main_layout.addWidget(self._label)

    @override
    def resizeEvent(self, event: QResizeEvent) -> None:
        self._cover.setFixedSize(self.size())
        self._adapt_theme_to_cover(self._cover.current_cover().content())
        return super().resizeEvent(event)

    @override
    def enterEvent(self, event: QEvent) -> None:
        super().enterEvent(event)
        self._cover.animation_on_entered_hover()

    @override
    def leaveEvent(self, event: QEvent) -> None:
        super().leaveEvent(event)
        self._cover.animation_on_left_hover()

    @override
    def mousePressEvent(self, event) -> None:
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton and self.__onclick_fn is not None:
            self.__onclick_fn()

    @override
    def setCursor(self, cursor: QCursor) -> None:
        super().setCursor(cursor)
        self._label.setCursor(cursor)

    def set_onclick_fn(self, fn: Callable[[], None]) -> None:
        self.__onclick_fn = fn

    def set_cover(self, pixmap: CoverProp) -> None:
        self._cover.set_cover(pixmap)
        self._adapt_theme_to_cover(pixmap.content())

    def _adapt_theme_to_cover(self, pixmap: QPixmap):
        rect = self.__get_label_rect()
        should_dark_mode_for_label = Pixmaps.check_contrast_at(pixmap, rect)
        if should_dark_mode_for_label:
            self._label.apply_dark_mode()
        else:
            self._label.apply_light_mode()

    def __get_label_rect(self):
        return QRect(self._label.pos().x(),
                     self._label.pos().y(),
                     self._label.rect().width(),
                     self._label.rect().height())

    def set_default_cover(self, pixmap: CoverProp) -> None:
        self._cover.set_default_cover(pixmap)

    def set_label_text(self, text: str) -> None:
        self._label.setText(text)

    def set_label_default_text(self, text: str) -> None:
        self._label.set_default_text(text)

    def set_animation(self, animation: Animation) -> None:
        self._cover.set_animation(
            duration=animation.duration_in_ms,
            start=animation.start,
            end=animation.end,
            on_value_changed=self._cover.zoom
        )


class EditablePlaylistCard(PlaylistCard):
    _main_layout: QVBoxLayout
    __buttons: QHBoxLayout
    __delete_btn: IconButton
    _cover: Cover
    _label: LabelWithDefaultText
    __onchange_cover_fn: Callable[[str], None]
    __onchange_title_fn: Callable[[str], bool]
    __delete_fn: Callable[[], None]

    def __init__(self, font: QFont, parent: Optional["QWidget"] = None):
        super().__init__(font, parent)

    def _init_ui(self, font: QFont) -> None:
        self.__edit_title_btn = IconButton.build(
            padding=Paddings.RELATIVE_50,
            size=Icons.MEDIUM,
            style=IconButtonStyle(
                light_mode_icon=Icons.EDIT.with_color(Colors.PRIMARY),
                light_mode_background=Backgrounds.CIRCLE_PRIMARY_10,
                dark_mode_icon=Icons.EDIT.with_color(Colors.WHITE),
                dark_mode_background=Backgrounds.CIRCLE_PRIMARY_75,
            ),
        )
        self.__edit_title_btn.apply_light_mode()
        self.__edit_title_btn.clicked.connect(lambda: self.__open_dialog())

        self.__delete_btn = IconButton.build(
            padding=Paddings.RELATIVE_50,
            size=Icons.MEDIUM,
            style=IconButtonStyle(
                light_mode_icon=Icons.DELETE.with_color(Colors.DANGER),
                light_mode_background=Backgrounds.CIRCLE_DANGER_10,
                dark_mode_icon=Icons.DELETE.with_color(Colors.WHITE),
                dark_mode_background=Backgrounds.CIRCLE_DANGER_75,
            ),
        )
        self.__delete_btn.apply_light_mode()

        self.__buttons = QVBoxLayout()
        self.__buttons.setContentsMargins(0, 0, 0, 0)
        self.__buttons.addWidget(self.__edit_title_btn)
        self.__buttons.addWidget(self.__delete_btn)

        top_layout = QHBoxLayout()
        top_layout.addStretch(1)
        top_layout.addLayout(self.__buttons)

        self._cover = Cover(self)
        self._label = LabelWithDefaultText.build(
            font=font,
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            dark_mode_style=TextStyle(text_color=ColorBoxes.WHITE),
            parent=self,
        )
        self._label.setFixedHeight(32)
        self._label.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))

        self._main_layout = QVBoxLayout(self)
        self._main_layout.setContentsMargins(20, 20, 20, 20)
        self._main_layout.addLayout(top_layout)
        self._main_layout.addStretch()
        self._main_layout.addWidget(self._label)

        self.__delete_btn.clicked.connect(lambda: self.__on_click_delete())

        self.__update_dialog = UpdatePlaylistWindow()

    def __open_dialog(self) -> None:
        self.__update_dialog.set_song_title(self._label.text())
        self.__update_dialog.set_cover(self._cover.current_cover().data())
        self.__update_dialog.on_apply_change(self.__on_change_title)
        self.__update_dialog.onclick_choose_cover(
            lambda: self.__onclick_select_cover() if self.__onchange_cover_fn is not None else None)
        Dialogs.Dialogs.show_dialog(self.__update_dialog)

    def __on_change_title(self, title: str) -> bool:
        changed_success = self.__onchange_title_fn(title)
        if changed_success:
            self.set_label_text(title)
        return changed_success

    def __on_click_delete(self) -> None:
        Dialogs.Dialogs.confirm(
            image=Images.DELETE,
            header="Warning",
            message="Are you sure want to delete this playlist?\n The playlist will be deleted permanently.",
            accept_text="Delete",
            cancel_text="Cancel",
            on_accept=lambda: self.__delete_fn() if self.__delete_fn is not None else None
        )

    def set_onchange_cover(self, fn: Callable[[str], None]) -> None:
        self.__onchange_cover_fn = fn

    def set_ondelete(self, fn: Callable[[], None]) -> None:
        self.__delete_fn = fn

    def set_onchange_title(self, fn: Callable[[str], bool]) -> None:
        self.__onchange_title_fn = fn

    @override
    def set_cover(self, pixmap: CoverProp) -> None:
        super().set_cover(pixmap)
        self.__update_dialog.set_cover(pixmap.data())

    def __onclick_select_cover(self) -> None:
        path = QFileDialog.getOpenFileName(self, filter=Properties.ImportType.IMAGE)[0]
        if path is not None and path != '':
            self.__onchange_cover_fn(path)

    @override
    def _adapt_theme_to_cover(self, pixmap: QPixmap) -> None:
        super()._adapt_theme_to_cover(pixmap)
        rect = self.__get_button_rect()
        should_dark_mode_for_buttons = Pixmaps.check_contrast_at(pixmap, rect)
        if should_dark_mode_for_buttons:
            self.__edit_title_btn.apply_dark_mode()
            self.__delete_btn.apply_dark_mode()
        else:
            self.__edit_title_btn.apply_light_mode()
            self.__delete_btn.apply_light_mode()

    def __get_button_rect(self) -> QRect:
        return QRect(self.__edit_title_btn.pos().x(),
                     self.__edit_title_btn.pos().y(),
                     self.__edit_title_btn.rect().width() + self.__delete_btn.rect().width(),
                     self.__edit_title_btn.rect().height())
