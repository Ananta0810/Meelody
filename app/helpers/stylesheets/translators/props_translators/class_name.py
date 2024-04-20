from typing import Optional

from app.helpers.base import Strings, Lists


class ClassName:

    def __init__(self, state: str, key: str, value: str) -> None:
        self.state = state
        self.key = key
        self.value = value
        super().__init__()

    def __str__(self) -> str:
        return f"className(state: {self.state}, key: {self.key}, value: {self.value})"

    @staticmethod
    def of(name: str) -> Optional['ClassName']:
        if name is None:
            return None
        state, props = ClassName.partsOfCn(name)
        key, value = ClassName.propsDetail(props)

        return ClassName(state, key, value)

    @staticmethod
    def propsDetail(props):
        classDetail = props.split("-")
        if len(classDetail) == 0:
            return classDetail[0], None
        return classDetail[0], Strings.join(classDetail[1:], "-")

    @staticmethod
    def partsOfCn(name) -> (str, str):
        parts = name.split(":")
        totalParts = len(parts)
        if totalParts == 1:
            return None, parts[0]

        props = Lists.lastOf(parts)

        if totalParts == 2:
            return (None, props) if parts[0] == "dark" else (parts[0], props)
        return parts[1], props
