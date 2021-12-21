from modules.screens.components.labels import ViewLabel
from modules.screens.others.animation import Animation
from PyQt5.QtCore import QRect, Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from widgets.hoverable_widget import HoverableWidget
from widgets.image_displayer import ImageDisplayer


class EditablePlaylistCard(HoverableWidget):
    clicked = pyqtSignal()

    def __init__(
        self,
        labelFormer: ViewLabel,
        font: QFont,
        editBtn,
        deleteBtn,
        animation: Animation,
        defaultText: str = "Unknown",
        parent=None,
    ):
        super().__init__(parent)
        self._labelFormer = labelFormer
        self._font = font
        self.editBtn = editBtn
        self.deleteBtn = deleteBtn
        self._animation = animation
        self._defaultText = defaultText
        self.setupUi()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.clicked.emit()

    def enterEvent(self, event):
        super().enterEvent(event)
        self.cover.animationOnEnteredHover()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.cover.animationOnLeavedHover()

    def setupUi(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 10, 10, 20)

        self.btns = QHBoxLayout()
        self.btns.setContentsMargins(0, 0, 0, 0)
        self.btns.addStretch()
        self.btns.addWidget(self.editBtn)
        self.btns.addWidget(self.deleteBtn)

        self.cover = ImageDisplayer(self)
        self.cover.setGeometry(QRect(0, 0, 256, 320))
        self.cover.setAnimation(
            duration=self._animation.durationInMs, start=self._animation.start, end=self._animation.end
        )

        self.label = self._labelFormer.render(self._font, parent=self)
        self.label.setFixedSize(160, 32)

        self.main_layout.addLayout(self.btns)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.label)

    def reset(self):
        self.setLabelText(self.defautText)
        self.setCover(None)

    def setCover(self, pixmap: QPixmap):
        self.cover.setPixmap(pixmap)

    def setDefaultCover(self, pixmap: QPixmap):
        self.cover.setDefaultPixmap(pixmap)

    def setLabelText(self, text: str):
        self.label.setText(text)

    def setDefaultText(self, text: str):
        oldText: str = self.defautText
        self.defautText = text

        if self.label.text() == oldText:
            self.label.setText(text)

    def setAnimation(self, animation: Animation):
        self.cover.setAnimation(duration=animation.durationInMs, start=animation.start, end=animation.end)
