from modules.helpers.types.Metas import SingletonMeta
from modules.widgets.BaseDialogs import AlertDialog, ConfirmDialog, Dialog
from modules.widgets.DialogWindow import DialogWindow


class Dialogs(metaclass=SingletonMeta):
    __window: DialogWindow = None

    def set_window(self, window: 'DialogWindow') -> None:
        self.__window = window

    def alert(self,
              with_image: bytes,
              with_header: str,
              with_message: str,
              with_accept_text: str = "OK",
              ) -> None:
        dialog = AlertDialog()
        dialog.set_info(with_image, with_header, with_message, with_accept_text)
        self.__window.add_alert(dialog)

    def confirm(self,
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
        self.__window.add_confirm(dialog)

    def show_dialog(self, dialog: Dialog) -> None:
        self.__window.add_dialog(dialog)



