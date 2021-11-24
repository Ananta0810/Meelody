from PyQt5.QtCore import QRect


class UiIcons(object):
    def __init__(self):
        self._song_cover_rect = QRect(20, 18, 64, 64)
        self._song_title_rect = QRect(110, 32, 160, 30)
        self._song_artist_rect = QRect(300, 32, 140, 30)
        self._song_length_rect = QRect(480, 32, 60, 30)
        self._song_play_rect = QRect(651, 29, 40, 40)
        self._song_add_rect = QRect(651, 29, 40, 40)
        self._song_more_rect = QRect(560, 32, 32, 32)
        self._song_more_widget_rect = QRect(544, 10, 160, 80)
        self._song_love_rect = QRect(600, 32, 32, 32)
        self._song_delete_rect = QRect(112, 26, 32, 32)
        self._song_hide_widget_rect = QRect(690, 4, 24, 24)
