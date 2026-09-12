import os
import sys

from PySide6.QtWidgets import QApplication

# Toolkit frontend API
from actions import Frontend

# Default properties
from models import properties

# Toolkit windows
from windows.create_geometry.geometry_menu import GeometryMenu

from ansys.aedt.toolkits.common.ui.common_windows.home_menu import HomeMenu
from ansys.aedt.toolkits.common.ui.common_windows.main_window import MainWindow
from ansys.aedt.toolkits.common.ui.common_windows.settings_column import SettingsMenu

# Import general common frontend modules
from ansys.aedt.toolkits.common.ui.logger_handler import logger
from ansys.aedt.toolkits.common.ui.main_window.main_window_layout import MainWindowLayout

# Backend URL and port
url = properties.backend_url
port = properties.backend_port

os.environ["QT_API"] = "pyside6"
os.environ["QT_FONT_DPI"] = "96"

if properties.high_resolution:
    os.environ["QT_SCALE_FACTOR"] = "2"


class ApplicationWindow(Frontend):
    def __init__(self):
        self.thread = None
        self.properties = properties

        Frontend.__init__(self)

        # General Settings

        # Create user interface object
        self.ui = MainWindowLayout(self)
        self.ui.setup_ui()

        # Setup main
        self.main_window = MainWindow(self)
        self.main_window.setup_gui()

        # Settings menu
        self.settings_menu = SettingsMenu(self)
        self.settings_menu.setup()

        # Check backend connection
        success = self.check_connection()

        # Populate settings column
        if not success:
            msg = "Error getting properties from backend. User interface running without backend"
            self.ui.logger.log(msg)
            logger.error(msg)
            self.settings_menu.signal_flag = False
            self.settings_menu.aedt_version.addItem("Backend OFF")
            self.settings_menu.aedt_session.addItem("Backend OFF")
        else:
            # Get default properties
            be_properties = self.get_properties()
            # Get AEDT installed versions
            installed_versions = self.installed_versions()
            self.settings_menu.signal_flag = False
            if installed_versions:
                self.settings_menu.connect_aedt.setEnabled(True)
                for ver in installed_versions:
                    self.settings_menu.aedt_version.addItem(ver)
            else:
                self.settings_menu.aedt_version.addItem("AEDT not installed")
            self.settings_menu.signal_flag = True
            if be_properties.get("aedt_version") in installed_versions:
                self.settings_menu.aedt_version.setCurrentText(be_properties.get("aedt_version"))

        # Toolkit specific wizard starts here

        # Home menu
        self.home_menu = HomeMenu(self)
        self.home_menu.setup()

        # Modeler menu
        self.geometry_menu = GeometryMenu(self)
        self.geometry_menu.setup()
        self.ui.left_menu.clicked.connect(self.geometry_menu_clicked)

        self.ui.set_page(self.ui.load_pages.home_page)

    def geometry_menu_clicked(self):
        selected_menu = self.main_window.get_selected_menu()
        if selected_menu.objectName() == "geometry_menu":
            self.ui.set_page(self.geometry_menu.geometry_menu_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ApplicationWindow()
    window.show()
    sys.exit(app.exec())
