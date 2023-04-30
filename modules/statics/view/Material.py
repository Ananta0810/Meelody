from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QCursor

from modules.helpers.types.Bytes import Bytes
from modules.models.view.Background import Background
from modules.models.view.Color import Color
from modules.models.view.ColorBox import ColorBox
from modules.models.view.Padding import Padding
from modules.widgets.Icons import AppIcon


class Paddings:
    DEFAULT = Padding(0.00)
    RELATIVE_25 = Padding(0.25)
    RELATIVE_33 = Padding(0.33)
    RELATIVE_50 = Padding(0.5)
    RELATIVE_67 = Padding(0.67)
    RELATIVE_75 = Padding(0.75)
    RELATIVE_100 = Padding(1.00)

    ABSOLUTE_SMALL = Padding(4)
    ABSOLUTE_MEDIUM = Padding(12)

    LABEL_SMALL = Padding(1.25, 0.625, is_relative=True)
    LABEL_MEDIUM = Padding(1.25, 0.625, is_relative=True)
    LABEL_LARGE = Padding(1.5, 1, is_relative=True)


class Colors:
    PRIMARY = Color(128, 64, 255)

    SUCCESS = Color(50, 216, 100)
    DANGER = Color(255, 80, 80)
    WARNING = Color(255, 170, 28)

    WHITE = Color(255, 255, 255)
    BLACK = Color(0, 0, 0)
    GRAY = Color(128, 128, 128)
    TRANSPARENT = Color(255, 255, 255, 0)


