from sys import argv, exit, path

path.append(".")
from functools import partial
from threading import Thread
from time import sleep

from entities.song import Song
from models.mixer import Mixer
from models.playlist_songs import PlaylistSongs
from models.timer import Timer
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ui.base.images import ApplicationImage
from ui.layouts.player import UIPlayerMusic
from ui.utils.pixmap_utils import PixmapUtils
from utils.my_file import MyFile


class MusicPlayer:
    def __init__(self, form: QWidget):
        self.ui = UIPlayerMusic(form)
        self.ui.setFixedSize(1368, 100)
        self.ui.setupUi()
        self.defaultSongCoverAsPixmap = self.getDisplayCoverFromBytes(
            ApplicationImage.defaultSongCover,
            self.ui.song_cover.width(),
        )

        self.currentThreadNumber = 0
        self.canRunTimeSlider = True

        songs = PlaylistSongs()
        files = MyFile.getFilesFrom("Library", withExtension="mp3")
        for file in files:
            song = Song(location=file)
            song.title = MyFile.getFileBasename(file)
            song.loadInfo()
            songs.insert(song)

        self.timer = Timer()
        self.mixer = Mixer()
        self.mixer.loadPlaylist(songs)
        self.mixer.load()
        self.showCurrentSongInfo()
        self.connectSignal()

    def connectSignal(self):
        self.ui.play_song_btn.clicked.connect(self.clickedPlayButton)
        self.ui.next_song_btn.clicked.connect(self.nextSong)
        self.ui.previous_song_btn.clicked.connect(self.prevSong)
        self.ui.timer_box.returnPressed.connect(self.setTimer)
        self.ui.volume_slider.valueChanged.connect(self.changeVolume)
        self.ui.time_slider.sliderPressed.connect(self.pauseTimeSlider)
        self.ui.time_slider.sliderReleased.connect(self.unpauseTimeSlider)
        self.ui.shuffle_btn.clicked.connect(self.clickedShuffleSong)
        self.ui.love_btn.clicked.connect(self.loveSong)

    def setTimer(self):
        timerBox = self.ui.timer_box
        timeElapsed: int = int(timerBox.text()) * 60
        self.timer.setTime(timeElapsed)
        timerBox.clear()
        timerBox.hide()

    def clickedShuffleSong(self):
        if self.ui.shuffle_btn.isChecked():
            self.mixer.shuffle()
        else:
            self.mixer.unshuffle()

    def pauseTimeSlider(self):
        self.canRunTimeSlider = False

    def unpauseTimeSlider(self):
        self.canRunTimeSlider = True
        timeStart: float = (
            self.ui.time_slider.sliderPosition()
            / 100
            * self.mixer.getCurrentSong().length
        )
        self.mixer.stop()
        self.mixer.setTimeStart(timeStart)
        self.clickedPlayButton()

    def changeVolume(self):
        volume: int = self.ui.volume_slider.value()
        self.mixer.setVolume(volume)

    def clickedPlayButton(self):
        if not self.ui.play_song_btn.isChecked():
            self.pauseMusic()
            return
        self.mixer.load()
        self.threadPlaySong()

    def pauseMusic(self):
        self.mixer.pause()
        self.ui.play_song_btn.setChecked(False)

    def threadPlaySong(self):
        thread: Thread = Thread(target=self.playMusic)
        self.currentThreadNumber += 1
        thread.start()

    def playMusic(self):
        self.ui.play_song_btn.setChecked(True)
        self.mixer.play()

        threadNumber: int = self.currentThreadNumber
        player = self.mixer
        timer = self.timer
        timer.setInterval(0.25)

        while threadNumber == self.currentThreadNumber and player.isPlaying():
            sleep(0.25)
            self.__doWhilePlayingMusic(player, timer)
            if player.isSongFinished():
                self.doAfterSongFinished()
                break

    def __doWhilePlayingMusic(self, player: Mixer, timer: Timer):
        playingTime = player.getPlayingTime()
        self.ui.displayPlayingTime(playingTime)

        if self.canRunTimeSlider:
            self.ui.runTimeSlider(playingTime, player.getCurrentSong().length)

        if timer.isEnabled():
            self.__runTimer(timer)

    def __runTimer(self, timer: Timer):
        timer.count()
        if not timer.isActive():
            return
        timer.reset()
        self.pauseMusic()

    def doAfterSongFinished(self):
        if self.ui.isLooping():
            self.rewind()
        else:
            self.nextSong()

    def loveSong(self):
        self.mixer.getCurrentSong().reverseLoveState()

    def rewind(self):
        self.mixer.stop()
        self.clickedPlayButton()

    def nextSong(self):
        self.mixer.next()
        self.mixer.load()
        self.showCurrentSongInfo()
        self.threadPlaySong()

    def prevSong(self):
        self.mixer.previous()
        self.mixer.load()
        self.showCurrentSongInfo()
        self.threadPlaySong()

    def showCurrentSongInfo(self):
        song: Song = self.mixer.getCurrentSong()

        coverAsPixmap = (
            self.defaultSongCoverAsPixmap
            if song.cover is None
            else self.getDisplayCoverFromBytes(
                song.cover,
                self.ui.song_cover.width(),
            )
        )
        self.ui.song_cover.setPixmap(coverAsPixmap)
        self.ui.song_title.setText(song.title)
        self.ui.song_artist.setText(song.artist)
        # self.ui.song_artist.setVisible(song.artist is not None)
        self.ui.displayPlayingTime(0)
        self.ui.displayTotalTime(song.length)

    def getDisplayCoverFromBytes(self, byteImage: bytes, width: int) -> QPixmap:
        pixmap = PixmapUtils.getPixmapFromBytes(byteImage)
        pixmap = PixmapUtils.cropPixmap(pixmap, width)
        pixmap = PixmapUtils.squarePixmap(pixmap)
        pixmap = PixmapUtils.roundPixmap(pixmap, radius=12)
        return pixmap


if __name__ == "__main__":
    app = QApplication(argv)
    form = QWidget()
    form.setGeometry(QRect(276, 490, 1368, 100))
    ui = MusicPlayer(form)
    form.show()
    exit(app.exec_())
