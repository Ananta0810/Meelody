from typing import Optional, Callable

from PyQt5.QtCore import pyqtSignal, QEvent, Qt
from PyQt5.QtGui import QFont, QCursor, QResizeEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from modules.helpers.types.Decorators import override
from modules.models.view.Animation import Animation
from modules.models.view.builder.TextStyle import TextStyle
from modules.statics.view.Material import ColorBoxes
from modules.widgets.Cover import Cover
from modules.widgets.ImageViewer import ImageViewer
from modules.widgets.LabelWithDefaultText import LabelWithDefaultText


class PlaylistCard(QWidget):
    __main_layout: QVBoxLayout
    __label: LabelWithDefaultText
    __cover: ImageViewer

    def __init__(self, font: QFont, parent: Optional["QWidget"] = None):
        super().__init__(parent)
        self.__onclick_fn = None
        self.clicked: pyqtSignal = pyqtSignal()
        self.__init_component_ui(font)

    def __init_component_ui(self, font: QFont) -> None:
        self.__main_layout = QVBoxLayout(self)
        self.__main_layout.setContentsMargins(20, 20, 20, 20)
        self.__cover = ImageViewer(self)
        self.__label = LabelWithDefaultText.build(
            font=font,
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            parent=self,
        )
        self.__label.setFixedSize(160, 32)
        self.__main_layout.addStretch()
        self.__main_layout.addWidget(self.__label)

    @override
    def resizeEvent(self, event: QResizeEvent) -> None:
        self.__cover.setFixedSize(self.size())
        return super().resizeEvent(event)

    @override
    def enterEvent(self, event: QEvent) -> None:
        super().enterEvent(event)
        self.__cover.animation_on_entered_hover()

    @override
    def leaveEvent(self, event: QEvent) -> None:
        super().leaveEvent(event)
        self.__cover.animation_on_left_hover()

    @override
    def mousePressEvent(self, event) -> None:
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton and self.__onclick_fn is not None:
            self.__onclick_fn()

    @override
    def setCursor(self, cursor: QCursor) -> None:
        super().setCursor(cursor)
        self.__label.setCursor(cursor)

    def set_onclick_fn(self, fn: Callable[[], None]) -> None:
        self.__onclick_fn = fn

    def set_cover(self, pixmap: Cover) -> None:
        self.__cover.set_cover(pixmap)

    def set_default_cover(self, pixmap: Cover) -> None:
        self.__cover.set_default_cover(pixmap)

    def set_label_text(self, text: str) -> None:
        self.__label.setText(text)

    def set_label_default_text(self, text: str) -> None:
        self.__label.set_default_text(text)

    def set_animation(self, animation: Animation) -> None:
        self.__cover.set_animation(
            duration=animation.duration_in_ms,
            start=animation.start,
            end=animation.end,
            on_value_changed=self.__cover.zoom
        )
