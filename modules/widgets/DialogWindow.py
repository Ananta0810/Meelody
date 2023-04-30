from modules.widgets.BaseDialogs import AlertDialog, ConfirmDialog, Dialog


class DialogWindow:
    def add_alert(self, dialog: AlertDialog) -> None:
        ...

    def add_confirm(self, dialog: ConfirmDialog) -> None:
        ...

    def add_dialog(self, dialog: Dialog) -> None:
        ...
