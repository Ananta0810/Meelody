class Languages:
    @staticmethod
    def getSupportiveLanguages() -> dict[str, str]:
        return {
            "eng": "lib/configs/langs/eng.json",
            "vie": "lib/configs/langs/vie.json",
        }


class ImportType:
    IMAGE: str = "JPEG, PNG (*.JPEG *.jpeg *.JPG *.jpg *.JPE *.jpe)"
