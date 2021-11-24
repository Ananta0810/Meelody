from sys import path

from PyQt5 import QtCore, QtGui, QtWidgets

from buttons.action_button_factory import ActionButtonFactory
from buttons.icon_button_factory import IconButtonFactory

path.append(".")
from ui.base.colors import Colors
from ui.base.icons import Icons
from ui.base.text import Text
from ui.utils.color_utils import ColorUtils
from ui.utils.icon_utils import IconUtils


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(960, 540)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.actionButtonList = QtWidgets.QWidget(self.centralwidget)
        self.actionButtonList.setGeometry(QtCore.QRect(20, 100, 900, 100))
        self.actionButtonList.setObjectName("actionButtonList")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.actionButtonList)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("actionButtonList")

        font = Text.FONT_PRIMARY_SMALL
        font.setBold(True)
        buttonFactory = ActionButtonFactory()

        self.primaryActionButton = buttonFactory.createButton(
            type="primary",
            name="PrimaryButton",
            text="Primary",
            font=font,
            cursor=QtGui.QCursor(QtCore.Qt.PointingHandCursor),
            parent=self.actionButtonList,
        )
        self.horizontalLayout.addWidget(self.primaryActionButton)

        self.secondaryActionButton = buttonFactory.createButton(
            type="secondary",
            name="SecondaryButton",
            text="Secondary",
            font=font,
            cursor=QtGui.QCursor(QtCore.Qt.PointingHandCursor),
            parent=self.actionButtonList,
        )
        self.horizontalLayout.addWidget(self.secondaryActionButton)

        self.disabledActionButton = buttonFactory.createButton(
            type="disabled",
            name="DisabledButton",
            text="Disabled",
            font=font,
            parent=self.actionButtonList,
        )
        self.horizontalLayout.addWidget(self.disabledActionButton)

        self.successActionButton = buttonFactory.createButton(
            type="success",
            name="SuccessButton",
            text="Success",
            font=font,
            cursor=QtGui.QCursor(QtCore.Qt.PointingHandCursor),
            parent=self.actionButtonList,
        )
        self.horizontalLayout.addWidget(self.successActionButton)

        self.dangerActionButton = buttonFactory.createButton(
            type="danger",
            name="DangersButton",
            text="Dangers",
            font=font,
            cursor=QtGui.QCursor(QtCore.Qt.PointingHandCursor),
            parent=self.actionButtonList,
        )
        self.horizontalLayout.addWidget(self.dangerActionButton)

        self.warningActionButton = buttonFactory.createButton(
            type="warning",
            name="WarningButton",
            text="Warning",
            font=font,
            cursor=QtGui.QCursor(QtCore.Qt.PointingHandCursor),
            parent=self.actionButtonList,
        )
        self.horizontalLayout.addWidget(self.warningActionButton)

        self.outlinedPrimary = buttonFactory.createButton(
            type="outlined-primary",
            name="Outline",
            text="Outline",
            font=font,
            cursor=QtGui.QCursor(QtCore.Qt.PointingHandCursor),
            parent=self.actionButtonList,
        )
        self.horizontalLayout.addWidget(self.outlinedPrimary)

        self.iconButtonList = QtWidgets.QWidget(self.centralwidget)
        self.iconButtonList.setGeometry(QtCore.QRect(20, 200, 900, 100))
        self.iconButtonList.setObjectName("iconButtonList")
        self.iconButtonsLayout = QtWidgets.QHBoxLayout(self.iconButtonList)
        self.iconButtonsLayout.setContentsMargins(0, 0, 0, 0)
        self.iconButtonsLayout.setObjectName("iconButtonList")

        icons = Icons()
        iconButtonFactory = IconButtonFactory()

        self.iconButtonUnstyled = iconButtonFactory.createButton(
            type="unstyled",
            name="iconButtonUnstyled",
            iconSize=icons.SIZES.MEDIUM,
            icon=IconUtils.changeColor(
                icons.ADD, ColorUtils.getQColorFromColor(Colors.BLACK)
            ),
            cursor=QtGui.QCursor(QtCore.Qt.PointingHandCursor),
            parent=self.iconButtonList,
        )
        self.iconButtonsLayout.addWidget(self.iconButtonUnstyled)

        self.iconButtonDefault = iconButtonFactory.createButton(
            type="default",
            name="iconButtonDefault",
            iconSize=icons.SIZES.MEDIUM,
            icon=IconUtils.changeColor(
                icons.ADD, ColorUtils.getQColorFromColor(Colors.BLACK)
            ),
            cursor=QtGui.QCursor(QtCore.Qt.PointingHandCursor),
            parent=self.iconButtonList,
        )
        self.iconButtonsLayout.addWidget(self.iconButtonDefault)

        self.iconButtonPrimary = iconButtonFactory.createButton(
            type="primary",
            name="iconButtonPrimary",
            iconSize=icons.SIZES.MEDIUM,
            icon=IconUtils.changeColor(
                icons.ADD, ColorUtils.getQColorFromColor(Colors.PRIMARY)
            ),
            cursor=QtGui.QCursor(QtCore.Qt.PointingHandCursor),
            parent=self.iconButtonList,
        )
        self.iconButtonsLayout.addWidget(self.iconButtonPrimary)

        self.iconButtonSuccess = iconButtonFactory.createButton(
            type="success",
            name="iconButtonSuccess",
            iconSize=icons.SIZES.MEDIUM,
            icon=IconUtils.changeColor(
                icons.ADD, ColorUtils.getQColorFromColor(Colors.SUCCESS)
            ),
            cursor=QtGui.QCursor(QtCore.Qt.PointingHandCursor),
            parent=self.iconButtonList,
        )
        self.iconButtonsLayout.addWidget(self.iconButtonSuccess)

        self.iconButtonDanger = iconButtonFactory.createButton(
            type="danger",
            name="iconButtonDanger",
            iconSize=icons.SIZES.MEDIUM,
            icon=IconUtils.changeColor(
                icons.ADD, ColorUtils.getQColorFromColor(Colors.DANGER)
            ),
            cursor=QtGui.QCursor(QtCore.Qt.PointingHandCursor),
            parent=self.iconButtonList,
        )
        self.iconButtonsLayout.addWidget(self.iconButtonDanger)

        self.iconButtonWarning = iconButtonFactory.createButton(
            type="warning",
            name="iconButtonWarning",
            iconSize=icons.SIZES.MEDIUM,
            icon=IconUtils.changeColor(
                icons.ADD, ColorUtils.getQColorFromColor(Colors.WARNING)
            ),
            cursor=QtGui.QCursor(QtCore.Qt.PointingHandCursor),
            parent=self.iconButtonList,
        )
        self.iconButtonsLayout.addWidget(self.iconButtonWarning)

        self.iconButtonDisabled = iconButtonFactory.createButton(
            type="disabled",
            name="iconButtonDisabled",
            iconSize=icons.SIZES.MEDIUM,
            icon=IconUtils.changeColor(
                icons.ADD,
                ColorUtils.getQColorFromColor(Colors.DISABLED),
            ),
            parent=self.iconButtonList,
        )
        self.iconButtonsLayout.addWidget(self.iconButtonDisabled)

        self.iconButtonHiddenPrimary = iconButtonFactory.createButton(
            type="hidden-primary",
            name="iconButtonHiddenPrimary",
            iconSize=icons.SIZES.MEDIUM,
            icon=IconUtils.changeColor(
                icons.ADD, ColorUtils.getQColorFromColor(Colors.PRIMARY)
            ),
            cursor=QtGui.QCursor(QtCore.Qt.PointingHandCursor),
            parent=self.iconButtonList,
        )
        self.iconButtonsLayout.addWidget(self.iconButtonHiddenPrimary)

        self.iconButtonHiddenSuccess = iconButtonFactory.createButton(
            type="hidden-success",
            name="iconButtonHiddenSuccess",
            iconSize=icons.SIZES.MEDIUM,
            icon=IconUtils.changeColor(
                icons.ADD, ColorUtils.getQColorFromColor(Colors.SUCCESS)
            ),
            cursor=QtGui.QCursor(QtCore.Qt.PointingHandCursor),
            parent=self.iconButtonList,
        )
        self.iconButtonsLayout.addWidget(self.iconButtonHiddenSuccess)

        self.iconButtonHiddentDanger = iconButtonFactory.createButton(
            type="hidden-danger",
            name="iconButtonHiddentDanger",
            iconSize=icons.SIZES.MEDIUM,
            icon=IconUtils.changeColor(
                icons.ADD, ColorUtils.getQColorFromColor(Colors.DANGER)
            ),
            cursor=QtGui.QCursor(QtCore.Qt.PointingHandCursor),
            parent=self.iconButtonList,
        )
        self.iconButtonsLayout.addWidget(self.iconButtonHiddentDanger)

        self.iconButtonHiddenWarning = iconButtonFactory.createButton(
            type="hidden-warning",
            name="iconButtonHiddenWarning",
            iconSize=icons.SIZES.MEDIUM,
            icon=IconUtils.changeColor(
                icons.ADD, ColorUtils.getQColorFromColor(Colors.WARNING)
            ),
            cursor=QtGui.QCursor(QtCore.Qt.PointingHandCursor),
            parent=self.iconButtonList,
        )
        self.iconButtonsLayout.addWidget(self.iconButtonHiddenWarning)

        self.iconButtonHiddenDisabled = iconButtonFactory.createButton(
            type="hidden-disabled",
            name="iconButtonHiddenDisabled",
            iconSize=icons.SIZES.MEDIUM,
            icon=IconUtils.changeColor(
                icons.ADD,
                ColorUtils.getQColorFromColor(Colors.DISABLED),
            ),
            parent=self.iconButtonList,
        )
        self.iconButtonsLayout.addWidget(self.iconButtonHiddenDisabled)

        self.checkableButton = iconButtonFactory.createButton(
            type="checkable-primary-danger",
            name="checkableButton",
            iconSize=icons.SIZES.MEDIUM,
            icon=IconUtils.changeColor(
                icons.LOVE, ColorUtils.getQColorFromColor(Colors.PRIMARY)
            ),
            checkedIcon=IconUtils.changeColor(
                icons.UNLOVE, ColorUtils.getQColorFromColor(Colors.DANGER)
            ),
            cursor=QtGui.QCursor(QtCore.Qt.PointingHandCursor),
            parent=self.iconButtonList,
        )

        self.iconButtonsLayout.addWidget(self.checkableButton)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
