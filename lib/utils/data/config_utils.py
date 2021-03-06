import json

from constants.application import supportedLanguages


def getJsonData(jsonFile) -> dict:
    # Opening JSON file
    f = open(jsonFile, encoding="utf-8")

    # returns JSON object as a dictionary
    data = json.load(f)

    # Closing file
    f.close()
    return data


def updateJsonData(jsonFile, property, value) -> None:
    with open(jsonFile, "r+") as jsonFile:
        data = json.load(jsonFile)

        # The change
        data[property] = value

        jsonFile.seek(0)
        json.dump(data, jsonFile, indent=4)
        jsonFile.truncate()


def retrieveSettingsData() -> dict:
    return getJsonData("lib/configs/settings.json")


def updateSettingsData(property, value) -> None:
    updateJsonData("lib/configs/settings.json", property, value)


def retrievePlayerData() -> dict:
    return getJsonData("lib/configs/music_player.json")


def updatePlayerData(property, value) -> None:
    updateJsonData("lib/configs/music_player.json", property, value)


def getLanguagePackageFromConfig() -> dict:
    data = getJsonData("lib/configs/settings.json")
    currentLanguage = data.get("language")
    currentLanguage = (
        currentLanguage if currentLanguage in supportedLanguages else "eng"
    )
    return getJsonData(supportedLanguages.get(currentLanguage))


def getLanguagePackage(language: str = "eng"):
    if language not in supportedLanguages:
        raise ValueError("Language is not supported")
    return getJsonData(supportedLanguages.get(language))
