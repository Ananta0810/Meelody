from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from lib.utils.ui.pixmap_utils import PixmapUtils
from lib.widgets.scaleable_qpixmap import ScaleAblePixmap


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.viewer = QLabel()
        pixmap = ScaleAblePixmap()
        self.viewer.setFixedSize(256, 320)
        VBlayout = QVBoxLayout(self)
        VBlayout.addWidget(self.viewer)

    # def getPixmap(self, coverAsByte: bytes) -> QPixmap:
    #     pixmap = AppUI.getEditedPixmapFromBytes(
    #         coverAsByte,
    #         width=self.library_cover.width(),
    #         height=self.library_cover.height(),
    #         cropCenter=False,
    #         radius=24,
    #     )
    #     return pixmap


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = Window()
    window.setGeometry(500, 300, 800, 600)
    window.show()
    sys.exit(app.exec_())
