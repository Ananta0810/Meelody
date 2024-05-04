from app.common.models import Song
from app.components.base import Cover, Factory, LabelWithDefaultText, CoverProps, CheckBox
from app.components.widgets import ExtendableStyleWidget, FlexBox
from app.helpers.others import Times
from app.resource.qt import Images


class SongRow(ExtendableStyleWidget):
    def __init__(self, song: Song):
        self.__song = song

        super().__init__()
        super()._initComponent()

        self.__displaySongInfo()

    def _createUI(self) -> None:
        self.setClassName("bg-none hover:bg-gray-8 border-b border-gray-12")
        self.setContentsMargins(0, 0, 0, 0)

        self._mainLayout = FlexBox()
        self._mainLayout.setContentsMargins(0, 8, 0, 8)
        self._mainLayout.setSpacing(0)
        self.setLayout(self._mainLayout)

        # ================================================= INFO  =================================================

        self._checkBox = CheckBox()
        self._checkBox.setFixedWidth(16)

        self._cover = Cover(self)
        self._cover.setFixedSize(64, 64)
        self._cover.setDefaultCover(CoverProps.fromBytes(Images.DEFAULT_SONG_COVER, width=64, height=64, radius=12))

        self._titleLabel = LabelWithDefaultText()
        self._titleLabel.enableEllipsis()
        self._titleLabel.setFixedWidth(240)
        self._titleLabel.setFont(Factory.createFont(size=10))
        self._titleLabel.setClassName("text-black dark:text-white")

        self._artistLabel = LabelWithDefaultText()
        self._artistLabel.enableEllipsis()
        self._artistLabel.setFixedWidth(128)
        self._artistLabel.setFont(Factory.createFont(size=10))
        self._artistLabel.setClassName("text-gray")

        self._lengthLabel = LabelWithDefaultText()
        self._lengthLabel.enableEllipsis()
        self._lengthLabel.setFixedWidth(64)
        self._lengthLabel.setFont(Factory.createFont(size=10))
        self._lengthLabel.setClassName("text-gray")

        self._mainLayout.addSpacing(24)
        self._mainLayout.addWidget(self._checkBox)
        self._mainLayout.addSpacing(24)
        self._mainLayout.addWidget(self._cover)
        self._mainLayout.addSpacing(24)
        self._mainLayout.addWidget(self._titleLabel)
        self._mainLayout.addSpacing(24)
        self._mainLayout.addWidget(self._artistLabel)
        self._mainLayout.addSpacing(24)
        self._mainLayout.addWidget(self._lengthLabel)

    def __displaySongInfo(self) -> None:
        self._cover.setCover(CoverProps.fromBytes(self.__song.getCover(), width=64, height=64, radius=12))
        self._titleLabel.setText(self.__song.getTitle())
        self._artistLabel.setText(self.__song.getArtist())
        self._lengthLabel.setText(Times.toString(self.__song.getLength()))
        self._checkBox.setFixedHeight(self.sizeHint().height())
