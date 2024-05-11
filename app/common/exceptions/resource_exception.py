from enum import Enum


class ResourceException(Exception):
    class __Reason(Enum):
        EXISTED = 'not found',
        NOT_FOUND = 'not found',
        BEING_USED = 'being used',
        BROKEN = 'broken',

    def __init__(self, reason: __Reason) -> None:
        super().__init__()
        self.__reason = reason

    def isNotFound(self) -> bool:
        return self.__reason == ResourceException.__Reason.NOT_FOUND

    def isBeingUsed(self) -> bool:
        return self.__reason == ResourceException.__Reason.BEING_USED

    def isExisted(self) -> bool:
        return self.__reason == ResourceException.__Reason.EXISTED

    def isBroken(self) -> bool:
        return self.__reason == ResourceException.__Reason.BROKEN

    @staticmethod
    def notFound() -> 'ResourceException':
        return ResourceException(ResourceException.__Reason.NOT_FOUND)

    @staticmethod
    def unChangeable() -> 'ResourceException':
        return ResourceException(ResourceException.__Reason.BEING_USED)

    @staticmethod
    def fileExisted() -> 'ResourceException':
        return ResourceException(ResourceException.__Reason.EXISTED)

    @staticmethod
    def brokenFile() -> 'ResourceException':
        return ResourceException(ResourceException.__Reason.BROKEN)
