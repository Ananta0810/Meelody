from typing import Optional, Callable

from PyQt5.QtCore import pyqtSignal, QEvent, Qt
from PyQt5.QtGui import QFont, QCursor, QResizeEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from modules.helpers.types.Decorators import override
from modules.models.view.Animation import Animation
from modules.models.view.builder.IconButtonStyle import IconButtonStyle
from modules.models.view.builder.TextStyle import TextStyle
from modules.statics.view.Material import ColorBoxes, Paddings, Icons, Colors, Backgrounds
from modules.widgets.Cover import Cover
from modules.widgets.IconButton import IconButton
from modules.widgets.ImageViewer import ImageViewer
from modules.widgets.LabelWithDefaultText import LabelWithDefaultText, EditableLabelWithDefaultText


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
    def __init__(self, font: QFont, parent: Optional["QWidget"] = None):
        super().__init__(font, parent)

    def _init_ui(self, font: QFont) -> None:
        self._main_layout = QVBoxLayout(self)
        self._main_layout.setContentsMargins(20, 20, 20, 20)

        self._delete_btn = IconButton.build(
            padding=Paddings.RELATIVE_50,
            size=Icons.MEDIUM,
            style=IconButtonStyle(
                light_mode_icon=Icons.DELETE.with_color(Colors.DANGER),
                light_mode_background=Backgrounds.CIRCLE_DANGER_10
            ),
        )
        self._delete_btn.apply_light_mode()

        self._buttons = QHBoxLayout()
        self._buttons.setContentsMargins(0, 0, 0, 0)
        self._buttons.addStretch()
        self._buttons.addWidget(self._delete_btn)

        self._cover = ImageViewer(self)
        self._label = EditableLabelWithDefaultText.build(
            font=font,
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            parent=self,
        )
        self._label.setFixedSize(160, 32)

        self._main_layout.addLayout(self._buttons)
        self._main_layout.addStretch()
        self._main_layout.addWidget(self._label)

    def set_ondelete(self, fn: Callable[[], None]) -> None:
        self._delete_btn.clicked.connect(lambda: fn())

    # def set_onchange_title(self, fn: Callable[[], None]) -> None:
    #     self._delete_btn.clicked.connect(lambda: fn())
