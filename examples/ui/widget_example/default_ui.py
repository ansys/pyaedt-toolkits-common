from random import randint
import sys

from PySide6 import QtWidgets

from ansys.aedt.toolkits.common.ui.main_window.main_window_layout import MainWindowLayout
from PySide6.QtWidgets import QApplication


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = MainWindowLayout(self)
        self.ui.setup()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ApplicationWindow()
    window.show()
    sys.exit(app.exec())