class ColorBoxes:
    TRANSPARENT = ColorBox(Colors.TRANSPARENT)

    # =========================// Primary //=========================
    PRIMARY = ColorBox(Colors.PRIMARY)
    PRIMARY_75 = ColorBox(Colors.PRIMARY.with_opacity(75))
    PRIMARY_50 = ColorBox(Colors.PRIMARY.with_opacity(75))
    PRIMARY_25 = ColorBox(Colors.PRIMARY.with_opacity(25))

    HOVERABLE_PRIMARY = ColorBox(normal=Colors.PRIMARY, active=Colors.PRIMARY)
    HOVERABLE_PRIMARY_75 = ColorBox(normal=Colors.PRIMARY.with_opacity(75), active=Colors.PRIMARY)
    HOVERABLE_PRIMARY_50 = ColorBox(normal=Colors.PRIMARY.with_opacity(50), active=Colors.PRIMARY.with_opacity(75))
    HOVERABLE_PRIMARY_25 = ColorBox(normal=Colors.PRIMARY.with_opacity(25), active=Colors.PRIMARY.with_opacity(50))
    HOVERABLE_PRIMARY_10 = ColorBox(normal=Colors.PRIMARY.with_opacity(12), active=Colors.PRIMARY.with_opacity(25))
    HOVERABLE_PRIMARY_HIDDEN = ColorBox(normal=Colors.TRANSPARENT, active=Colors.PRIMARY)
    HOVERABLE_PRIMARY_HIDDEN_75 = ColorBox(normal=Colors.TRANSPARENT, active=Colors.PRIMARY.with_opacity(75))
    HOVERABLE_PRIMARY_HIDDEN_50 = ColorBox(normal=Colors.TRANSPARENT, active=Colors.PRIMARY.with_opacity(50))
    HOVERABLE_PRIMARY_HIDDEN_25 = ColorBox(normal=Colors.TRANSPARENT, active=Colors.PRIMARY.with_opacity(25))
    HOVERABLE_PRIMARY_HIDDEN_10 = ColorBox(normal=Colors.TRANSPARENT, active=Colors.PRIMARY.with_opacity(12))

    # =========================// Warning //=========================
    WARNING = ColorBox(Colors.WARNING)
    WARNING_75 = ColorBox(Colors.WARNING.with_opacity(75))
    WARNING_50 = ColorBox(Colors.WARNING.with_opacity(50))
    WARNING_25 = ColorBox(Colors.WARNING.with_opacity(25))

    HOVERABLE_WARNING = ColorBox(normal=Colors.WARNING, active=Colors.WARNING)
    HOVERABLE_WARNING_75 = ColorBox(normal=Colors.WARNING.with_opacity(75), active=Colors.WARNING)
    HOVERABLE_WARNING_50 = ColorBox(normal=Colors.WARNING.with_opacity(50), active=Colors.WARNING.with_opacity(75))
    HOVERABLE_WARNING_25 = ColorBox(normal=Colors.WARNING.with_opacity(25), active=Colors.WARNING.with_opacity(50))
    HOVERABLE_WARNING_HIDDEN = ColorBox(normal=Colors.TRANSPARENT, active=Colors.WARNING)
    HOVERABLE_WARNING_HIDDEN_75 = ColorBox(normal=Colors.TRANSPARENT, active=Colors.WARNING.with_opacity(75))
    HOVERABLE_WARNING_HIDDEN_50 = ColorBox(normal=Colors.TRANSPARENT, active=Colors.WARNING.with_opacity(50))
    HOVERABLE_WARNING_HIDDEN_25 = ColorBox(normal=Colors.TRANSPARENT, active=Colors.WARNING.with_opacity(25))

    # =========================// Danger //=========================
    DANGER = ColorBox(Colors.DANGER)
    DANGER_75 = ColorBox(Colors.DANGER.with_opacity(75))
    DANGER_50 = ColorBox(Colors.DANGER.with_opacity(50))
    DANGER_25 = ColorBox(Colors.DANGER.with_opacity(25))

    HOVERABLE_DANGER = ColorBox(normal=Colors.DANGER, active=Colors.DANGER)
    HOVERABLE_DANGER_75 = ColorBox(normal=Colors.DANGER.with_opacity(75), active=Colors.DANGER)
    HOVERABLE_DANGER_50 = ColorBox(normal=Colors.DANGER.with_opacity(50), active=Colors.DANGER.with_opacity(75))
    HOVERABLE_DANGER_25 = ColorBox(normal=Colors.DANGER.with_opacity(25), active=Colors.DANGER.with_opacity(50))
    HOVERABLE_DANGER_10 = ColorBox(normal=Colors.DANGER.with_opacity(12), active=Colors.DANGER.with_opacity(25))
    HOVERABLE_DANGER_HIDDEN = ColorBox(normal=Colors.TRANSPARENT, active=Colors.DANGER)
    HOVERABLE_DANGER_HIDDEN_75 = ColorBox(normal=Colors.TRANSPARENT, active=Colors.DANGER.with_opacity(75))
    HOVERABLE_DANGER_HIDDEN_50 = ColorBox(normal=Colors.TRANSPARENT, active=Colors.DANGER.with_opacity(50))
    HOVERABLE_DANGER_HIDDEN_25 = ColorBox(normal=Colors.TRANSPARENT, active=Colors.DANGER.with_opacity(25))
    HOVERABLE_DANGER_HIDDEN_10 = ColorBox(normal=Colors.TRANSPARENT, active=Colors.DANGER.with_opacity(12))

    # =========================// Black //=========================
    BLACK = ColorBox(Colors.BLACK)
    BLACK_75 = ColorBox(Colors.BLACK.with_opacity(75))
    BLACK_50 = ColorBox(Colors.BLACK.with_opacity(50))
    BLACK_25 = ColorBox(Colors.BLACK.with_opacity(25))

    HOVERABLE_BLACK = ColorBox(normal=Colors.BLACK, active=Colors.BLACK)
    HOVERABLE_BLACK_75 = ColorBox(normal=Colors.BLACK.with_opacity(75), active=Colors.BLACK)
    HOVERABLE_BLACK_50 = ColorBox(normal=Colors.BLACK.with_opacity(50), active=Colors.BLACK.with_opacity(75))
    HOVERABLE_BLACK_25 = ColorBox(normal=Colors.BLACK.with_opacity(25), active=Colors.BLACK.with_opacity(50))
    HOVERABLE_BLACK_HIDDEN = ColorBox(normal=Colors.TRANSPARENT, active=Colors.BLACK)
    HOVERABLE_BLACK_HIDDEN_75 = ColorBox(normal=Colors.TRANSPARENT, active=Colors.BLACK.with_opacity(75))
    HOVERABLE_BLACK_HIDDEN_50 = ColorBox(normal=Colors.TRANSPARENT, active=Colors.BLACK.with_opacity(50))
    HOVERABLE_BLACK_HIDDEN_25 = ColorBox(normal=Colors.TRANSPARENT, active=Colors.BLACK.with_opacity(25))

    # =========================// White //=========================
    WHITE = ColorBox(Colors.WHITE)
    WHITE_75 = ColorBox(Colors.WHITE.with_opacity(75))
    WHITE_50 = ColorBox(Colors.WHITE.with_opacity(50))
    WHITE_25 = ColorBox(Colors.WHITE.with_opacity(25))

    HOVERABLE_WHITE = ColorBox(normal=Colors.WHITE, active=Colors.WHITE)
    HOVERABLE_WHITE_75 = ColorBox(normal=Colors.WHITE.with_opacity(75), active=Colors.WHITE)
    HOVERABLE_WHITE_50 = ColorBox(normal=Colors.WHITE.with_opacity(50), active=Colors.WHITE.with_opacity(75))
    HOVERABLE_WHITE_25 = ColorBox(normal=Colors.WHITE.with_opacity(25), active=Colors.WHITE.with_opacity(50))
    HOVERABLE_WHITE_HIDDEN = ColorBox(normal=Colors.TRANSPARENT, active=Colors.WHITE)
    HOVERABLE_WHITE_HIDDEN_75 = ColorBox(normal=Colors.TRANSPARENT, active=Colors.WHITE.with_opacity(75))
    HOVERABLE_WHITE_HIDDEN_50 = ColorBox(normal=Colors.TRANSPARENT, active=Colors.WHITE.with_opacity(50))
    HOVERABLE_WHITE_HIDDEN_25 = ColorBox(normal=Colors.TRANSPARENT, active=Colors.WHITE.with_opacity(25))

    # =========================// Gray //=========================
    GRAY = ColorBox(Colors.GRAY)
    GRAY_75 = ColorBox(Colors.GRAY.with_opacity(75))
    GRAY_50 = ColorBox(Colors.GRAY.with_opacity(50))
    GRAY_25 = ColorBox(Colors.GRAY.with_opacity(25))

    HOVERABLE_GRAY = ColorBox(normal=Colors.GRAY, active=Colors.GRAY)
    HOVERABLE_GRAY_75 = ColorBox(normal=Colors.GRAY.with_opacity(75), active=Colors.GRAY)
    HOVERABLE_GRAY_50 = ColorBox(normal=Colors.GRAY.with_opacity(50), active=Colors.GRAY.with_opacity(75))
    HOVERABLE_GRAY_25 = ColorBox(normal=Colors.GRAY.with_opacity(25), active=Colors.GRAY.with_opacity(50))
    HOVERABLE_GRAY_10 = ColorBox(normal=Colors.GRAY.with_opacity(10), active=Colors.GRAY.with_opacity(12))
    HOVERABLE_GRAY_HIDDEN = ColorBox(normal=Colors.TRANSPARENT, active=Colors.GRAY)
    HOVERABLE_GRAY_HIDDEN_75 = ColorBox(normal=Colors.TRANSPARENT, active=Colors.GRAY.with_opacity(75))
    HOVERABLE_GRAY_HIDDEN_50 = ColorBox(normal=Colors.TRANSPARENT, active=Colors.GRAY.with_opacity(50))
    HOVERABLE_GRAY_HIDDEN_25 = ColorBox(normal=Colors.TRANSPARENT, active=Colors.GRAY.with_opacity(25))
    HOVERABLE_GRAY_HIDDEN_10 = ColorBox(normal=Colors.TRANSPARENT, active=Colors.GRAY.with_opacity(12))


