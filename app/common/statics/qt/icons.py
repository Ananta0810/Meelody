from PyQt5.QtCore import QSize

from app.helpers.base import memoizeStaticProperty


class Icons:
    small: QSize = QSize(24, 24)
    medium: QSize = QSize(32, 32)
    large: QSize = QSize(48, 48)
    xLarge: QSize = QSize(64, 64)

    @memoizeStaticProperty
    def logo(self) -> 'AppIcon':
        from app.components.base import AppIcon
        return AppIcon("app/resource/images/logo.ico")

    @memoizeStaticProperty
    def delete(self) -> 'AppIcon':
        from app.components.base import AppIcon

        return AppIcon("app/resource/images/icons/delete.png")

    @memoizeStaticProperty
    def playSong(self) -> 'AppIcon':
        from app.components.base import AppIcon

        return AppIcon("app/resource/images/icons/play-menu.png")

    @memoizeStaticProperty
    def more(self) -> 'AppIcon':
        from app.components.base import AppIcon

        return AppIcon("app/resource/images/icons/more.png")

    @memoizeStaticProperty
    def minus(self) -> 'AppIcon':
        from app.components.base import AppIcon

        return AppIcon("app/resource/images/icons/minus.png")

    @memoizeStaticProperty
    def add(self) -> 'AppIcon':
        from app.components.base import AppIcon

        return AppIcon("app/resource/images/icons/add.png")

    @memoizeStaticProperty
    def edit(self) -> 'AppIcon':
        from app.components.base import AppIcon

        return AppIcon("app/resource/images/icons/edit.png")

    @memoizeStaticProperty
    def image(self) -> 'AppIcon':
        from app.components.base import AppIcon

        return AppIcon("app/resource/images/icons/image.png")

    @memoizeStaticProperty
    def love(self) -> 'AppIcon':
        from app.components.base import AppIcon

        return AppIcon("app/resource/images/icons/love.png")

    @memoizeStaticProperty
    def download(self) -> 'AppIcon':
        from app.components.base import AppIcon

        return AppIcon("app/resource/images/icons/download.png")

    @memoizeStaticProperty
    def minimize(self) -> 'AppIcon':
        from app.components.base import AppIcon

        return AppIcon("app/resource/images/icons/minimize.png")

    @memoizeStaticProperty
    def close(self) -> 'AppIcon':
        from app.components.base import AppIcon

        return AppIcon("app/resource/images/icons/close.png")

    @memoizeStaticProperty
    def backward(self) -> 'AppIcon':
        from app.components.base import AppIcon

        return AppIcon("app/resource/images/icons/chevron-backward.png")

    @memoizeStaticProperty
    def forward(self) -> 'AppIcon':
        from app.components.base import AppIcon

        return AppIcon("app/resource/images/icons/chevron-forward.png")

    @memoizeStaticProperty
    def settings(self) -> 'AppIcon':
        from app.components.base import AppIcon

        return AppIcon("app/resource/images/icons/settings.png")

    @memoizeStaticProperty
    def languages(self) -> 'AppIcon':
        from app.components.base import AppIcon

        return AppIcon("app/resource/images/icons/language.png")

    @memoizeStaticProperty
    def folder(self) -> 'AppIcon':
        from app.components.base import AppIcon

        return AppIcon("app/resource/images/icons/folder.png")

    @memoizeStaticProperty
    def darkMode(self) -> 'AppIcon':
        from app.components.base import AppIcon

        return AppIcon("app/resource/images/icons/dark-mode.png")

    @memoizeStaticProperty
    def apply(self) -> 'AppIcon':
        from app.components.base import AppIcon

        return AppIcon("app/resource/images/icons/apply.png")

    @memoizeStaticProperty
    def play(self) -> 'AppIcon':
        from app.components.base import AppIcon

        return AppIcon("app/resource/images/icons/play.png")

    @memoizeStaticProperty
    def pause(self) -> 'AppIcon':
        from app.components.base import AppIcon

        return AppIcon("app/resource/images/icons/pause.png")

    @memoizeStaticProperty
    def previous(self) -> 'AppIcon':
        from app.components.base import AppIcon

        return AppIcon("app/resource/images/icons/previous.png")

    @memoizeStaticProperty
    def next(self) -> 'AppIcon':
        from app.components.base import AppIcon

        return AppIcon("app/resource/images/icons/next.png")

    @memoizeStaticProperty
    def loop(self) -> 'AppIcon':
        from app.components.base import AppIcon

        return AppIcon("app/resource/images/icons/loop.png")

    @memoizeStaticProperty
    def shuffle(self) -> 'AppIcon':
        from app.components.base import AppIcon

        return AppIcon("app/resource/images/icons/shuffle.png")

    @memoizeStaticProperty
    def volumeUp(self) -> 'AppIcon':
        from app.components.base import AppIcon

        return AppIcon("app/resource/images/icons/volume-up.png")

    @memoizeStaticProperty
    def volumeDown(self) -> 'AppIcon':
        from app.components.base import AppIcon

        return AppIcon("app/resource/images/icons/volume-down.png")

    @memoizeStaticProperty
    def volumeSilent(self) -> 'AppIcon':
        from app.components.base import AppIcon

        return AppIcon("app/resource/images/icons/volume-silent.png")

    @memoizeStaticProperty
    def timer(self) -> 'AppIcon':
        from app.components.base import AppIcon

        return AppIcon("app/resource/images/icons/timer.png")
