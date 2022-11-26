from typing import Optional, Self, Union

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QLayout

from modules.models.view.builder.IconButtonStyle import IconButtonStyle
from modules.statics.view.Material import Paddings, Icons, Colors, Backgrounds
from modules.widgets.IconButton import IconButton
from modules.widgets.windows.FramelessWindow import FramelessWindow


class FramelessWindowWithTitleBar(FramelessWindow):
    main_layout: QVBoxLayout
    home_screen: QWidget
    title_bar: QHBoxLayout
    background: QWidget
    close_btn: IconButton
    minimize_btn: IconButton

    def __init__(self, parent: Optional["QWidget"] = None):
        super(FramelessWindowWithTitleBar, self).__init__(parent)
        self.__init_component_ui()

    def __init_component_ui(self) -> None:
        self.background = QWidget(self)
        self.home_screen = QWidget(self)
        self.setCentralWidget(self.home_screen)

        self.main_layout = QVBoxLayout(self.home_screen)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.title_bar = QHBoxLayout()
        self.title_bar.setContentsMargins(12, 12, 12, 12)
        self.title_bar.setSpacing(8)

        self.minimize_btn = IconButton.build(
            padding=Paddings.RELATIVE_50,
            size=Icons.MEDIUM,
            style=IconButtonStyle(
                light_mode_icon=Icons.MINIMIZE.with_color(Colors.PRIMARY),
                dark_mode_icon=Icons.MINIMIZE.with_color(Colors.WHITE),
                light_mode_background=Backgrounds.ROUNDED_HIDDEN_PRIMARY_25.with_border_radius(8),
                dark_mode_background=Backgrounds.ROUNDED_HIDDEN_WHITE_50.with_border_radius(8),
            )
        )

        self.close_btn = IconButton.build(
            padding=Paddings.RELATIVE_50,
            size=Icons.MEDIUM,
            style=IconButtonStyle(
                light_mode_icon=Icons.CLOSE.with_color(Colors.DANGER),
                light_mode_background=Backgrounds.ROUNDED_DANGER_25.with_border_radius(8),
                dark_mode_background=Backgrounds.ROUNDED_DANGER_25.with_border_radius(8),
            )
        )

        self.minimize_btn.clicked.connect(self.showMinimized)

        self.title_bar.addStretch()
        self.title_bar.addWidget(self.minimize_btn)
        self.title_bar.addWidget(self.close_btn)

        self.addLayout(self.title_bar)

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.background.resize(self.size())
        return super().resizeEvent(event)

    def with_title_bar_height(self, height: int) -> Self:
        return super().with_height(height)

    def addLayout(self, widget: QLayout) -> None:
        self.main_layout.addLayout(widget)

    def addWidget(self, layout: QWidget, stretch: int = 0, alignment: Union[Qt.Alignment, Qt.AlignmentFlag] = None) -> None:
        if alignment is None:
            self.main_layout.addWidget(layout, stretch=stretch)
            return
        self.main_layout.addWidget(layout, stretch=stretch, alignment=alignment)

    def add_widget_with_alignment(self, a0: QWidget, stretch: int = 0,
                                  alignment: Union[Qt.Alignment, Qt.AlignmentFlag] = None) -> None:
        if alignment is None:
            self.main_layout.addWidget(a0, stretch)
            return
        self.main_layout.addWidget(a0, stretch, alignment)

    def setStyleSheet(self, style_sheet: str) -> None:
        self.background.setStyleSheet(style_sheet)

    def apply_light_mode(self) -> None:
        self.minimize_btn.apply_light_mode()
        self.close_btn.apply_light_mode()

    def apply_dark_mode(self) -> None:
        self.minimize_btn.apply_dark_mode()
        self.close_btn.apply_dark_mode()
