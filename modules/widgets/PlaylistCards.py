from typing import Optional, Callable

from PyQt5.QtCore import pyqtSignal, QEvent, Qt, QRect
from PyQt5.QtGui import QFont, QCursor, QResizeEvent, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QFileDialog

from modules.helpers import Pixmaps
from modules.helpers.types.Decorators import override
from modules.models.view.Animation import Animation
from modules.models.view.builder.IconButtonStyle import IconButtonStyle
from modules.models.view.builder.TextStyle import TextStyle
from modules.statics import Properties
from modules.statics.view.Material import ColorBoxes, Paddings, Icons, Colors, Backgrounds, Images
from modules.widgets.Buttons import IconButton
from modules.widgets.Cover import Cover, CoverProp
from modules.widgets.Dialogs import Dialogs
from modules.widgets.Labels import LabelWithDefaultText, DoubleClickedEditableLabel


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
        self._adapt_theme_to_cover(self._cover.current_cover())
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
    _buttons: QHBoxLayout
    __delete_btn: IconButton
    _cover: Cover
    _label: DoubleClickedEditableLabel
    __onchange_cover_fn: Callable[[str], None]
    __delete_fn: Callable[[], None]

    def __init__(self, font: QFont, parent: Optional["QWidget"] = None):
        super().__init__(font, parent)

    def _init_ui(self, font: QFont) -> None:
        self._main_layout = QVBoxLayout(self)
        self._main_layout.setContentsMargins(20, 20, 20, 20)

        self.__edit_cover_btn = IconButton.build(
            padding=Paddings.RELATIVE_50,
            size=Icons.MEDIUM,
            style=IconButtonStyle(
                light_mode_icon=Icons.EDIT.with_color(Colors.PRIMARY),
                light_mode_background=Backgrounds.CIRCLE_PRIMARY_10,
                dark_mode_icon=Icons.EDIT.with_color(Colors.WHITE),
                dark_mode_background=Backgrounds.CIRCLE_PRIMARY_75,
            ),
        )
        self.__edit_cover_btn.apply_light_mode()
        self.__edit_cover_btn.clicked.connect(
            lambda: self.__onclick_select_cover() if self.__onchange_cover_fn is not None else None)

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
        self.__delete_btn.clicked.connect(lambda: self.__on_click_delete())

        self._buttons = QHBoxLayout()
        self._buttons.setContentsMargins(0, 0, 0, 0)
        self._buttons.addStretch()
        self._buttons.addWidget(self.__edit_cover_btn)
        self._buttons.addWidget(self.__delete_btn)

        self._cover = Cover(self)
        self._label = DoubleClickedEditableLabel.build(
            font=font,
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            dark_mode_style=TextStyle(text_color=ColorBoxes.WHITE),
            parent=self,
        )
        self._label.setFixedHeight(32)
        self._label.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))

        self._main_layout.addLayout(self._buttons)
        self._main_layout.addStretch()
        self._main_layout.addWidget(self._label)

    def __on_click_delete(self):
        Dialogs().confirm(
            image=Images.DELETE,
            header="Warning",
            message="Are you sure want to delete this playlist? The playlist will be deleted permanently.",
            accept_text="Delete",
            cancel_text="Cancel",
            on_accept=lambda: self.__delete_fn() if self.__delete_fn is not None else None
        )

    def set_onchange_cover(self, fn: Callable[[str], None]) -> None:
        self.__onchange_cover_fn = fn

    def set_ondelete(self, fn: Callable[[], None]) -> None:
        self.__delete_fn = fn

    def set_onchange_title(self, fn: Callable[[str], None]) -> None:
        self._label.set_onchange_text(fn)

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
            self.__delete_btn.apply_dark_mode()
            self.__edit_cover_btn.apply_dark_mode()
        else:
            self.__delete_btn.apply_light_mode()
            self.__edit_cover_btn.apply_light_mode()

    def __get_button_rect(self) -> QRect:
        return QRect(self.__edit_cover_btn.pos().x(),
                     self.__edit_cover_btn.pos().y(),
                     self.__edit_cover_btn.rect().width() + self.__delete_btn.rect().width(),
                     self.__edit_cover_btn.rect().height())
