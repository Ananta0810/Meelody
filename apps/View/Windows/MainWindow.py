from PyQt5.QtCore import pyqtSignal, Qt

from modules.helpers.types.Decorators import override
from modules.models.view.Background import Background
from modules.screens.AbstractScreen import BaseView
from modules.screens.body.HomeBodyView import HomeBodyView
from modules.screens.music_bar.MusicPlayerControl import MusicPlayerControl
from modules.statics.view.Material import ColorBoxes
from modules.widgets.Windows import CloseableWindow


class MainWindow(CloseableWindow, BaseView):
    _body: HomeBodyView
    _music_player: MusicPlayerControl
    post_show: pyqtSignal = pyqtSignal()

    def __init__(self, width: int = 1280, height: int = 720):
        super().__init__()
        self.__is_first_load = True

        self.setFixedWidth(width)
        self.setFixedHeight(height)
        self.__init_ui()

        # self.installEventFilter(self)

    def __init_ui(self) -> None:
        self._body = HomeBodyView()
        self._body.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._body.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._body.setWidgetResizable(True)
        self._body.setContentsMargins(72, 20, 50, 0)

        self._music_player = MusicPlayerControl()
        self._music_player.setFixedHeight(96)
        self._music_player.setObjectName("musicPlayer")

        self.addWidget(self._body)
        self.addWidget(self._music_player, alignment=Qt.AlignBottom)

    @override
    def apply_light_mode(self) -> None:
        super().apply_light_mode()
        self.setStyleSheet(Background(border_radius=32, color=ColorBoxes.WHITE).to_stylesheet())
        self._body.apply_light_mode()
        self._music_player.setStyleSheet("QWidget#musicPlayer{border-top: 1px solid #eaeaea};border-radius:0px")
        self._music_player.apply_light_mode()

    @override
    def apply_dark_mode(self) -> None:
        super().apply_dark_mode()
        self.setStyleSheet(Background(border_radius=32, color=ColorBoxes.BLACK).to_stylesheet())
        self._body.apply_dark_mode()
        self._music_player.setStyleSheet("QWidget#musicPlayer{border-top: 1px solid #202020};border-radius:0px")
        self._music_player.apply_dark_mode()
