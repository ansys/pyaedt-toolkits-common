from random import randint
import sys

from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QApplication

from ansys.aedt.toolkits.common.ui.main_window.main_window_layout import MainWindowLayout

# Common windows
from ansys.aedt.toolkits.common.ui.main_window.main_window_layout import MainWindowLayout
from ansys.aedt.toolkits.common.ui.common_windows.home_menu import HomeMenu
from ansys.aedt.toolkits.common.ui.common_windows.settings_column import SettingsMenu


class ApplicationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = MainWindowLayout(self)
        self.ui.setup()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ApplicationWindow()
    window.show()
    sys.exit(app.exec())
