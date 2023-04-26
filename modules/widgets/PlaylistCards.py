from typing import Optional, Callable

from PyQt5.QtCore import pyqtSignal, QEvent, Qt
from PyQt5.QtGui import QFont, QCursor, QResizeEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QFileDialog

from modules.helpers.types.Decorators import override
from modules.models.view.Animation import Animation
from modules.models.view.builder.IconButtonStyle import IconButtonStyle
from modules.models.view.builder.TextStyle import TextStyle
from modules.statics.view.Material import ColorBoxes, Paddings, Icons, Colors, Backgrounds
from modules.widgets.Cover import Cover
from modules.widgets.IconButton import IconButton
from modules.widgets.ImageViewer import ImageViewer
from modules.widgets.LabelWithDefaultText import LabelWithDefaultText, DoubleClickedEditableLabel


class PlaylistCard(QWidget):
    _main_layout: QVBoxLayout
    _label: LabelWithDefaultText
    _cover: ImageViewer

    def __init__(self, font: QFont, parent: Optional["QWidget"] = None):
        super().__init__(parent)
        self.__onclick_fn: Callable[[], None] = None
        self.clicked: pyqtSignal = pyqtSignal()
        self._init_ui(font)

    def _init_ui(self, font: QFont) -> None:
        self._main_layout = QVBoxLayout(self)
        self._main_layout.setContentsMargins(20, 20, 20, 20)
        self._cover = ImageViewer(self)
        self._label = LabelWithDefaultText.build(
            font=font,
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            parent=self,
        )
        self._label.setFixedSize(160, 32)
        self._main_layout.addStretch()
        self._main_layout.addWidget(self._label)

    @override
    def resizeEvent(self, event: QResizeEvent) -> None:
        self._cover.setFixedSize(self.size())
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

    def set_cover(self, pixmap: Cover) -> None:
        self._cover.set_cover(pixmap)

    def set_default_cover(self, pixmap: Cover) -> None:
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
    _cover: ImageViewer
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
                light_mode_background=Backgrounds.CIRCLE_PRIMARY_10
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
                light_mode_background=Backgrounds.CIRCLE_DANGER_10
            ),
        )
        self.__delete_btn.apply_light_mode()
        self.__delete_btn.clicked.connect(lambda: self.__delete_fn() if self.__delete_fn is not None else None)

        self._buttons = QHBoxLayout()
        self._buttons.setContentsMargins(0, 0, 0, 0)
        self._buttons.addStretch()
        self._buttons.addWidget(self.__edit_cover_btn)
        self._buttons.addWidget(self.__delete_btn)

        self._cover = ImageViewer(self)
        self._label = DoubleClickedEditableLabel.build(
            font=font,
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            parent=self,
        )
        self._label.setFixedHeight(32)
        self._label.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))

        self._main_layout.addLayout(self._buttons)
        self._main_layout.addStretch()
        self._main_layout.addWidget(self._label)

    def set_onchange_cover(self, fn: Callable[[str], None]) -> None:
        self.__onchange_cover_fn = fn

    def set_ondelete(self, fn: Callable[[], None]) -> None:
        self.__delete_fn = fn

    def set_onchange_title(self, fn: Callable[[str], None]) -> None:
        self._label.set_onchange_text(fn)

    def __onclick_select_cover(self) -> None:
        path = QFileDialog.getOpenFileName(self, filter="JPEG, PNG (*.JPEG *.jpeg *.JPG *.jpg *.JPE *.jpe)")[0]
        if path is not None and path != '':
            self.__onchange_cover_fn(path)
