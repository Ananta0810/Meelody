from modules.widgets.BaseDialogs import Dialog
from modules.widgets.CustomDialogs import AlertDialog, ConfirmDialog
from modules.widgets.DialogWindow import DialogWindow


def alert(
    image: bytes,
    header: str,
    message: str,
    accept_text: str = "OK",
) -> None:
    dialog = AlertDialog()
    dialog.set_info(image, header, message, accept_text)
    dialog.show()

    def confirm(
        image: bytes,
        header: str,
        message: str,
        accept_text: str = "OK",
        cancel_text: str = "Cancel",
        on_accept: callable = None,
        on_cancel: callable = None
    ) -> None:
        dialog = ConfirmDialog()
        dialog.set_info(image, header, message, accept_text, cancel_text)
        dialog.on_accept(on_accept)
        dialog.on_cancel(on_cancel)
        dialog.show()


class Dialogs:
    __window: DialogWindow = None
    __instance: 'Dialogs' = None

    @staticmethod
    def get_instance() -> 'Dialogs':
        if Dialogs.__instance is None:
            Dialogs.__instance = Dialogs()
        return Dialogs.__instance

    def set_window(self, window: 'DialogWindow') -> None:
        self.__window = window

    @staticmethod
    def show_dialog(dialog: Dialog) -> None:
        Dialogs.get_instance().__window.add_dialog(dialog)
