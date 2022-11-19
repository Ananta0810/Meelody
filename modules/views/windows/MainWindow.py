from typing import Optional, Union, Self

from PyQt5.QtCore import QMetaObject, Qt
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLayout

from modules.widgets.windows.FramelessWindow import FramelessWindow


class MainWindow(FramelessWindow):

    def __init__(self, parent: Optional["QWidget"] = None):
        super(MainWindow, self).__init__(parent)
        self.title_bar = QHBoxLayout()
        self.home_screen = QWidget(self)
        self.background = QWidget(self)
        self.main_layout = QVBoxLayout(self.home_screen)
        self.setup_ui()

    def setup_ui(self) -> None:
        self.setCentralWidget(self.home_screen)

        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.title_bar.setContentsMargins(12, 12, 12, 12)
        self.title_bar.setSpacing(8)
        self.main_layout.addLayout(self.title_bar)

        self.title_bar.addStretch()
        self.setStyleSheet("background:WHITE;border-radius:24px")
        # self.titleBar.addWidget(self.minimize_btn)
        # self.titleBar.addWidget(self.close_btn)

        QMetaObject.connectSlotsByName(self)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.background.resize(self.size())
        return super().resizeEvent(a0)

    def with_title_bar_height(self, height: int) -> Self:
        return super().with_height(height)

    def add_layout(self, widget: Optional["QWidget"]) -> None:
        self.main_layout.addLayout(widget)

    def add_widget(self, layout: QLayout, stretch: int = 0) -> None:
        self.main_layout.addLayout(layout, stretch=stretch)

    def add_widget_with_alignment(self, a0: QWidget, stretch: int = 0, alignment: Union[Qt.Alignment, Qt.AlignmentFlag] = None) -> None:
        if alignment is None:
            self.main_layout.addWidget(a0, stretch)
            return
        self.main_layout.addWidget(a0, stretch, alignment)