class Backgrounds:
    TRANSPARENT = Background(color=ColorBoxes.TRANSPARENT)

    # ========================= //Primary// =========================
    CIRCLE_PRIMARY = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_PRIMARY)
    CIRCLE_PRIMARY_75 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_PRIMARY_75)
    CIRCLE_PRIMARY_50 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_PRIMARY_50)
    CIRCLE_PRIMARY_25 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_PRIMARY_25)
    CIRCLE_PRIMARY_10 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_PRIMARY_10)

    CIRCLE_HIDDEN_PRIMARY = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_PRIMARY_HIDDEN)
    CIRCLE_HIDDEN_PRIMARY_75 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_PRIMARY_HIDDEN_75)
    CIRCLE_HIDDEN_PRIMARY_50 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_PRIMARY_HIDDEN_50)
    CIRCLE_HIDDEN_PRIMARY_25 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_PRIMARY_HIDDEN_25)
    CIRCLE_HIDDEN_PRIMARY_10 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_PRIMARY_HIDDEN_10)

    ROUNDED_PRIMARY = Background(border_radius=12, color=ColorBoxes.HOVERABLE_PRIMARY)
    ROUNDED_PRIMARY_75 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_PRIMARY_75)
    ROUNDED_PRIMARY_50 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_PRIMARY_50)
    ROUNDED_PRIMARY_25 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_PRIMARY_25)
    ROUNDED_PRIMARY_10 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_PRIMARY_10)

    ROUNDED_HIDDEN_PRIMARY = Background(border_radius=12, color=ColorBoxes.HOVERABLE_PRIMARY_HIDDEN)
    ROUNDED_HIDDEN_PRIMARY_75 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_PRIMARY_HIDDEN_75)
    ROUNDED_HIDDEN_PRIMARY_50 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_PRIMARY_HIDDEN_50)
    ROUNDED_HIDDEN_PRIMARY_25 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_PRIMARY_HIDDEN_25)
    ROUNDED_HIDDEN_PRIMARY_10 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_PRIMARY_HIDDEN_10)

    # ========================= //Warning// =========================
    CIRCLE_WARNING = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_WARNING)
    CIRCLE_WARNING_75 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_WARNING_75)
    CIRCLE_WARNING_50 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_WARNING_50)
    CIRCLE_WARNING_25 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_WARNING_25)

    CIRCLE_HIDDEN_WARNING = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_WARNING_HIDDEN)
    CIRCLE_HIDDEN_WARNING_75 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_WARNING_HIDDEN_75)
    CIRCLE_HIDDEN_WARNING_50 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_WARNING_HIDDEN_50)
    CIRCLE_HIDDEN_WARNING_25 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_WARNING_HIDDEN_25)

    ROUNDED_WARNING = Background(border_radius=12, color=ColorBoxes.HOVERABLE_WARNING)
    ROUNDED_WARNING_75 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_WARNING_75)
    ROUNDED_WARNING_50 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_WARNING_50)
    ROUNDED_WARNING_25 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_WARNING_25)

    ROUNDED_HIDDEN_WARNING = Background(border_radius=12, color=ColorBoxes.HOVERABLE_WARNING_HIDDEN)
    ROUNDED_HIDDEN_WARNING_75 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_WARNING_HIDDEN_75)
    ROUNDED_HIDDEN_WARNING_50 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_WARNING_HIDDEN_50)
    ROUNDED_HIDDEN_WARNING_25 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_WARNING_HIDDEN_25)

    # ========================= //Danger// =========================
    CIRCLE_DANGER = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_DANGER)
    CIRCLE_DANGER_75 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_DANGER_75)
    CIRCLE_DANGER_50 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_DANGER_50)
    CIRCLE_DANGER_25 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_DANGER_25)

    CIRCLE_HIDDEN_DANGER = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_DANGER_HIDDEN)
    CIRCLE_HIDDEN_DANGER_75 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_DANGER_HIDDEN_75)
    CIRCLE_HIDDEN_DANGER_50 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_DANGER_HIDDEN_50)
    CIRCLE_HIDDEN_DANGER_25 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_DANGER_HIDDEN_25)
    CIRCLE_HIDDEN_DANGER_10 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_DANGER_HIDDEN_10)
    CIRCLE_DANGER_10 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_DANGER_10)

    ROUNDED_HIDDEN_DANGER = Background(border_radius=12, color=ColorBoxes.HOVERABLE_DANGER_HIDDEN)
    ROUNDED_HIDDEN_DANGER_75 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_DANGER_HIDDEN_75)
    ROUNDED_HIDDEN_DANGER_50 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_DANGER_HIDDEN_50)
    ROUNDED_HIDDEN_DANGER_25 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_DANGER_HIDDEN_25)

    ROUNDED_DANGER = Background(border_radius=12, color=ColorBoxes.HOVERABLE_DANGER)
    ROUNDED_DANGER_75 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_DANGER_75)
    ROUNDED_DANGER_50 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_DANGER_50)
    ROUNDED_DANGER_25 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_DANGER_25)

    # ========================= //Black// =========================
    CIRCLE_BLACK = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_BLACK)
    CIRCLE_BLACK_75 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_BLACK_75)
    CIRCLE_BLACK_50 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_BLACK_50)
    CIRCLE_BLACK_25 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_BLACK_25)

    CIRCLE_HIDDEN_BLACK = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_BLACK_HIDDEN)
    CIRCLE_HIDDEN_BLACK_75 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_BLACK_HIDDEN_75)
    CIRCLE_HIDDEN_BLACK_50 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_BLACK_HIDDEN_50)
    CIRCLE_HIDDEN_BLACK_25 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_BLACK_HIDDEN_25)

    ROUNDED_BLACK = Background(border_radius=12, color=ColorBoxes.HOVERABLE_BLACK)
    ROUNDED_BLACK_75 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_BLACK_75)
    ROUNDED_BLACK_50 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_BLACK_50)
    ROUNDED_BLACK_25 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_BLACK_25)

    ROUNDED_HIDDEN_BLACK = Background(border_radius=12, color=ColorBoxes.HOVERABLE_BLACK_HIDDEN)
    ROUNDED_HIDDEN_BLACK_75 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_BLACK_HIDDEN_75)
    ROUNDED_HIDDEN_BLACK_50 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_BLACK_HIDDEN_50)
    ROUNDED_HIDDEN_BLACK_25 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_BLACK_HIDDEN_25)

    # ========================= //White// =========================
    CIRCLE_WHITE = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_WHITE)
    CIRCLE_WHITE_75 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_WHITE_75)
    CIRCLE_WHITE_50 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_WHITE_50)
    CIRCLE_WHITE_25 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_WHITE_25)

    CIRCLE_HIDDEN_WHITE = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_WHITE_HIDDEN)
    CIRCLE_HIDDEN_WHITE_75 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_WHITE_HIDDEN_75)
    CIRCLE_HIDDEN_WHITE_50 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_WHITE_HIDDEN_50)
    CIRCLE_HIDDEN_WHITE_25 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_WHITE_HIDDEN_25)

    ROUNDED_WHITE = Background(border_radius=12, color=ColorBoxes.HOVERABLE_WHITE)
    ROUNDED_WHITE_75 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_WHITE_75)
    ROUNDED_WHITE_50 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_WHITE_50)
    ROUNDED_WHITE_25 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_WHITE_25)

    ROUNDED_HIDDEN_WHITE = Background(border_radius=12, color=ColorBoxes.HOVERABLE_WHITE_HIDDEN)
    ROUNDED_HIDDEN_WHITE_75 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_WHITE_HIDDEN_75)
    ROUNDED_HIDDEN_WHITE_50 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_WHITE_HIDDEN_50)
    ROUNDED_HIDDEN_WHITE_25 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_WHITE_HIDDEN_25)

    # ========================= //Gray// =========================
    CIRCLE_GRAY = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_GRAY)
    CIRCLE_GRAY_75 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_GRAY_75)
    CIRCLE_GRAY_50 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_GRAY_50)
    CIRCLE_GRAY_25 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_GRAY_25)
    CIRCLE_GRAY_10 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_GRAY_10)

    CIRCLE_HIDDEN_GRAY = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_GRAY_HIDDEN)
    CIRCLE_HIDDEN_GRAY_75 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_GRAY_HIDDEN_75)
    CIRCLE_HIDDEN_GRAY_50 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_GRAY_HIDDEN_50)
    CIRCLE_HIDDEN_GRAY_25 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_GRAY_HIDDEN_25)
    CIRCLE_HIDDEN_GRAY_10 = Background(border_radius=0.5, color=ColorBoxes.HOVERABLE_GRAY_HIDDEN_10)

    ROUNDED_GRAY = Background(border_radius=12, color=ColorBoxes.HOVERABLE_GRAY)
    ROUNDED_GRAY_75 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_GRAY_75)
    ROUNDED_GRAY_50 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_GRAY_50)
    ROUNDED_GRAY_25 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_GRAY_25)

    ROUNDED_HIDDEN_GRAY = Background(border_radius=12, color=ColorBoxes.HOVERABLE_GRAY_HIDDEN)
    ROUNDED_HIDDEN_GRAY_75 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_GRAY_HIDDEN_75)
    ROUNDED_HIDDEN_GRAY_50 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_GRAY_HIDDEN_50)
    ROUNDED_HIDDEN_GRAY_25 = Background(border_radius=12, color=ColorBoxes.HOVERABLE_GRAY_HIDDEN_25)


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
    def init_value():
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


