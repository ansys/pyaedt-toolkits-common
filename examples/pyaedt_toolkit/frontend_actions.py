import os
import sys
import json
from PySide6.QtWidgets import QApplication

# Import general common frontend modules
from ansys.aedt.toolkits.common.ui.logger_handler import logger
# Default properties
from ansys.aedt.toolkits.common.ui.properties import general_settings
# Load toolkit properties
with open(os.path.join(os.path.dirname(__file__), "properties.json")) as fh:
    _properties = json.load(fh)
for key, value in _properties.items():
    if hasattr(general_settings, key):
        setattr(general_settings, key, value)

from ansys.aedt.toolkits.common.ui.main_gui.frontend_ui import MainWindow
from ansys.aedt.toolkits.common.ui.toolkit_windows.setup_main_window import SetupMainWindow
from ansys.aedt.toolkits.common.ui.toolkit_windows.setup_home_column import SetupHomeMenu
from ansys.aedt.toolkits.common.ui.toolkit_windows.setup_settings_column import SetupSettingsMenu

# Toolkit frontend API
from frontend_api import ToolkitFrontend

# Backend URL and port
url = general_settings.backend_url
port = general_settings.backend_port

os.environ["QT_API"] = "pyside6"

if general_settings.high_resolution:
    os.environ["QT_FONT_DPI"] = "96"
    os.environ["QT_SCALE_FACTOR"] = "2"


class ApplicationWindow(ToolkitFrontend):
    def __init__(self):
        self.thread = None

        ToolkitFrontend.__init__(self)

        self.url = f"http://{url}:{port}"

        # General Settings

        # Create user interface object
        self.ui = MainWindow(self)
        self.ui.setup_ui()

        # Setup main
        self.main_window = SetupMainWindow(self)
        self.main_window.setup_gui()

        # Settings
        settings_menu = SetupSettingsMenu(self.ui)
        settings_menu.setup()

        # Home
        home_menu = SetupHomeMenu(self.ui)
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
