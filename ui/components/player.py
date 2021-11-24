# from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from appIcon import UiIcons
from MyPlayer import MyPlayer
from threading import Thread
from ui_source import *
from Validation import MyString
from test import CurrentPlaylist


class ApplicationPlayer(QWidget):
    play_song_signal = pyqtSignal()
    love_signal = pyqtSignal()
    shuffle_signal = pyqtSignal()

    def setupUi(self):
        self.setObjectName("Form")
        self.resize(1368, 100)

        self._ui = UiIcons()
        self._player = MyPlayer()
        self._player._playlist = CurrentPlaylist().playlist
        self._player.set_current_song_index(0)

        self._run_time_slider = True
        self._string = MyString()

        self.player_box = QWidget(self)
        self.player_box.setGeometry(QRect(0, 0, 1368, 100))
        self.player_box.setObjectName("player_box")
        self.player_box.setStyleSheet("QPushButton{border:none}")
        self.ui_current_song_img = Label(self.player_box)
        self.ui_current_song_img.setGeometry(QRect(54, 18, 64, 64))
        self.ui_current_song_img.setObjectName("ui_current_song_img")

        self.ui_current_song_title = QLabel(self.player_box)
        self.ui_current_song_title.setGeometry(QRect(130, 26, 160, 30))
        self.ui_current_song_title.setFont(self._ui.font_size_small)
        self.ui_current_song_title.setObjectName("ui_current_song_title")

        self.ui_current_song_artist = QLabel(self.player_box)
        self.ui_current_song_artist.setGeometry(QRect(130, 46, 140, 30))
        self.ui_current_song_artist.setFont(self._ui.font_size_small)
        self.ui_current_song_artist.setPalette(self._ui.gray_text)
        self.ui_current_song_artist.setObjectName("ui_current_song_artist")

        self.ui_play_song_btn = QPushButton(self.player_box)
        self.ui_play_song_btn.setGeometry(QRect(361, 27, 48, 48))
        self.ui_play_song_btn.setCursor(self._ui.hand_cursor)
        self.ui_play_song_btn.setStyleSheet(
            "QPushButton{image:url(images/icons/play-player.png);margin:2px}\n"
            "QPushButton::hover{margin:0px;background:transparent}"
            "QPushButton::checked{image:url(images/icons/pause-player.png)}"
        )
        self.ui_play_song_btn.setCheckable(True)
        self.ui_play_song_btn.setObjectName("ui_play_song_btn")
        self.ui_prev_song_btn = QPushButton(self.player_box)
        self.ui_prev_song_btn.setGeometry(QRect(311, 27, 48, 48))
        self.ui_prev_song_btn.setCursor(self._ui.hand_cursor)
        self.ui_prev_song_btn.setStyleSheet(
            "QPushButton{image:url(images/icons/previous.png);margin:2px}\n"
            "QPushButton::hover{margin:0px;background:transparent}"
        )
        self.ui_prev_song_btn.setObjectName("ui_prev_song_btn")
        self.ui_next_song_btn = QPushButton(self.player_box)
        self.ui_next_song_btn.setGeometry(QRect(411, 27, 48, 48))
        self.ui_next_song_btn.setCursor(self._ui.hand_cursor)
        self.ui_next_song_btn.setStyleSheet(
            "QPushButton{image:url(images/icons/next.png);margin:2px}\n"
            "QPushButton::hover{margin:0px;background:transparent}"
        )
        self.ui_next_song_btn.setObjectName("ui_next_song_btn")

        self.ui_time_slider = QSlider(self.player_box)
        self.ui_time_slider.setGeometry(QRect(556, 44, 250, 12))
        self.ui_time_slider.setCursor(self._ui.hand_cursor)
        self.ui_time_slider.setStyleSheet(
            "QSlider{background:transparent;border:none}\n"
            "QSlider::groove{border:none}\n"
            "QSlider::handle{background:#8040ff;border:none;border-radius:5px;width:10px;margin: 1px 1px 1px 1px}\n"
            "QSlider::sub-page{background:#8040ff;border:none;border-radius:1px;margin:5px 1px 5px}\n"
            "QSlider::add-page{background:#c8c8c8;border:none;border-radius:1px;margin:5px 1px 5px}\n"
            "QSlider::handle::hover{background:#8040ff;border:none;border-radius:6px;width:12px;margin: 0px 0px 0px}"
        )
        self.ui_time_slider.setProperty("value", 0)
        self.ui_time_slider.setOrientation(Qt.Horizontal)
        self.ui_time_slider.setTickPosition(QSlider.NoTicks)
        self.ui_time_slider.setObjectName("ui_time_slider")

        self.ui_time_playing = QLabel(self.player_box)
        self.ui_time_playing.setGeometry(QRect(500, 40, 60, 20))
        self.ui_time_playing.setAlignment(self._ui.align_center)
        self.ui_time_playing.setFont(self._ui.font_size_small)
        self.ui_time_playing.setPalette(self._ui.black_text)
        self.ui_time_playing.setObjectName("ui_time_playing")

        self.ui_time_end = QLabel(self.player_box)
        self.ui_time_end.setGeometry(QRect(806, 40, 61, 21))
        self.ui_time_end.setAlignment(self._ui.align_center)
        self.ui_time_end.setFont(self._ui.font_size_small)
        self.ui_time_end.setPalette(self._ui.black_text)
        self.ui_time_end.setObjectName("ui_time_end")

        self.ui_loop_btn = QPushButton(self.player_box)
        self.ui_loop_btn.setGeometry(QRect(920, 30, 40, 40))
        self.ui_loop_btn.setCursor(self._ui.hand_cursor)
        self.ui_loop_btn.setStyleSheet(
            "QPushButton{image:url(images/icons/unloop.png)}\n"
            "QPushButton::checked{image: url(images/icons/loop.png);}"
        )
        self.ui_loop_btn.setCheckable(True)
        self.ui_loop_btn.setChecked(True)
        self.ui_loop_btn.setObjectName("ui_loop_btn")
        self.ui_shuffle_btn = QPushButton(self.player_box)
        self.ui_shuffle_btn.setGeometry(QRect(960, 30, 40, 40))
        self.ui_shuffle_btn.setCursor(self._ui.hand_cursor)
        self.ui_shuffle_btn.setStyleSheet(
            "QPushButton{image:url(images/icons/unshuffle.png)}\n"
            "QPushButton::checked{image:url(images/icons/shuffle.png)}"
        )
        self.ui_shuffle_btn.setCheckable(True)
        self.ui_shuffle_btn.setObjectName("ui_shuffle_btn")
        self.ui_love_btn = QPushButton(self.player_box)
        self.ui_love_btn.setGeometry(QRect(1000, 30, 40, 40))
        self.ui_love_btn.setCursor(self._ui.hand_cursor)
        self.ui_love_btn.setStyleSheet(
            "QPushButton{image:url(images/icons/love.png)}\n"
            "QPushButton::checked{image:url(images/icons/unlove.png)}"
        )
        self.ui_love_btn.setCheckable(True)
        self.ui_love_btn.setObjectName("ui_love_btn")
        self.ui_volume_btn = QPushButton(self.player_box)
        self.ui_volume_btn.setGeometry(QRect(1040, 30, 40, 40))
        self.ui_volume_btn.setCursor(self._ui.hand_cursor)
        self.ui_volume_btn.setIcon(self._ui.volume_up_icon)
        self.ui_volume_btn.setIconSize(self._ui.icon_size_40)
        self.ui_volume_btn.setCheckable(True)
        self.ui_volume_btn.setObjectName("ui_volume_btn")
        self.ui_volume_slider = QSlider(self.player_box)
        self.ui_volume_slider.setGeometry(QRect(1090, 30, 160, 40))
        self.ui_volume_slider.setStyleSheet(
            "QSlider{background:rgba(160,160,160,0.2);border:none;border-radius:12px}\n"
            "QSlider::groove{border:none}\n"
            "QSlider::handle{background:#8040ff;border:none;border-radius:5px;width:10px;margin:15px 16px 15px}\n"
            "QSlider::sub-page{background:#8040ff;border:none;border-radius:1px;margin:19px 0px 19px 16px}\n"
            "QSlider::add-page{background:#c8c8c8;border:none;border-radius:1px;margin:19px 16px 19px 0px}\n"
            "QSlider::hover{background:rgba(160,160,160,0.25);border:none;border-radius:12px}\n"
            "QSlider::handle:hover{border:none;border-radius:6px;width:12px;margin:14px 15px 14px}"
        )
        self.ui_volume_slider.setOrientation(Qt.Horizontal)
        self.ui_volume_slider.setSliderPosition(100)
        self.ui_volume_slider.setCursor(self._ui.hand_cursor)
        self.ui_volume_slider.setObjectName("ui_volume_slider")
        self.ui_volume_slider.setVisible(False)
        self.ui_timer = QPushButton(self.player_box)
        self.ui_timer.setGeometry(QRect(1300, 30, 40, 40))
        self.ui_timer.setCursor(self._ui.hand_cursor)
        self.ui_timer.setIcon(self._ui.timer_icon)
        self.ui_timer.setIconSize(self._ui.icon_size_40)
        self.ui_timer.setStyleSheet(
            "QPushButton::hover{background:rgba(160,160,160,0.25);border-radius:20px}"
        )
        self.ui_timer.setCheckable(True)
        self.ui_timer.setObjectName("ui_timer")

        self.ui_timer_box = QLineEdit(self.player_box)
        self.ui_timer_box.setGeometry(QRect(1170, 30, 120, 40))
        self.ui_timer_box.setStyleSheet(
            "QLineEdit{background:rgba(160,160,160,0.2);border-radius:12px;padding:0px 16px 0px}\n"
            "QLineEdit::hover{background:rgba(160,160,160,0.25)}"
        )
        self.ui_timer_box.setAlignment(self._ui.align_center)
        self.ui_timer_box.setPlaceholderText("Enter Minute")
        self.ui_timer_box.setValidator(QIntValidator())
        self.ui_timer_box.setObjectName("ui_timer_box")
        self.ui_timer_box.setVisible(False)

        self.display_song_info()
        self.connect_signal()
        QMetaObject.connectSlotsByName(self)

    def dark_mode(self):
        self.ui_current_song_title.setPalette(self._ui.white_text)
        self.ui_time_playing.setPalette(self._ui.white_text)
        self.ui_time_end.setPalette(self._ui.white_text)

    def light_mode(self):
        self.ui_current_song_title.setPalette(self._ui.black_text)
        self.ui_time_playing.setPalette(self._ui.black_text)
        self.ui_time_end.setPalette(self._ui.black_text)

    def is_looping(self):
        return self.ui_loop_btn.isChecked()

    def is_shuffling(self):
        return self.ui_shuffle_btn.isChecked()

    def connect_signal(self):
        self.ui_play_song_btn.clicked.connect(self.press_play_btn)
        self.ui_prev_song_btn.clicked.connect(self.play_previous_song)
        self.ui_next_song_btn.clicked.connect(self.play_next_song)

        self.ui_time_slider.sliderPressed.connect(self.pause_time_slider)
        self.ui_time_slider.sliderReleased.connect(self.unpause_time_slider)
        self.ui_shuffle_btn.clicked.connect(self.press_shuffle_btn)
        self.ui_love_btn.clicked.connect(self.press_love_btn)

        self.ui_timer.clicked.connect(self.show_timer)
        self.ui_timer_box.returnPressed.connect(self.set_timer)

        self.ui_volume_btn.clicked.connect(self.show_volume_slider)
        self.ui_volume_slider.valueChanged.connect(self.set_song_volume)

    def press_play_btn(self):
        if self.ui_play_song_btn.isChecked():
            self.thr_play_song()
        else:
            self.pause_song()

    def press_shuffle_btn(self):
        if self.ui_shuffle_btn.isChecked():
            self.shuffle_songs()
        else:
            self.unshuffle_songs()
        self.shuffle_signal.emit()

    def press_love_btn(self):
        self.love_signal.emit()
        self.change_love_state()

    def change_love_state(self):
        self.ui_love_btn.setChecked(self._player._player._song._loved)

    def display_song_info(self):
        if not self._player._player.has_song():
            return

        song = self._player.get_current_song()
        cover = song._cover
        if cover is None:
            cover = self._ui.default_song_cover
        pixmap = self.ui_current_song_img.get_pixmap(cover)
        self.ui_current_song_img.set_pixmap(pixmap, rad=self._ui.SONG_COVER_RADIUS)
        self.ui_current_song_title.setText(song._title)
        self.ui_current_song_artist.setText(song._artist)
        self.ui_time_end.setText(self._string.get_clock_time(song._length))
        self.ui_love_btn.setChecked(song._loved)

    def display_playing_time(self):
        self.ui_time_playing.setText(
            self._string.get_clock_time(self._player._player._time_playing_in_sec)
        )

    def show_timer(self) -> None:
        self.ui_timer_box.setVisible(self.ui_timer.isChecked())
        self.ui_volume_slider.setVisible(False)
        self.ui_volume_btn.setChecked(False)

    def show_volume_slider(self):
        self.ui_volume_slider.setVisible(self.ui_volume_btn.isChecked())
        self.ui_timer_box.setVisible(False)

    def set_song_volume(self):
        volume = self.ui_volume_slider.sliderPosition()
        self._player._player.set_volume(volume)

        if volume == 0:
            self.ui_volume_btn.setIcon(self._ui.volume_silent_icon)
            return

        if volume < 50:
            self.ui_volume_btn.setIcon(self._ui.volume_down_icon)
            return

        self.ui_volume_btn.setIcon(self._ui.volume_up_icon)

    def set_timer(self):
        time_to_shutdown = int(self.ui_timer_box.text())
        self._timer.set_time(time_to_shutdown)
        self.ui_timer_box.clear()
        self.ui_timer_box.hide()
        self.ui_timer.setChecked(False)

    def run_time_slider(self):
        player = self._player._player
        self.ui_time_slider.setSliderPosition(
            int(player._time_playing_in_sec * 100 / player._song._length)
        )

    def pause_time_slider(self):
        self._run_time_slider = False

    def unpause_time_slider(self):
        self._player._player._time_playing_in_sec = (
            self.ui_time_slider.sliderPosition()
            / 100
            * self._player._player._song._length
        )

        # print("Unpaused time slider")
        # print(self._player)
        self._run_time_slider = True

        if self._player._player.is_playing():
            self._player._player.pause()
            self.thr_play_song()
        else:
            self._player._player._time_start_in_sec = (
                self._player._player._time_playing_in_sec
            )

    def change_song(self):
        self.ui_play_song_btn.setChecked(True)
        self.display_song_info()
        self._player._player.stop()
        self.thr_play_song()

    def thr_play_song(self):
        Thread(target=self.play_song).start()

    def play_song(self):
        player = self._player._player
        timer = self._player._timer

        if not player.has_song():
            self.ui_play_song_btn.setChecked(False)
            return

        self.play_song_signal.emit()
        player.ease()
        player.play()

        time_sleep = player._song._length / 100
        if time_sleep > 0.25:
            time_sleep = 0.25

        timer.set_interval(time_sleep)
        player.set_interval(time_sleep)

        while player.is_playing():
            player.run_time_playing()
            self.display_playing_time()

            if self._run_time_slider:
                self.run_time_slider()

            if timer.active():
                timer.run()
                if timer.reach_timer():
                    timer.reset()
                    self.pause_song()

            player.ease()
            if not player.song_ended():
                continue
            if self.is_looping():
                player.rewind()
            else:
                self.play_next_song()

    def pause_song(self):
        self._player._player.pause()
        self.ui_play_song_btn.setChecked(False)

    def play_previous_song(self):
        self._player.previous_song()
        self.change_song()

    def play_next_song(self):
        self._player.next_song()
        self.change_song()

    def shuffle_songs(self):
        self._player.shuffle()

    def unshuffle_songs(self):
        self._player.unshuffle()

    def play_song_at(self, index):
        self._player.set_current_song_index(index)
        self.change_song()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    Form = QWidget()
    ui = ApplicationPlayer(Form)
    ui.setupUi()
    ui.dark_mode()
    Form.show()
    sys.exit(app.exec_())
