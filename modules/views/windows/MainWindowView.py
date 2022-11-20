from typing import Optional, Union, Self

from PyQt5.QtCore import QMetaObject, Qt
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLayout

from modules.models.view.Background import Background
from modules.models.view.builder.IconButtonStyle import IconButtonStyle
from modules.statics.view.Material import ColorBoxes, Paddings, Colors, Icons, Backgrounds
from modules.views.music_bar.MusicPlayerBar import MusicPlayerBar
from modules.widgets.IconButton import IconButton
from modules.widgets.windows.FramelessWindow import FramelessWindow


class MainWindowView(FramelessWindow):
    music_player: MusicPlayerBar
    main_layout: QVBoxLayout
    home_screen: QWidget
    title_bar: QHBoxLayout
    background: QWidget
    close_btn: IconButton
    minimize_btn: IconButton

    def __init__(self, parent: Optional["QWidget"] = None, width: int = 1280, height: int = 720):
        super(MainWindowView, self).__init__(parent)
        self.setFixedWidth(width)
        self.setFixedHeight(height)
        self.setup_ui()

    def setup_ui(self) -> None:
        self.background = QWidget(self)
        self.home_screen = QWidget(self)
        self.setCentralWidget(self.home_screen)

        self.main_layout = QVBoxLayout(self.home_screen)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.title_bar = QHBoxLayout()
        self.title_bar.setContentsMargins(12, 12, 12, 12)
        self.title_bar.setSpacing(8)
        self.main_layout.addLayout(self.title_bar)
        self.main_layout.addStretch(1)

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

        self.music_player = MusicPlayerBar()
        self.music_player.setFixedHeight(96)
        self.music_player.setObjectName("musicPlayer")

        self.main_layout.addWidget(self.music_player, alignment=Qt.AlignBottom)
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

    def add_widget_with_alignment(self, a0: QWidget, stretch: int = 0,
                                  alignment: Union[Qt.Alignment, Qt.AlignmentFlag] = None) -> None:
        if alignment is None:
            self.main_layout.addWidget(a0, stretch)
            return
        self.main_layout.addWidget(a0, stretch, alignment)

    def apply_light_mode(self) -> None:
        self.background.setStyleSheet(Background(border_radius=24, color=ColorBoxes.WHITE).to_stylesheet())
        self.music_player.setStyleSheet("QWidget#musicPlayer{border-top: 1px solid #eaeaea};border-radius:0px")
        self.minimize_btn.apply_light_mode()
        self.close_btn.apply_light_mode()
        self.music_player.apply_light_mode()

    def apply_dark_mode(self) -> None:
        self.background.setStyleSheet(Background(border_radius=24, color=ColorBoxes.BLACK).to_stylesheet())
        self.music_player.setStyleSheet("QWidget#musicPlayer{border-top: 1px solid #202020};border-radius:0px")
        self.minimize_btn.apply_dark_mode()
        self.close_btn.apply_dark_mode()
        self.music_player.apply_dark_mode()

    def connect_signal(self) -> None:
        pass

    def translate(self) -> None:
        pass
