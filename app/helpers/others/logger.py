from typing import final


@final
class Logger:
    @staticmethod
    def error(message: any) -> None:
        print('\033[31m' + 'Error::' + str(message) + '\033[0m')
