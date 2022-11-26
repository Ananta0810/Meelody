from typing import Self, Optional

from PyQt5.QtCore import pyqtSignal, QEvent
from PyQt5.QtGui import QFont, QCursor, QPixmap, QResizeEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from modules.helpers.types.Decorators import override
from modules.models.view.Animation import Animation
from modules.models.view.builder.TextStyle import TextStyle
from modules.statics.view.Material import ColorBoxes
from modules.widgets.ImageViewer import ImageViewer
from modules.widgets.LabelWithDefaultText import LabelWithDefaultText


class DefaultPlaylistCard(QWidget):
    main_layout: QVBoxLayout
    label: LabelWithDefaultText
    cover: ImageViewer

    def __init__(self, font: QFont, parent: Optional["QWidget"] = None) -> Self:
        super().__init__(parent)
        self.clicked: pyqtSignal = pyqtSignal()
        self.setup_ui(font)

    def setup_ui(self, font: QFont) -> None:
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.cover = ImageViewer(self)
        self.label = LabelWithDefaultText.build(
            font=font,
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            parent=self,
        )
        self.label.setFixedSize(160, 32)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.label)

    @override
    def resizeEvent(self, event: QResizeEvent) -> None:
        self.cover.setFixedSize(self.size())
        return super().resizeEvent(event)

    @override
    def enterEvent(self, event: QEvent) -> None:
        super().enterEvent(event)
        self.cover.animation_on_entered_hover()

    @override
    def leaveEvent(self, event: QEvent) -> None:
        super().leaveEvent(event)
        self.cover.animation_on_left_hover()

    @override
    def mousePressEvent(self, event) -> None:
        super().mousePressEvent(event)
        # if event.button() == Qt.LeftButton:
        #     self.clicked.emit()

    @override
    def setCursor(self, cursor: QCursor) -> None:
        super().setCursor(cursor)
        self.label.setCursor(cursor)

    def set_cover(self, pixmap: QPixmap) -> None:
        self.cover.setPixmap(pixmap)

    def set_default_cover(self, pixmap: QPixmap) -> None:
        self.cover.set_default_pixmap(pixmap)

    def set_label_text(self, text: str) -> None:
        self.label.setText(text)

    def set_label_default_text(self, text: str) -> None:
        self.label.set_default_text(text)

    def set_animation(self, animation: Animation) -> None:
        self.cover.set_animation(
            duration=animation.duration_in_ms,
            start=animation.start,
            end=animation.end,
            on_value_changed=self.cover.zoom
        )
