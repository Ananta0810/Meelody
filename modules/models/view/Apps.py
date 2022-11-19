from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QCursor


class Icons:
    SMALL: QSize = QSize(24, 24)
    MEDIUM: QSize = QSize(32, 32)
    LARGE: QSize = QSize(48, 48)
    X_LARGE: QSize = QSize(64, 64)

    LOGO: QIcon
    DELETE: QIcon
    PLAY_SONG: QIcon
    MORE: QIcon

    MINUS: QIcon
    ADD: QIcon
    EDIT: QIcon
    LOVE: QIcon
    DOWNLOAD: QIcon
    MINIMIZE: QIcon
    CLOSE: QIcon
    BACKWARD: QIcon
    FORWARD: QIcon
    SETTINGS: QIcon
    LANGUAGES: QIcon
    FOLDER: QIcon
    DARK_MODE: QIcon

    # Icon on Player Bar
    APPLY: QIcon
    PLAY: QIcon
    PAUSE: QIcon
    PREVIOUS: QIcon
    NEXT: QIcon
    LOOP: QIcon
    SHUFFLE: QIcon
    VOLUME_UP: QIcon
    VOLUME_DOWN: QIcon
    VOLUME_SILENT: QIcon
    TIMER: QIcon

    @staticmethod
    def init_value():
        Icons.LOGO = QIcon("assets/images/logo.ico")

        Icons.DELETE = QIcon("assets/images/icons/delete.png")
        Icons.PLAY_SONG = QIcon("assets/images/icons/play-menu.png")
        Icons.MORE = QIcon("assets/images/icons/more.png")
        Icons.MINUS = QIcon("assets/images/icons/minus.png")
        Icons.ADD = QIcon("assets/images/icons/add.png")
        Icons.EDIT = QIcon("assets/images/icons/edit.png")
        Icons.LOVE = QIcon("assets/images/icons/love.png")
        Icons.DOWNLOAD = QIcon("assets/images/icons/download.png")

        Icons.MINIMIZE = QIcon("assets/images/icons/minimize.png")
        Icons.CLOSE = QIcon("assets/images/icons/close.png")
        Icons.BACKWARD = QIcon("assets/images/icons/chevron-backward.png")
        Icons.FORWARD = QIcon("assets/images/icons/chevron-forward.png")

        Icons.SETTINGS = QIcon("assets/images/icons/settings.png")
        Icons.LANGUAGES = QIcon("assets/images/icons/language.png")
        Icons.FOLDER = QIcon("assets/images/icons/folder.png")
        Icons.DARK_MODE = QIcon("assets/images/icons/dark-mode.png")

        Icons.APPLY = QIcon("assets/images/icons/apply.png")
        Icons.PLAY = QIcon("assets/images/icons/play.png")
        Icons.PAUSE = QIcon("assets/images/icons/pause.png")
        Icons.PREVIOUS = QIcon("assets/images/icons/previous.png")
        Icons.NEXT = QIcon("assets/images/icons/next.png")
        Icons.LOOP = QIcon("assets/images/icons/loop.png")
        Icons.SHUFFLE = QIcon("assets/images/icons/shuffle.png")
        Icons.VOLUME_UP = QIcon("assets/images/icons/volume-up.png")
        Icons.VOLUME_DOWN = QIcon("assets/images/icons/volume-down.png")
        Icons.VOLUME_SILENT = QIcon("assets/images/icons/volume-silent.png")
        Icons.TIMER = QIcon("assets/images/icons/timer.png")


class Cursors:
    HAND: QCursor = None

    @staticmethod
    def init_value():
        Cursors.HAND = QCursor(Qt.PointingHandCursor)
