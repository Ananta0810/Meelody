from PyQt5.QtCore import QSize

from app.components.base import AppIcon
from app.utils.reflections import memoizeStaticProperty


class Icons:
    small: QSize = QSize(24, 24)
    medium: QSize = QSize(32, 32)
    large: QSize = QSize(48, 48)
    xLarge: QSize = QSize(64, 64)

    @memoizeStaticProperty
    def logo(self) -> AppIcon:
        return AppIcon("resource/images/logo.ico")

    @memoizeStaticProperty
    def export(self) -> AppIcon:
        return AppIcon("resource/images/icons/export.png")

    @memoizeStaticProperty
    def delete(self) -> AppIcon:
        return AppIcon("resource/images/icons/delete.png")

    @memoizeStaticProperty
    def playSong(self) -> AppIcon:
        return AppIcon("resource/images/icons/play-menu.png")

    @memoizeStaticProperty
    def more(self) -> AppIcon:
        return AppIcon("resource/images/icons/more.png")

    @memoizeStaticProperty
    def minus(self) -> AppIcon:
        return AppIcon("resource/images/icons/minus.png")

    @memoizeStaticProperty
    def add(self) -> AppIcon:
        return AppIcon("resource/images/icons/add.png")

    @memoizeStaticProperty
    def edit(self) -> AppIcon:
        return AppIcon("resource/images/icons/edit.png")

    @memoizeStaticProperty
    def image(self) -> AppIcon:
        return AppIcon("resource/images/icons/image.png")

    @memoizeStaticProperty
    def love(self) -> AppIcon:
        return AppIcon("resource/images/icons/love.png")

    @memoizeStaticProperty
    def loved(self) -> AppIcon:
        return AppIcon("resource/images/icons/loved.png")

    @memoizeStaticProperty
    def download(self) -> AppIcon:
        return AppIcon("resource/images/icons/download.png")

    @memoizeStaticProperty
    def minimize(self) -> AppIcon:
        return AppIcon("resource/images/icons/minimize.png")

    @memoizeStaticProperty
    def maximize(self) -> AppIcon:
        return AppIcon("resource/images/icons/maximize.png")

    @memoizeStaticProperty
    def close(self) -> AppIcon:
        return AppIcon("resource/images/icons/close.png")

    @memoizeStaticProperty
    def backward(self) -> AppIcon:
        return AppIcon("resource/images/icons/chevron-backward.png")

    @memoizeStaticProperty
    def forward(self) -> AppIcon:
        return AppIcon("resource/images/icons/chevron-forward.png")

    @memoizeStaticProperty
    def settings(self) -> AppIcon:
        return AppIcon("resource/images/icons/settings.png")

    @memoizeStaticProperty
    def languages(self) -> AppIcon:
        return AppIcon("resource/images/icons/language.png")

    @memoizeStaticProperty
    def folder(self) -> AppIcon:
        return AppIcon("resource/images/icons/folder.png")

    @memoizeStaticProperty
    def darkMode(self) -> AppIcon:
        return AppIcon("resource/images/icons/dark-mode.png")

    @memoizeStaticProperty
    def apply(self) -> AppIcon:
        return AppIcon("resource/images/icons/apply.png")

    @memoizeStaticProperty
    def play(self) -> AppIcon:
        return AppIcon("resource/images/icons/play.png")

    @memoizeStaticProperty
    def pause(self) -> AppIcon:
        return AppIcon("resource/images/icons/pause.png")

    @memoizeStaticProperty
    def previous(self) -> AppIcon:
        return AppIcon("resource/images/icons/previous.png")

    @memoizeStaticProperty
    def next(self) -> AppIcon:
        return AppIcon("resource/images/icons/next.png")

    @memoizeStaticProperty
    def loop(self) -> AppIcon:
        return AppIcon("resource/images/icons/loop.png")

    @memoizeStaticProperty
    def shuffle(self) -> AppIcon:
        return AppIcon("resource/images/icons/shuffle.png")

    @memoizeStaticProperty
    def volumeUp(self) -> AppIcon:
        return AppIcon("resource/images/icons/volume-up.png")

    @memoizeStaticProperty
    def volumeDown(self) -> AppIcon:
        return AppIcon("resource/images/icons/volume-down.png")

    @memoizeStaticProperty
    def volumeSilent(self) -> AppIcon:
        return AppIcon("resource/images/icons/volume-silent.png")

    @memoizeStaticProperty
    def timer(self) -> AppIcon:
        return AppIcon("resource/images/icons/timer.png")
