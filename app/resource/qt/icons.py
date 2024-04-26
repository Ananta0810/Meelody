from PyQt5.QtCore import QSize

from app.components.base import AppIcon
from app.helpers.base import memoizeStaticProperty


class Icons:
    SMALL: QSize = QSize(24, 24)
    MEDIUM: QSize = QSize(32, 32)
    LARGE: QSize = QSize(48, 48)
    X_LARGE: QSize = QSize(64, 64)

    @memoizeStaticProperty
    def LOGO(self) -> AppIcon:
        return AppIcon("assets/images/logo.ico")

    @memoizeStaticProperty
    def DELETE(self) -> AppIcon:
        return AppIcon("assets/images/icons/delete.png")

    @memoizeStaticProperty
    def PLAY_SONG(self) -> AppIcon:
        return AppIcon("assets/images/icons/play-menu.png")

    @memoizeStaticProperty
    def MORE(self) -> AppIcon:
        return AppIcon("assets/images/icons/more.png")

    @memoizeStaticProperty
    def MINUS(self) -> AppIcon:
        return AppIcon("assets/images/icons/minus.png")

    @memoizeStaticProperty
    def ADD(self) -> AppIcon:
        return AppIcon("assets/images/icons/add.png")

    @memoizeStaticProperty
    def EDIT(self) -> AppIcon:
        return AppIcon("assets/images/icons/edit.png")

    @memoizeStaticProperty
    def IMAGE(self) -> AppIcon:
        return AppIcon("assets/images/icons/image.png")

    @memoizeStaticProperty
    def LOVE(self) -> AppIcon:
        return AppIcon("assets/images/icons/love.png")

    @memoizeStaticProperty
    def DOWNLOAD(self) -> AppIcon:
        return AppIcon("assets/images/icons/download.png")

    @memoizeStaticProperty
    def MINIMIZE(self) -> AppIcon:
        return AppIcon("assets/images/icons/minimize.png")

    @memoizeStaticProperty
    def CLOSE(self) -> AppIcon:
        return AppIcon("assets/images/icons/close.png")

    @memoizeStaticProperty
    def BACKWARD(self) -> AppIcon:
        return AppIcon("assets/images/icons/chevron-backward.png")

    @memoizeStaticProperty
    def FORWARD(self) -> AppIcon:
        return AppIcon("assets/images/icons/chevron-forward.png")

    @memoizeStaticProperty
    def SETTINGS(self) -> AppIcon:
        return AppIcon("assets/images/icons/settings.png")

    @memoizeStaticProperty
    def LANGUAGES(self) -> AppIcon:
        return AppIcon("assets/images/icons/language.png")

    @memoizeStaticProperty
    def FOLDER(self) -> AppIcon:
        return AppIcon("assets/images/icons/folder.png")

    @memoizeStaticProperty
    def DARK_MODE(self) -> AppIcon:
        return AppIcon("assets/images/icons/dark-mode.png")

    @memoizeStaticProperty
    def APPLY(self) -> AppIcon:
        return AppIcon("assets/images/icons/apply.png")

    @memoizeStaticProperty
    def PLAY(self) -> AppIcon:
        return AppIcon("assets/images/icons/play.png")

    @memoizeStaticProperty
    def PAUSE(self) -> AppIcon:
        return AppIcon("assets/images/icons/pause.png")

    @memoizeStaticProperty
    def PREVIOUS(self) -> AppIcon:
        return AppIcon("assets/images/icons/previous.png")

    @memoizeStaticProperty
    def NEXT(self) -> AppIcon:
        return AppIcon("assets/images/icons/next.png")

    @memoizeStaticProperty
    def LOOP(self) -> AppIcon:
        return AppIcon("assets/images/icons/loop.png")

    @memoizeStaticProperty
    def SHUFFLE(self) -> AppIcon:
        return AppIcon("assets/images/icons/shuffle.png")

    @memoizeStaticProperty
    def VOLUME_UP(self) -> AppIcon:
        return AppIcon("assets/images/icons/volume-up.png")

    @memoizeStaticProperty
    def VOLUME_DOWN(self) -> AppIcon:
        return AppIcon("assets/images/icons/volume-down.png")

    @memoizeStaticProperty
    def VOLUME_SILENT(self) -> AppIcon:
        return AppIcon("assets/images/icons/volume-silent.png")

    @memoizeStaticProperty
    def TIMER(self) -> AppIcon:
        return AppIcon("assets/images/icons/timer.png")
