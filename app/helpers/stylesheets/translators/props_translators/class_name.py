from typing import Optional

from app.helpers.base import Strings, Lists


class ClassName:

    def __init__(self, element: str, state: str, key: str, value: str) -> None:
        self.element = element
        self.state = state
        self.key = key
        self.value = value
        super().__init__()

    def __str__(self) -> str:
        return f"className(element: {self.element}, state: {self.state}, key: {self.key}, value: {self.value})"

    @staticmethod
    def of(name: str) -> Optional['ClassName']:
        if name is None:
            return None

        element, others = ClassName.__separateElementAndOthers(name.replace("dark:", ""))
        state, props = ClassName.__separateStateAndProps(others)
        key, value = ClassName.__separateProps(props)

        return ClassName(element, state, key, value)

    @staticmethod
    def __separateElementAndOthers(name) -> (str, str):
        parts = name.split("/", maxsplit=1)
        totalParts = len(parts)
        if totalParts == 1:
            return None, parts[0]

        return parts[0], parts[1]

    @staticmethod
    def __separateStateAndProps(name) -> (str, str):
        parts = name.split(":")
        totalParts = len(parts)
        if totalParts == 1:
            return None, parts[0]

        props = Lists.lastOf(parts)

        if totalParts == 2:
            return parts[0], props
        return parts[1], props

    @staticmethod
    def __separateProps(props) -> (str, str):
        classDetail = props.split("-")
        if len(classDetail) == 0:
            return classDetail[0], None
        return classDetail[0], Strings.join("-", classDetail[1:])
