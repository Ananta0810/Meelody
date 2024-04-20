from typing import Optional

from app.helpers.base import Strings


class ClassName:

    def __init__(self, theme: str, state: str, key: str, value: str) -> None:
        self.theme = theme
        self.state = state
        self.key = key
        self.value = value
        super().__init__()

    def __str__(self) -> str:
        return f"className(theme: {self.theme}, state: {self.state}, key: {self.key}, value: {self.value})"

    @staticmethod
    def of(name: str) -> Optional['ClassName']:
        if name is None:
            return None
        theme, state, props = ClassName.partsOfCn(name)
        key, value = ClassName.propsDetail(props)

        return ClassName(theme or "light", state, key, value)

    @staticmethod
    def propsDetail(props):
        classDetail = props.split("-")
        if len(classDetail) == 0:
            return classDetail[0], None
        return classDetail[0], Strings.join(classDetail[1:], "-")

    @staticmethod
    def partsOfCn(name):
        parts = name.split(":")
        totalParts = len(parts)
        if totalParts == 1:
            return None, None, parts[0]
        if totalParts == 2:
            return None, parts[0], parts[1]
        return parts[0], parts[1], parts[2]
