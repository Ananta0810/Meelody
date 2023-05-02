from modules.widgets.BaseDialogs import AlertDialog, ConfirmDialog, Dialog
from modules.widgets.DialogWindow import DialogWindow


class Dialogs:
    __window: DialogWindow = None
    __instance: 'Dialogs' = None

    @staticmethod
    def get_instance() -> 'Dialogs':
        if Dialogs.__instance is None:
            Dialogs.__instance = Dialogs()
        return Dialogs.__instance

    def __init__(self):
        self.__alert_dialog: AlertDialog = AlertDialog()
        self.__confirm_dialog: ConfirmDialog = ConfirmDialog()

    def set_window(self, window: 'DialogWindow') -> None:
        self.__window = window

    @staticmethod
    def alert(
              image: bytes,
              header: str,
              message: str,
              with_accept_text: str = "OK",
              ) -> None:
        Dialogs.get_instance().__alert_dialog.set_info(image, header, message, with_accept_text)
        Dialogs.get_instance().__window.add_alert(Dialogs.get_instance().__alert_dialog)

    @staticmethod
    def confirm(
                image: bytes,
                header: str,
                message: str,
                accept_text: str = "OK",
                cancel_text: str = "Cancel",
                on_accept: callable = None,
                on_cancel: callable = None
                ) -> None:
        Dialogs.get_instance().__confirm_dialog.set_info(image, header, message, accept_text, cancel_text)
        Dialogs.get_instance().__confirm_dialog.on_accept(on_accept)
        Dialogs.get_instance().__confirm_dialog.on_cancel(on_cancel)
        Dialogs.get_instance().__window.add_confirm(Dialogs.get_instance().__confirm_dialog)

    @staticmethod
    def show_dialog( dialog: Dialog) -> None:
        Dialogs.get_instance().__window.add_dialog(dialog)



