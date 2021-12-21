from modules.screens.components.labels import ViewLabel
from modules.screens.others.animation import Animation
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QVBoxLayout
from widgets.hoverable_widget import HoverableWidget
from widgets.image_displayer import ImageDisplayer


class DefaultPlaylistCard(HoverableWidget):
    def __init__(self, labelFormer: ViewLabel, font: QFont, animation: Animation, parent=None):
        super().__init__(parent)
        self.labelFormer = labelFormer
        self.font = font
        self.animation = animation
        self.setupUi()

    def setupUi(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.cover = ImageDisplayer(self)
        self.cover.setGeometry(QRect(0, 0, 256, 320))

        self.cover.setAnimation(
            duration=self.animation.durationInMs, start=self.animation.start, end=self.animation.end
        )

        self.label = self.labelFormer.render(self.font, parent=self)
        self.label.setFixedSize(160, 32)
        self.layout.addStretch()
        self.layout.addWidget(self.label)
