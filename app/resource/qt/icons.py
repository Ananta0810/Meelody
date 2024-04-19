from PyQt5.QtCore import QSize

from app.components.base import AppIcon


class Icons:
    SMALL: QSize = QSize(24, 24)
    MEDIUM: QSize = QSize(32, 32)
    LARGE: QSize = QSize(48, 48)
    X_LARGE: QSize = QSize(64, 64)

    LOGO: AppIcon
    DELETE: AppIcon
    PLAY_SONG: AppIcon
    MORE: AppIcon
    IMAGE: AppIcon

    MINUS: AppIcon
    ADD: AppIcon
    EDIT: AppIcon
    LOVE: AppIcon
    DOWNLOAD: AppIcon
    MINIMIZE: AppIcon
    CLOSE: AppIcon
    BACKWARD: AppIcon
    FORWARD: AppIcon
    SETTINGS: AppIcon
    LANGUAGES: AppIcon
    FOLDER: AppIcon
    DARK_MODE: AppIcon

    # Icon on Player Bar
    APPLY: AppIcon
    PLAY: AppIcon
    PAUSE: AppIcon
    PREVIOUS: AppIcon
    NEXT: AppIcon
    LOOP: AppIcon
    SHUFFLE: AppIcon
    VOLUME_UP: AppIcon
    VOLUME_DOWN: AppIcon
    VOLUME_SILENT: AppIcon
    TIMER: AppIcon

    @staticmethod
    def init():
        Icons.LOGO = AppIcon("assets/images/logo.ico")

        Icons.DELETE = AppIcon("assets/images/icons/delete.png")
        Icons.PLAY_SONG = AppIcon("assets/images/icons/play-menu.png")
        Icons.MORE = AppIcon("assets/images/icons/more.png")
        Icons.MINUS = AppIcon("assets/images/icons/minus.png")
        Icons.ADD = AppIcon("assets/images/icons/add.png")
        Icons.EDIT = AppIcon("assets/images/icons/edit.png")
        Icons.IMAGE = AppIcon("assets/images/icons/image.png")
        Icons.LOVE = AppIcon("assets/images/icons/love.png")
        Icons.DOWNLOAD = AppIcon("assets/images/icons/download.png")

        Icons.MINIMIZE = AppIcon("assets/images/icons/minimize.png")
        Icons.CLOSE = AppIcon("assets/images/icons/close.png")
        Icons.BACKWARD = AppIcon("assets/images/icons/chevron-backward.png")
        Icons.FORWARD = AppIcon("assets/images/icons/chevron-forward.png")

        Icons.SETTINGS = AppIcon("assets/images/icons/settings.png")
        Icons.LANGUAGES = AppIcon("assets/images/icons/language.png")
        Icons.FOLDER = AppIcon("assets/images/icons/folder.png")
        Icons.DARK_MODE = AppIcon("assets/images/icons/dark-mode.png")

        Icons.APPLY = AppIcon("assets/images/icons/apply.png")
        Icons.PLAY = AppIcon("assets/images/icons/play.png")
        Icons.PAUSE = AppIcon("assets/images/icons/pause.png")
        Icons.PREVIOUS = AppIcon("assets/images/icons/previous.png")
        Icons.NEXT = AppIcon("assets/images/icons/next.png")
        Icons.LOOP = AppIcon("assets/images/icons/loop.png")
        Icons.SHUFFLE = AppIcon("assets/images/icons/shuffle.png")
        Icons.VOLUME_UP = AppIcon("assets/images/icons/volume-up.png")
        Icons.VOLUME_DOWN = AppIcon("assets/images/icons/volume-down.png")
        Icons.VOLUME_SILENT = AppIcon("assets/images/icons/volume-silent.png")
        Icons.TIMER = AppIcon("assets/images/icons/timer.png")
