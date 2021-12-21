        if len(folderDir) == 0:
            return
        self.ui.settings_panel_inner.changeCurrentFolder(folderDir)
        updateSettingsData("path", folderDir)
        self.loadPlaylistFromDirForPlayer(folderDir)
        self.musicPlayer.player.setCurrentSongIndex(0)
        self.musicPlayer.player.loadSongToPlay()
        self.musicPlayer.displayCurrentSongInfo()