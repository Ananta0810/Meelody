from modules.screens.components.labels import StandardLabel
from modules.screens.others.animation import Animation
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor, QFont, QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from widgets.image_displayer import ImageDisplayer


class PlaylistCard(QWidget):
    clicked = pyqtSignal()

    def __init__(self, font: QFont, parent=None):
        super().__init__(parent)
        self.setupUi(font)

    def setupUi(self, font: QFont) -> None:
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.cover = ImageDisplayer(self)
        self.label = StandardLabel.render(font, parent=self)
        self.label.setFixedSize(160, 32)
        self.layout.addStretch()
        self.layout.addWidget(self.label)

    def resizeEvent(self, event) -> None:
        self.cover.setFixedSize(self.size())
        return super().resizeEvent(event)

    def enterEvent(self, event) -> None:
        super().enterEvent(event)
        self.cover.animationOnEnteredHover()

    def leaveEvent(self, event) -> None:
        super().leaveEvent(event)
        self.cover.animationOnLeavedHover()

    def mousePressEvent(self, event) -> None:
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.clicked.emit()

    def setCursor(self, cursor: QCursor) -> None:
        super().setCursor(cursor)
        self.label.setCursor(cursor)

    def setCover(self, pixmap: QPixmap) -> None:
        self.cover.setPixmap(pixmap)

    def setDefaultCover(self, pixmap: QPixmap) -> None:
        self.cover.setDefaultPixmap(pixmap)

    def setLabelText(self, text: str) -> None:
        self.label.setText(text)

    def setLabelDefaultText(self, text: str) -> None:
        self.label.setDefaultText(text)

    def setAnimation(self, animation: Animation) -> None:
        self.cover.setAnimation(
            duration=animation.durationInMs, start=animation.start, end=animation.end, type=self.cover.zoom
        )
