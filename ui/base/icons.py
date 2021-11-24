from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon


class IconSize:
    SIZE_SMALL = QSize(24, 24)
    SIZE_MEDIUM = QSize(32, 32)
    # SIZE_LARGE = QSize(40, 40)
    SIZE_LARGE = QSize(48, 48)
    SIZE_XLARGE = QSize(64, 64)


class Icon:
    # align_center = Qt.AlignCenter
    SIZES = IconSize
    APP_ICON = QIcon("Music.ico")

    DELETE = QIcon("images/icons/playlist-delete.png")
    PLAY_SONG = QIcon("images/icons/play-menu.png")
    MORE = QIcon("images/icons/more.png")
    SUBSTRACT = QIcon("images/icons/substract.png")
    ADD = QIcon("images/icons/add.png")
    EDIT = QIcon("images/icons/edit-song.png")
    EDIT_PLAYLIST = QIcon("images/icons/edit-playlist.png")
    CLOSE = QIcon("images/icons/close.png")

    LOVE = QIcon("images/icons/love.png")
    UNLOVE = QIcon("images/icons/unlove.png")

    LIGHT_MINIMIZE = QIcon("images/icons/minimize-light.png")
    DARK_MINIMIZE = QIcon("images/icons/minimize-dark.png")
    CLOSE_2 = QIcon("images/icons/close-window.png")
    LIGHT_BACKWARD = QIcon("images/icons/chevron-backward-light.png")
    DARK_BACKWARD = QIcon("images/icons/chevron-backward-dark.png")

    LIGHT_FORWARD = QIcon("images/icons/chevron-forward-light.png")
    DARK_FORWARD = QIcon("images/icons/chevron-forward-dark.png")

    DARK_SETTINGS = QIcon("images/icons/settings-dark.png")
    LIGHT_SETTINGS = QIcon("images/icons/settings-light.png")
    LIGHT_LANGUAGE = QIcon("images/icons/language-light.png")
    DARK_LANGUAGE = QIcon("images/icons/language-dark.png")
    LIGHT_FOLDER = QIcon("images/icons/folder-light.png")
    DARK_FOLDER = QIcon("images/icons/folder-dark.png")
    LIGHT_DARKMODE = QIcon("images/icons/dark-mode-light.png")
    DARK_DARKMODE = QIcon("images/icons/dark-mode-dark.png")

    # Icon on Player Bar
    APPLY = QIcon("images/icons/apply.png")
    PLAY_PLAYER = QIcon("images/icons/play-player.png")
    PAUSE = QIcon("images/icons/pause-player.png")
    PREVIOUS = QIcon("images/icons/previous.png")
    NEXT = QIcon("images/icons/next.png")
    LOOP = QIcon("images/icons/loop.png")
    UNLOOP = QIcon("images/icons/unloop.png")
    SHUFFLE = QIcon("images/icons/shuffle.png")
    UNSHUFFLE = QIcon("images/icons/unshuffle.png")
    VOLUME_UP = QIcon("images/icons/volume-up.png")
    VOLUME_DOWN = QIcon("images/icons/volume-down.png")
    VOLUME_SILENT = QIcon("images/icons/volume-silent.png")
    TIMER = QIcon("images/icons/timer.png")

    # # ! magic numbers
    # PLAYLIST_COVER_SIZE = 320
    # PLAYLIST_COVER_RADIUS = 32
    # SONG_COVER_SIZE = 64
    # SONG_COVER_RADIUS = 12
