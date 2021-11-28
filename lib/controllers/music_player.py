from sys import argv, exit, path

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget

path.append("./lib")
from threading import Thread
from time import sleep

from constants.ui.images import ApplicationImage
from entities.song import Song
from modules.models.player import Player
from modules.models.playlist_songs import PlaylistSongs
from modules.models.timer import Timer
from utils.helpers.my_file import MyFile
from utils.ui.pixmap_utils import PixmapUtils
from views.player import UIPlayerMusic


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

        playlist = PlaylistSongs()
        files = MyFile.getFilesFrom("Library", withExtension="mp3")
        for file in files:
            song = Song(location=file, title=MyFile.getFileBasename(file))
            song.loadInfo()
            playlist.insert(song)

        self.timer = Timer()
        self.player = Player()
        self.player.loadPlaylist(playlist)
        self.player.loadSongToPlay()
        self.showCurrentSongInfo()
        self.connectSignals()

    def connectSignals(self):
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
            self.player.shuffle()
        else:
            self.player.unshuffle()

    def pauseTimeSlider(self):
        self.canRunTimeSlider = False

    def unpauseTimeSlider(self):
        self.canRunTimeSlider = True
        timeStart: float = (
            self.ui.time_slider.sliderPosition()
            / 100
            * self.player.getCurrentSong().length
        )
        self.player.stop()
        self.player.setTimeStart(timeStart)
        self.clickedPlayButton()

    def changeVolume(self):
        volume: int = self.ui.volume_slider.value()
        self.player.setVolume(volume)

    def clickedPlayButton(self):
        if not self.ui.play_song_btn.isChecked():
            self.pauseMusic()
            return
        self.player.loadSongToPlay()
        self.threadPlaySong()

    def pauseMusic(self):
        self.player.pause()
        self.ui.play_song_btn.setChecked(False)

    def threadPlaySong(self):
        thread: Thread = Thread(target=self.playMusic)
        self.currentThreadNumber += 1
        thread.start()

    def playMusic(self):
        self.ui.play_song_btn.setChecked(True)
        self.player.play()

        threadNumber: int = self.currentThreadNumber
        player = self.player
        timer = self.timer
        timer.setInterval(0.25)

        while threadNumber == self.currentThreadNumber and player.isPlaying():
            sleep(0.25)
            self.__doWhilePlayingMusic(player, timer)
            if player.isSongFinished():
                self.doAfterSongFinished()
                break

    def __doWhilePlayingMusic(self, player: Player, timer: Timer):
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
        self.player.getCurrentSong().reverseLoveState()

    def rewind(self):
        self.player.stop()
        self.clickedPlayButton()

    def nextSong(self):
        self.player.next()
        self.player.loadSongToPlay()
        self.showCurrentSongInfo()
        self.threadPlaySong()

    def prevSong(self):
        self.player.previous()
        self.player.loadSongToPlay()
        self.showCurrentSongInfo()
        self.threadPlaySong()

    def showCurrentSongInfo(self):
        song: Song = self.player.getCurrentSong()

        coverAsPixmap = self.defaultSongCoverAsPixmap
        if song.cover is not None:
            coverAsPixmap = self.getDisplayCoverFromBytes(
                song.cover,
                self.ui.song_cover.width(),
            )

        self.ui.song_cover.setPixmap(coverAsPixmap)
        self.ui.song_title.setText(song.title)
        self.ui.song_artist.setText(song.artist)
        self.ui.displayPlayingTime(0)
        self.ui.displayTotalTime(song.length)

    def getDisplayCoverFromBytes(
        self, byteImage: bytes, width: int, radius: int = 12
    ) -> QPixmap:
        pixmap = PixmapUtils.getPixmapFromBytes(byteImage)
        pixmap = PixmapUtils.cropPixmap(pixmap, width)
        pixmap = PixmapUtils.squarePixmap(pixmap)
        pixmap = PixmapUtils.roundPixmap(pixmap, radius=radius)
        return pixmap


if __name__ == "__main__":
    app = QApplication(argv)
    form = QWidget()
    form.setGeometry(QRect(276, 490, 1368, 100))
    ui = MusicPlayer(form)
    form.show()
    exit(app.exec_())
