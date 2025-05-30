import sys

from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QApplication

from examples.ui.default_ui_example.models import properties

# Windows

# Common windows

from ansys.aedt.toolkits.common.ui.main_window.main_window_layout import MainWindowLayout

properties.version = "dummy_version"


class ApplicationWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.properties = properties

        self.ui = MainWindowLayout(self)
        self.ui.setup()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ApplicationWindow()
    window.show()
    sys.exit(app.exec())
