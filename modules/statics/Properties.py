class Languages:
    @staticmethod
    def getSupportiveLanguages() -> dict[str, str]:
        return {
            "eng": "lib/configs/langs/eng.json",
            "vie": "lib/configs/langs/vie.json",
        }

class ImportType:
    IMAGE: str = "JPEG, PNG, WEBP (*.JPEG *.jpeg *.JPG *.jpg *.JPE *.jpe *.webp)"