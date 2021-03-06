from functools import lru_cache

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QCursor, QIcon

from .metaclass import SingletonConst


class IconSizes:
    SMALL = QSize(24, 24)
    MEDIUM = QSize(32, 32)
    LARGE = QSize(48, 48)
    XLARGE = QSize(64, 64)


class AppIcons(metaclass=SingletonConst):
    def __init__(self):
        self.SIZES = IconSizes
        self.APP_ICON = QIcon("assets/images/Music.ico")

        self.DELETE = QIcon("assets/images/icons/delete.png")
        self.PLAY_SONG = QIcon("assets/images/icons/play-menu.png")
        self.MORE = QIcon("assets/images/icons/more.png")
        self.SUBSTRACT = QIcon("assets/images/icons/substract.png")
        self.ADD = QIcon("assets/images/icons/add.png")
        self.EDIT = QIcon("assets/images/icons/edit.png")
        self.LOVE = QIcon("assets/images/icons/love.png")
        self.DOWNLOAD = QIcon("assets/images/icons/download.png")

        self.MINIMIZE = QIcon("assets/images/icons/minimize.png")
        self.CLOSE = QIcon("assets/images/icons/close.png")
        self.BACKWARD = QIcon("assets/images/icons/chevron-backward.png")
        self.FORWARD = QIcon("assets/images/icons/chevron-forward.png")

        self.SETTINGS = QIcon("assets/images/icons/settings.png")
        self.LANGUAGES = QIcon("assets/images/icons/language.png")
        self.FOLDER = QIcon("assets/images/icons/folder.png")
        self.DARKMODE = QIcon("assets/images/icons/dark-mode.png")

        # Icon on Player Bar
        self.APPLY = QIcon("assets/images/icons/apply.png")
        self.PLAY = QIcon("assets/images/icons/play.png")
        self.PAUSE = QIcon("assets/images/icons/pause.png")
        self.PREVIOUS = QIcon("assets/images/icons/previous.png")
        self.NEXT = QIcon("assets/images/icons/next.png")
        self.LOOP = QIcon("assets/images/icons/loop.png")
        self.SHUFFLE = QIcon("assets/images/icons/shuffle.png")
        self.VOLUME_UP = QIcon("assets/images/icons/volume-up.png")
        self.VOLUME_DOWN = QIcon("assets/images/icons/volume-down.png")
        self.VOLUME_SILENT = QIcon("assets/images/icons/volume-silent.png")
        self.TIMER = QIcon("assets/images/icons/timer.png")


class AppCursors:
    hands: QCursor = None

    def __init__(self):
        self.HAND = QCursor(Qt.PointingHandCursor)

    # @property
    def hand() -> QCursor:
        return QCursor(Qt.PointingHandCursor)
