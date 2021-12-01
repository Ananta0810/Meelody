from sys import argv, exit, path

from PyQt5.QtWidgets import QApplication, QWidget

path.append("./lib")
from threading import Thread
from time import perf_counter, sleep

from modules.entities.song import Song
from modules.models.player import Player
from utils.helpers.playlist_song_utils import getPlaylistFromDir
from views.ui_player_music import UIPlayerMusic


class MusicPlayer:
    def __init__(self, form: QWidget):
        self.ui = UIPlayerMusic(form)
        self.ui.setSizePolicy(1368, 100)
        self.ui.setupUi()

        self.currentThreadNumber = 0
        self.canRunTimeSlider = True
        self.player = Player()

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
        timeElapsed: int = self.ui.getTimerValue() * 60
        self.player.timer.setTime(timeElapsed)
        self.ui.closeTimerBox()

    def clickedShuffleSong(self):
        if self.ui.isShuffling():
            self.player.shuffle()
        else:
            self.player.unshuffle()

    def pauseTimeSlider(self):
        self.canRunTimeSlider = False

    def unpauseTimeSlider(self):
        self.canRunTimeSlider = True
        if not self.player.hasSong():
            return
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
        if self.player.getCurrentSong() is None:
            return
        if not self.ui.isPlaying():
            self.pauseMusic()
            return
        self.player.loadSongToPlay()
        self.threadPlaySong()

    def threadPlaySong(self):
        thread: Thread = Thread(target=self.playMusic)
        self.currentThreadNumber += 1
        thread.start()

    def playMusic(self):
        self.ui.play_song_btn.setChecked(True)
        player = self.player
        player.play()

        threadNumber: int = self.currentThreadNumber
        TIMES_THAT_UI_HAS_TO_UPDATE_FOR_SLIDER_WHILE_PLAYING: int = 100
        LONGEST_TIME_BREAK_FOR_A_UI_UPDATE_IN_SECONDS: float = 0.25

        interval: float = (
            player.getCurrentSong().length
            / TIMES_THAT_UI_HAS_TO_UPDATE_FOR_SLIDER_WHILE_PLAYING
        )
        if interval > LONGEST_TIME_BREAK_FOR_A_UI_UPDATE_IN_SECONDS:
            interval = LONGEST_TIME_BREAK_FOR_A_UI_UPDATE_IN_SECONDS
        player.timer.setInterval(interval)

        while threadNumber == self.currentThreadNumber and player.isPlaying():
            self.__doWhilePlayingMusic(player)
            sleep(interval)

        playingThisSong: bool = threadNumber == self.currentThreadNumber
        songIsFinished: bool = self.ui.isPlaying() and playingThisSong

        if songIsFinished:
            self.__doAfterSongFinished()

    def __doWhilePlayingMusic(self, player: Player):
        playingTime = player.getPlayingTime()
        self.ui.displayPlayingTime(playingTime)

        if self.canRunTimeSlider:
            self.ui.runTimeSlider(playingTime, player.getCurrentSong().length)
        if player.timer.isEnabled():
            self.__runTimer()

    def __doAfterSongFinished(self):
        self.ui.play_song_btn.setChecked(False)
        if self.ui.isLooping():
            self.player.resetTime()
            self.threadPlaySong()
        else:
            self.nextSong()

    def __runTimer(self):
        timer = self.player.timer
        timer.count()
        if not timer.isActive():
            return
        timer.reset()
        self.pauseMusic()

    def loveSong(self):
        if not self.player.hasSong():
            return
        self.player.getCurrentSong().reverseLoveState()

    def pauseMusic(self):
        self.player.pause()
        self.ui.play_song_btn.setChecked(False)

    def rewind(self):
        self.player.stop()
        self.threadPlaySong()

    def nextSong(self):
        if not self.player.hasSong():
            return
        self.player.next()
        self.player.loadSongToPlay()
        self.displayCurrentSongInfo()
        self.threadPlaySong()

    def prevSong(self):
        if not self.player.hasSong():
            return
        self.player.previous()
        self.player.loadSongToPlay()
        self.displayCurrentSongInfo()
        self.threadPlaySong()

    def displayCurrentSongInfo(self):
        song: Song = self.player.getCurrentSong()
        if song is None:
            return
        self.ui.displaySongInfo(song.cover, song.title, song.artist)
        self.ui.displayPlayingTime(0)
        self.ui.displayTotalTime(song.length)


def main():
    start = perf_counter()
    app = QApplication(argv)
    form = QWidget()
    form.setGeometry(276, 490, 1368, 100)
    appTheme = MusicPlayer(form)
    playlist = getPlaylistFromDir("Library", withExtension=".mp3")
    appTheme.player.loadPlaylist(playlist)
    appTheme.player.loadSongToPlay()
    appTheme.displayCurrentSongInfo()
    appTheme.ui.setFixedSize(1368, 100)
    form.show()
    end = perf_counter()
    print(f"Time to start application: {end - start}")
    exit(app.exec_())


if __name__ == "__main__":
    main()
