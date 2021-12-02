from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QColor, QCursor, QIcon
from PyQt5.QtWidgets import QGraphicsDropShadowEffect


class IconSize:
    SMALL = QSize(24, 24)
    MEDIUM = QSize(32, 32)
    LARGE = QSize(48, 48)
    XLARGE = QSize(64, 64)


class AppIcons:
    def __init__(self):
        self.SIZES = IconSize
        self.APP_ICON = QIcon("assets/images/Music.ico")

        self.DELETE = QIcon("assets/images/icons/playlist-delete.png")
        self.PLAY_SONG = QIcon("assets/images/icons/play-menu.png")
        self.MORE = QIcon("assets/images/icons/more.png")
        self.SUBSTRACT = QIcon("assets/images/icons/substract.png")
        self.ADD = QIcon("assets/images/icons/add.png")
        self.EDIT = QIcon("assets/images/icons/edit.png")
        self.CLOSE = QIcon("assets/images/icons/close.png")

        self.LOVE = QIcon("assets/images/icons/love.png")

        self.LIGHT_MINIMIZE = QIcon("assets/images/icons/minimize-light.png")
        self.DARK_MINIMIZE = QIcon("assets/images/icons/minimize-dark.png")
        self.CLOSE_2 = QIcon("assets/images/icons/close-window.png")
        self.LIGHT_BACKWARD = QIcon("assets/images/icons/chevron-backward-light.png")
        self.DARK_BACKWARD = QIcon("assets/images/icons/chevron-backward-dark.png")

        self.LIGHT_FORWARD = QIcon("assets/images/icons/chevron-forward-light.png")
        self.DARK_FORWARD = QIcon("assets/images/icons/chevron-forward-dark.png")

        self.DARK_SETTINGS = QIcon("assets/images/icons/settings-dark.png")
        self.LIGHT_SETTINGS = QIcon("assets/images/icons/settings-light.png")
        self.LIGHT_LANGUAGE = QIcon("assets/images/icons/language-light.png")
        self.DARK_LANGUAGE = QIcon("assets/images/icons/language-dark.png")
        self.LIGHT_FOLDER = QIcon("assets/images/icons/folder-light.png")
        self.DARK_FOLDER = QIcon("assets/images/icons/folder-dark.png")
        self.LIGHT_DARKMODE = QIcon("assets/images/icons/dark-mode-light.png")
        self.DARK_DARKMODE = QIcon("assets/images/icons/dark-mode-dark.png")

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


class AppAlignment:
    def __init__(self):
        self.CENTER = Qt.AlignCenter
        self.LEFT = Qt.AlignLeft
        self.RIGHT = Qt.AlignRight


class AppCursors:
    def __init__(self):
        self.HAND = QCursor(Qt.PointingHandCursor)


class AppEffect:
    shadow = QGraphicsDropShadowEffect(
        blurRadius=50, color=QColor(128, 64, 255, 100), xOffset=0, yOffset=3
    )
