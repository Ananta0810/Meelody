from sys import argv, exit, path

from PyQt5.QtWidgets import QApplication, QWidget

path.append("./lib")
from threading import Thread
from time import perf_counter, sleep

from constants.ui.images import ApplicationImage as AppImage
from entities.song import Song
from modules.models.player import Player
from modules.models.timer import Timer
from utils.helpers.playlist_song_utils import getPlaylistFromDir
from views.player import UIPlayerMusic


class MusicPlayer:
    def __init__(self, form: QWidget):
        self.ui = UIPlayerMusic(form)
        self.ui.setFixedSize(1368, 100)
        self.ui.setupUi()

        self.currentThreadNumber = 0
        self.canRunTimeSlider = True
        self.defaultSongCoverAsPixmap = self.ui.getPixmapForSongCover(
            AppImage.defaultSongCover
        )
        self.timer = Timer()
        self.player = Player()

        playlist = getPlaylistFromDir("Library", withExtension=".mp3")
        self.player.loadPlaylist(playlist)
        self.player.loadSongToPlay()
        self.showCurrentSongInfo()
        self.connectSignals()

    def connectSignals(self):
        self.ui.previous_song_btn.clicked.connect(self.prevSong)
        self.ui.play_song_btn.clicked.connect(self.clickedPlayButton)
        self.ui.next_song_btn.clicked.connect(self.nextSong)
        self.ui.time_slider.sliderPressed.connect(self.pauseTimeSlider)
        self.ui.time_slider.sliderReleased.connect(self.unpauseTimeSlider)
        self.ui.shuffle_btn.clicked.connect(self.clickedShuffleSong)
        self.ui.love_btn.clicked.connect(self.loveSong)
        self.ui.volume_slider.valueChanged.connect(self.changeVolume)
        self.ui.timer_box.returnPressed.connect(self.setTimer)

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

        TIMES_THAT_UI_HAS_TO_UPDATE_FOR_SLIDER_WHILE_PLAYING: int = 100
        LONGEST_TIME_BREAK_FOR_A_UI_UPDATE_IN_SECONDS: float = 0.25

        interval: float = (
            self.player.getCurrentSong().length
            / TIMES_THAT_UI_HAS_TO_UPDATE_FOR_SLIDER_WHILE_PLAYING
        )
        if interval > LONGEST_TIME_BREAK_FOR_A_UI_UPDATE_IN_SECONDS:
            interval = LONGEST_TIME_BREAK_FOR_A_UI_UPDATE_IN_SECONDS

        timer.setInterval(interval)

        while threadNumber == self.currentThreadNumber and player.isPlaying():
            sleep(interval)
            self.__doWhilePlayingMusic(player, timer)
            if not player.isSongFinished():
                continue
            self.__doAfterSongFinished()
            break

    def __doWhilePlayingMusic(self, player: Player, timer: Timer):
        playingTime = player.getPlayingTime()
        self.ui.displayPlayingTime(playingTime)

        if self.canRunTimeSlider:
            self.ui.runTimeSlider(playingTime, player.getCurrentSong().length)
        if timer.isEnabled():
            self.__runTimer(timer)

    def __doAfterSongFinished(self):
        if self.ui.isLooping():
            self.rewind()
        else:
            self.nextSong()

    def __runTimer(self, timer: Timer):
        timer.count()
        if not timer.isActive():
            return
        timer.reset()
        self.pauseMusic()

    def loveSong(self):
        self.player.getCurrentSong().reverseLoveState()

    def rewind(self):
        self.player.stop()
        self.threadPlaySong()

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
        coverAsPixmap = self.defaultSongCoverAsPixmap
        song: Song = self.player.getCurrentSong()
        if song.cover is not None:
            coverAsPixmap = self.ui.getPixmapForSongCover(song.cover)

        self.ui.displaySongInfo(coverAsPixmap, song.title, song.artist)
        self.ui.displayPlayingTime(0)
        self.ui.displayTotalTime(song.length)


def main():
    start = perf_counter()
    app = QApplication(argv)
    form = QWidget()
    form.setGeometry(276, 490, 1368, 100)
    ui = MusicPlayer(form)
    form.show()
    end = perf_counter()
    print(end - start)
    exit(app.exec_())


if __name__ == "__main__":
    main()
