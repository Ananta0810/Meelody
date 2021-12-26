from constants.application import supportedLanguages
from utils.data.config_utils import (getLanguagePackage, retrievePlayerData,
                                     retrieveSettingsData, updateSettingsData)


class SettingsController:
    def __init__(self, view) -> None:
        self.view = view

    def handleChangedLanguage(self, index: int) -> None:
        supportedLanguagesAsList = [key for key in supportedLanguages.keys()]
        language = supportedLanguagesAsList[index]
        languagePackage = getLanguagePackage(language)
        self.view.translate(languagePackage)
        updateSettingsData("language", language)

    def handleChangedDarkMode(self) -> None:
        self.view.switchDarkMode(not self.view.isDarkMode)
        updateSettingsData("darkMode", self.view.isDarkMode)

    def handleChangedFolder(self, folderDir: str) -> None:
        if len(folderDir) == 0:
            return
        self.view.settings_panel.changeCurrentFolder(folderDir)
        updateSettingsData("path", folderDir)
        # self.loadPlaylistFromDirForPlayer(folderDir)
        # self.musicPlayer.player.setCurrentSongIndex(0)
        # self.musicPlayer.player.loadSongToPlay()
        # self.musicPlayer.displayCurrentSongInfo()