class Images:
    ERROR_PLAYLIST: bytes = Bytes.get_bytes_from_file("assets\images\defaults\oops.png")
    DOWNLOAD: bytes = Bytes.get_bytes_from_file("assets\images\defaults\download.png")
    EDIT: bytes = Bytes.get_bytes_from_file("assets\images\defaults\edit.png")
    DELETE: bytes = Bytes.get_bytes_from_file("assets\images\defaults\delete.png")
    DEFAULT_SONG_COVER: bytes = Bytes.get_bytes_from_file("assets\images\defaults\song_cover.jpg")
    DEFAULT_PLAYLIST_COVER: bytes = Bytes.get_bytes_from_file("assets\images\defaults\playlist_cover.jpg")
    FAVOURITES_PLAYLIST_COVER: bytes = Bytes.get_bytes_from_file("assets\images\defaults\playlist_favourite_cover.jpg")
    NULL_IMAGE: bytes = Bytes.get_bytes_from_file("assets\images\defaults\playlist_cover.jpg")


class Cursors:
    HAND: QCursor = None
    DEFAULT: QCursor = None

    @staticmethod
    def init_value():
        Cursors.HAND = QCursor(Qt.PointingHandCursor)
        Cursors.DEFAULT = QCursor(Qt.ArrowCursor)
