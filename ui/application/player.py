# from PyQt5 import QtCore, QtGui, QtWidgets
from sys import path
from threading import Thread

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

path.append(".")
from ui.base.colors import Colors
from ui.base.icons import Icons
from ui.base.text import Text
from ui.components.buttons.icon_button_factory import IconButtonFactory
from ui.utils.color_utils import ColorUtils
from ui.utils.icon_utils import IconUtils


class ApplicationPlayer(QWidget):
    play_song_signal = pyqtSignal()
    love_signal = pyqtSignal()
    shuffle_signal = pyqtSignal()

    def setupUi(self):
        self.setObjectName("Form")
        self.setFixedSize(1368, 100)

        self._run_time_slider = True
        icons = Icons()
        iconButtonFactory = IconButtonFactory()

        self.player_box = QWidget(self)
        self.player_box.setGeometry(QRect(0, 0, 1368, 100))
        self.player_box.setObjectName("player_box")
        self.player_box.setStyleSheet("QPushButton{border:none}")
        self.current_song_img = QLabel(self.player_box)
        self.current_song_img.setGeometry(QRect(54, 18, 64, 64))
        self.current_song_img.setObjectName("ui_current_song_img")

        self.current_song_title = QLabel(self.player_box)
        self.current_song_title.setGeometry(QRect(130, 26, 160, 30))
        self.current_song_title.setFont(Text.FONT_PRIMARY_SMALL)
        self.current_song_title.setText("Song's title")
        self.current_song_title.setObjectName("ui_current_song_title")

        self.current_song_artist = QLabel(self.player_box)
        self.current_song_artist.setGeometry(QRect(130, 46, 140, 30))
        # self.current_song_artist.setFont(self._ui.font_size_small)
        # self.current_song_artist.setPalette(self._ui.gray_text)
        self.current_song_artist.setText("Song's artist")
        self.current_song_artist.setObjectName("ui_current_song_artist")

        self.play_song_btn = QPushButton(self.player_box)
        self.play_song_btn.setGeometry(QRect(361, 27, 48, 48))
        # self.play_song_btn.setCursor(self._ui.hand_cursor)
        self.play_song_btn.setStyleSheet(
            "QPushButton{image:url(images/icons/play-player.png);margin:2px}\n"
            "QPushButton::hover{margin:0px;background:transparent}"
            "QPushButton::checked{image:url(images/icons/pause-player.png)}"
        )
        self.play_song_btn.setCheckable(True)
        self.play_song_btn.setObjectName("ui_play_song_btn")
        self.prev_song_btn = QPushButton(self.player_box)
        self.prev_song_btn.setGeometry(QRect(311, 27, 48, 48))
        # self.prev_song_btn.setCursor(self._ui.hand_cursor)
        self.prev_song_btn.setStyleSheet(
            "QPushButton{image:url(images/icons/previous.png);margin:2px}\n"
            "QPushButton::hover{margin:0px;background:transparent}"
        )
        self.prev_song_btn.setObjectName("ui_prev_song_btn")
        self.next_song_btn = QPushButton(self.player_box)
        self.next_song_btn.setGeometry(QRect(411, 27, 48, 48))
        # self.next_song_btn.setCursor(self._ui.hand_cursor)
        self.next_song_btn.setStyleSheet(
            "QPushButton{image:url(images/icons/next.png);margin:2px}\n"
            "QPushButton::hover{margin:0px;background:transparent}"
        )
        self.next_song_btn.setObjectName("ui_next_song_btn")

        self.time_slider = QSlider(self.player_box)
        self.time_slider.setGeometry(QRect(556, 44, 250, 12))
        # self.time_slider.setCursor(self._ui.hand_cursor)
        self.time_slider.setStyleSheet(
            "QSlider{background:transparent;border:none}\n"
            "QSlider::groove{border:none}\n"
            "QSlider::handle{background:#8040ff;border:none;border-radius:5px;width:10px;margin: 1px 1px 1px 1px}\n"
            "QSlider::sub-page{background:#8040ff;border:none;border-radius:1px;margin:5px 1px 5px}\n"
            "QSlider::add-page{background:#c8c8c8;border:none;border-radius:1px;margin:5px 1px 5px}\n"
            "QSlider::handle::hover{background:#8040ff;border:none;border-radius:6px;width:12px;margin: 0px 0px 0px}"
        )
        self.time_slider.setProperty("value", 0)
        self.time_slider.setOrientation(Qt.Horizontal)
        self.time_slider.setTickPosition(QSlider.NoTicks)
        self.time_slider.setObjectName("ui_time_slider")

        self.time_playing = QLabel(self.player_box)
        self.time_playing.setGeometry(QRect(500, 40, 60, 20))
        # self.time_playing.setAlignment(self._ui.align_center)
        # self.time_playing.setFont(self._ui.font_size_small)
        # self.time_playing.setPalette(self._ui.black_text)
        self.time_playing.setObjectName("ui_time_playing")

        self.time_end = QLabel(self.player_box)
        self.time_end.setGeometry(QRect(806, 40, 61, 21))
        # self.time_end.setAlignment(self._ui.align_center)
        # self.time_end.setFont(self._ui.font_size_small)
        # self.time_end.setPalette(self._ui.black_text)
        self.time_end.setObjectName("ui_time_end")

        self.music_interaction_buttons = QWidget(self.player_box)
        self.music_interaction_buttons.setGeometry(QRect(920, 0, 220, 100))
        self.music_interaction_buttons.setObjectName("music_interaction_buttons")
        self.music_interaction_buttons_layout = QHBoxLayout(
            self.music_interaction_buttons
        )
        self.music_interaction_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.music_interaction_buttons_layout.setObjectName(
            "music_interaction_buttons_layout"
        )

        self.loop_btn = iconButtonFactory.createButton(
            type="checkable-hidden-primary-danger",
            name="loop_btn",
            padding=1,
            iconSize=icons.SIZES.SMALL,
            icon=IconUtils.changeColor(
                icons.LOOP, ColorUtils.getQColorFromColor(Colors.PRIMARY)
            ),
            checkedIcon=IconUtils.changeColor(
                icons.LOOP, ColorUtils.getQColorFromColor(Colors.DANGER)
            ),
            cursor=QCursor(Qt.PointingHandCursor),
            parent=self.music_interaction_buttons,
        )
        self.music_interaction_buttons_layout.addWidget(self.loop_btn)

        self.shuffle_btn = iconButtonFactory.createButton(
            type="checkable-hidden-primary-danger",
            name="shuffle_btn",
            padding=1,
            iconSize=icons.SIZES.SMALL,
            icon=IconUtils.changeColor(
                icons.SHUFFLE, ColorUtils.getQColorFromColor(Colors.PRIMARY)
            ),
            checkedIcon=IconUtils.changeColor(
                icons.SHUFFLE, ColorUtils.getQColorFromColor(Colors.DANGER)
            ),
            cursor=QCursor(Qt.PointingHandCursor),
            parent=self.music_interaction_buttons,
        )
        self.music_interaction_buttons_layout.addWidget(self.shuffle_btn)

        self.love_btn = iconButtonFactory.createButton(
            type="checkable-hidden-primary-danger",
            name="love_btn",
            padding=1,
            iconSize=icons.SIZES.SMALL,
            icon=IconUtils.changeColor(
                icons.LOVE, ColorUtils.getQColorFromColor(Colors.PRIMARY)
            ),
            checkedIcon=IconUtils.changeColor(
                icons.LOVE, ColorUtils.getQColorFromColor(Colors.DANGER)
            ),
            cursor=QCursor(Qt.PointingHandCursor),
            parent=self.music_interaction_buttons,
        )
        self.music_interaction_buttons_layout.addWidget(self.love_btn)

        self.volume_btn = iconButtonFactory.createButton(
            type="checkable-hidden-primary",
            name="volume_btn",
            padding=1,
            iconSize=icons.SIZES.SMALL,
            icon=IconUtils.changeColor(
                icons.VOLUME_UP, ColorUtils.getQColorFromColor(Colors.PRIMARY)
            ),
            cursor=QCursor(Qt.PointingHandCursor),
            parent=self.music_interaction_buttons,
        )
        self.music_interaction_buttons_layout.addWidget(self.volume_btn)

        self.volume_slider = QSlider(self.player_box)
        self.volume_slider.setGeometry(QRect(1090, 30, 160, 40))
        self.volume_slider.setStyleSheet(
            "QSlider{background:rgba(160,160,160,0.2);border:none;border-radius:12px}\n"
            "QSlider::groove{border:none}\n"
            "QSlider::handle{background:#8040ff;border:none;border-radius:5px;width:10px;margin:15px 16px 15px}\n"
            "QSlider::sub-page{background:#8040ff;border:none;border-radius:1px;margin:19px 0px 19px 16px}\n"
            "QSlider::add-page{background:#c8c8c8;border:none;border-radius:1px;margin:19px 16px 19px 0px}\n"
            "QSlider::hover{background:rgba(160,160,160,0.25);border:none;border-radius:12px}\n"
            "QSlider::handle:hover{border:none;border-radius:6px;width:12px;margin:14px 15px 14px}"
        )
        self.volume_slider.setOrientation(Qt.Horizontal)
        self.volume_slider.setSliderPosition(100)
        # self.volume_slider.setCursor(self._ui.hand_cursor)
        self.volume_slider.setObjectName("ui_volume_slider")
        self.volume_slider.setVisible(False)

        self.timer_btn = iconButtonFactory.createButton(
            type="checkable-hidden-primary",
            name="timer_btn",
            padding=1,
            iconSize=icons.SIZES.SMALL,
            icon=IconUtils.changeColor(
                icons.TIMER, ColorUtils.getQColorFromColor(Colors.PRIMARY)
            ),
            cursor=QCursor(Qt.PointingHandCursor),
            parent=self.player_box,
        )
        self.timer_btn.setGeometry(QRect(1300, 30, 0, 0))

        self.timer_box = QLineEdit(self.player_box)
        self.timer_box.setGeometry(QRect(1170, 30, 120, 40))
        self.timer_box.setStyleSheet(
            "QLineEdit{background:rgba(160,160,160,0.2);border-radius:12px;padding:0px 16px 0px}\n"
            "QLineEdit::hover{background:rgba(160,160,160,0.25)}"
        )
        # self.timer_box.setAlignment(self._ui.align_center)
        self.timer_box.setPlaceholderText("Enter Minute")
        self.timer_box.setValidator(QIntValidator())
        self.timer_box.setObjectName("ui_timer_box")
        self.timer_box.setVisible(False)

        # self.connect_signal()
        QMetaObject.connectSlotsByName(self)

    # def connect_signal(self):
    #     self.play_song_btn.clicked.connect(self.press_play_btn)
    #     self.prev_song_btn.clicked.connect(self.play_previous_song)
    #     self.next_song_btn.clicked.connect(self.play_next_song)

    #     self.time_slider.sliderPressed.connect(self.pause_time_slider)
    #     self.time_slider.sliderReleased.connect(self.unpause_time_slider)
    #     self.shuffle_btn.clicked.connect(self.press_shuffle_btn)
    #     self.love_btn.clicked.connect(self.press_love_btn)

    #     self.timer.clicked.connect(self.show_timer)
    #     self.timer_box.returnPressed.connect(self.set_timer)

    #     self.volume_btn.clicked.connect(self.show_volume_slider)
    #     self.volume_slider.valueChanged.connect(self.set_song_volume)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    Form = QWidget()
    ui = ApplicationPlayer(Form)
    ui.setupUi()
    Form.setGeometry(QRect(276, 490, 1368, 100))

    Form.show()
    sys.exit(app.exec_())
