from enum import Enum


class ThemeMode(Enum):
    SYSTEM = "system"
    LIGHT = "light"
    DARK = "dark"

    def __str__(self) -> str:
        return f'{self.name}'

    @staticmethod
    def of(value: str) -> 'ThemeMode':
        if value.upper() == 'LIGHT':
            return ThemeMode.LIGHT
        if value.upper() == 'DARK':
            return ThemeMode.DARK

        return ThemeMode.SYSTEM

    @staticmethod
    def systemTheme() -> bool:
        return True
