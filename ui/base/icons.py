from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon


class IconSize:
    SMALL = QSize(24, 24)
    MEDIUM = QSize(32, 32)
    # LARGE = QSize(40, 40)
    LARGE = QSize(48, 48)
    XLARGE = QSize(64, 64)


class Icons:
    def __init__(self):
        # align_center = Qt.AlignCenter
        self.SIZES = IconSize
        self.APP_ICON = QIcon("Music.ico")

        self.DELETE = QIcon("src/icons/playlist-delete.png")
        self.PLAY_SONG = QIcon("src/icons/play-menu.png")
        self.MORE = QIcon("src/icons/more.png")
        self.SUBSTRACT = QIcon("src/icons/substract.png")
        self.ADD = QIcon("src/icons/add.png")
        self.EDIT = QIcon("src/icons/edit.png")
        self.CLOSE = QIcon("src/icons/close.png")

        self.LOVE = QIcon("src/icons/love.png")
        # self.UNLOVE = QIcon("src/icons/unlove.png")

        self.LIGHT_MINIMIZE = QIcon("src/icons/minimize-light.png")
        self.DARK_MINIMIZE = QIcon("src/icons/minimize-dark.png")
        self.CLOSE_2 = QIcon("src/icons/close-window.png")
        self.LIGHT_BACKWARD = QIcon("src/icons/chevron-backward-light.png")
        self.DARK_BACKWARD = QIcon("src/icons/chevron-backward-dark.png")

        self.LIGHT_FORWARD = QIcon("src/icons/chevron-forward-light.png")
        self.DARK_FORWARD = QIcon("src/icons/chevron-forward-dark.png")

        self.DARK_SETTINGS = QIcon("src/icons/settings-dark.png")
        self.LIGHT_SETTINGS = QIcon("src/icons/settings-light.png")
        self.LIGHT_LANGUAGE = QIcon("src/icons/language-light.png")
        self.DARK_LANGUAGE = QIcon("src/icons/language-dark.png")
        self.LIGHT_FOLDER = QIcon("src/icons/folder-light.png")
        self.DARK_FOLDER = QIcon("src/icons/folder-dark.png")
        self.LIGHT_DARKMODE = QIcon("src/icons/dark-mode-light.png")
        self.DARK_DARKMODE = QIcon("src/icons/dark-mode-dark.png")

        # Icon on Player Bar
        self.APPLY = QIcon("src/icons/apply.png")
        self.PLAY = QIcon("src/icons/play.png")
        self.PAUSE = QIcon("src/icons/pause.png")
        self.PREVIOUS = QIcon("src/icons/previous.png")
        self.NEXT = QIcon("src/icons/next.png")
        self.LOOP = QIcon("src/icons/loop.png")
        self.UNLOOP = QIcon("src/icons/unloop.png")
        self.SHUFFLE = QIcon("src/icons/shuffle.png")
        self.UNSHUFFLE = QIcon("src/icons/unshuffle.png")
        self.VOLUME_UP = QIcon("src/icons/volume-up.png")
        self.VOLUME_DOWN = QIcon("src/icons/volume-down.png")
        self.VOLUME_SILENT = QIcon("src/icons/volume-silent.png")
        self.TIMER = QIcon("src/icons/timer.png")

        # # ! magic numbers
        # PLAYLIST_COVER_SIZE = 320
        # PLAYLIST_COVER_RADIUS = 32
        # SONG_COVER_SIZE = 64
        # SONG_COVER_RADIUS = 12
