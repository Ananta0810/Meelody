from modules.screens.components.labels import ViewLabel
from modules.screens.others.animation import Animation
from PyQt5.QtCore import QEvent, QRect, Qt, pyqtSignal
from PyQt5.QtGui import QCursor, QFont, QPixmap
from PyQt5.QtWidgets import QVBoxLayout
from widgets.hoverable_widget import HoverableWidget
from widgets.image_displayer import ImageDisplayer


class DefaultPlaylistCard(HoverableWidget):
    clicked = pyqtSignal()

    def __init__(self, labelFormer: ViewLabel, font: QFont, animation: Animation, parent=None):
        super().__init__(parent)
        self._labelFormer = labelFormer
        self._font = font
        self._animation = animation
        self.setupUi()

    def resizeEvent(self, event):
        self.cover.setFixedSize(self.size())
        return super().resizeEvent(event)

    def enterEvent(self, event):
        super().enterEvent(event)
        self.cover.animationOnEnteredHover()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.cover.animationOnLeavedHover()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.clicked.emit()

    def setupUi(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.cover = ImageDisplayer(self)
        self.cover.setAnimation(
            duration=self._animation.durationInMs, start=self._animation.start, end=self._animation.end
        )

        self.label = self._labelFormer.render(self._font, parent=self)
        self.label.setFixedSize(160, 32)
        self.layout.addStretch()
        self.layout.addWidget(self.label)

    def setCover(self, pixmap: QPixmap):
        self.cover.setPixmap(pixmap)

    def setDefaultCover(self, pixmap: QPixmap):
        self.cover.setDefaultPixmap(pixmap)

    def setLabelText(self, text: str):
        self.label.setText(text)

    def setLabelDefaultText(self, text: str):
        self.label.setDefaultText(text)

    def setAnimation(self, animation: Animation):
        self.cover.setAnimation(duration=animation.durationInMs, start=animation.start, end=animation.end)

    def setCursor(self, cursor: QCursor):
        super().setCursor(cursor)
        self.label.setCursor(cursor)
