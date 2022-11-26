from typing import Optional, Union

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QWidget

from modules.helpers.PixmapHelper import PixmapHelper
from modules.helpers.types.Decorators import override
from modules.models.view.builder.FontBuilder import FontBuilder
from modules.models.view.builder.TextStyle import TextStyle
from modules.statics.view.Material import ColorBoxes
from modules.views.ViewComponent import ViewComponent
from modules.widgets.ImageViewer import ImageViewer
from modules.widgets.LabelWithDefaultText import LabelWithDefaultText


class PlaylistInfoView(QVBoxLayout, ViewComponent):
    __cover: ImageViewer
    __text_area: QVBoxLayout
    __label_title: LabelWithDefaultText
    __label_total_song: LabelWithDefaultText

    def __init__(self, parent: Optional["QWidget"] = None):
        super(PlaylistInfoView, self).__init__(parent)
        self.__init_ui()
        self.set_title("Library")
        self.set_total_song(0)

    def __init_ui(self):
        self.setSpacing(12)
        self.__cover = ImageViewer()
        self.__cover.setFixedSize(320, 320)

        self.__text_area = QVBoxLayout()
        self.__text_area.setSpacing(0)
        self.__label_title = LabelWithDefaultText.build(
            width=128,
            font=FontBuilder.build(size=20, bold=True),
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            dark_mode_style=TextStyle(text_color=ColorBoxes.WHITE)
        )
        self.__label_total_song = LabelWithDefaultText.build(
            width=128,
            font=FontBuilder.build(size=10, bold=False),
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            dark_mode_style=TextStyle(text_color=ColorBoxes.WHITE)
        )

        self.__text_area.addWidget(self.__label_title)
        self.__text_area.addWidget(self.__label_total_song)

        self.addWidget(self.__cover)
        self.addLayout(self.__text_area)
        self.addStretch()

    def set_info(self, cover: bytes, label: str, song_count: int) -> None:
        self.set_cover(cover)
        self.set_title(label)
        self.set_total_song(song_count)

    def set_cover(self, cover: bytes) -> None:
        self.__cover.setPixmap(self.__get_cover_pixmap(cover))

    def set_default_cover(self, cover: bytes) -> None:
        self.__cover.set_default_pixmap(self.__get_cover_pixmap(cover))

    def set_title(self, name: str) -> None:
        self.__label_title.setText(name)

    def set_total_song(self, song_count: int) -> None:
        self.__label_total_song.setText(f"{str(song_count)} TRACKS")

    @override
    def apply_light_mode(self) -> None:
        self.__label_title.apply_light_mode()
        self.__label_total_song.apply_light_mode()

    @override
    def apply_dark_mode(self) -> None:
        self.__label_title.apply_dark_mode()
        self.__label_total_song.apply_dark_mode()

    @staticmethod
    def __get_cover_pixmap(pixmap_byte: bytes) -> Union[QPixmap, None]:
        if pixmap_byte is None:
            return None
        return PixmapHelper.get_edited_pixmap_from_bytes(pixmap_byte, width=320, height=320, radius=24)
