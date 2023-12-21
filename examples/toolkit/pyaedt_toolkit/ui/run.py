import os
import sys
import json
from PySide6.QtWidgets import QApplication

# Default properties
from ansys.aedt.toolkits.common.ui.properties import general_settings

# Load toolkit properties
with open(os.path.join(os.path.dirname(__file__), "properties.json")) as fh:
    _properties = json.load(fh)
for key, value in _properties.items():
    if hasattr(general_settings, key):
        setattr(general_settings, key, value)

# Import general common frontend modules
from ansys.aedt.toolkits.common.ui.logger_handler import logger
from ansys.aedt.toolkits.common.ui.main_window.main_window_layout import MainWindowLayout
from ansys.aedt.toolkits.common.ui.common_windows.main_window import MainWindow
from ansys.aedt.toolkits.common.ui.common_windows.home_menu import HomeMenu
from ansys.aedt.toolkits.common.ui.common_windows.settings_column import SettingsMenu

# Toolkit frontend API
from actions import Frontend

# Backend URL and port
url = general_settings.backend_url
port = general_settings.backend_port

os.environ["QT_API"] = "pyside6"
os.environ["QT_FONT_DPI"] = "96"

if general_settings.high_resolution:
    os.environ["QT_SCALE_FACTOR"] = "2"


class ApplicationWindow(Frontend):
    def __init__(self):
        self.thread = None

        Frontend.__init__(self)

        self.url = f"http://{url}:{port}"

        # General Settings

        # Create user interface object
        self.ui = MainWindowLayout(self)
        self.ui.setup_ui()

        # Setup main
        self.main_window = MainWindow(self)
        self.main_window.setup_gui()

        # Settings menu
        settings_menu = SettingsMenu(self.ui)
        settings_menu.setup()

        # Home menu
        home_menu = HomeMenu(self.ui)
        home_menu.setup()

        # Get default properties
        success = self.get_properties()
        if not success:
            logger.error("Error getting default properties from backend. User interface running without backend.")
            settings_menu.aedt_version.addItem("Backend OFF")
            settings_menu.aedt_session.addItem("Backend OFF")
        else:
            # Get AEDT installed versions
            installed_versions = self.installed_versions()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ApplicationWindow()
    window.show()
    sys.exit(app.exec())
