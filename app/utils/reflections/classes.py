from typing import final


@final
class Classes:
    @staticmethod
    def typeNameOf(obj: object) -> str:
        return obj.__class__.__name__
