import os
import sys

# PySide6 Widgets
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QApplication

# Toolkit frontend API
from actions import Frontend

# Default user interface properties
from models import properties

# Windows

# New windows
from windows.create_geometry.geometry_menu import GeometryMenu
from windows.plot_design.plot_design_menu import PlotDesignMenu

# Common windows
from ansys.aedt.toolkits.common.ui.main_window.main_window_layout import MainWindowLayout
from ansys.aedt.toolkits.common.ui.common_windows.home_menu import HomeMenu
from ansys.aedt.toolkits.common.ui.common_windows.settings_column import SettingsMenu

# Import general common frontend modules
from ansys.aedt.toolkits.common.ui.logger_handler import logger

# Backend URL and port
url = properties.backend_url
port = properties.backend_port

os.environ["QT_API"] = "pyside6"
os.environ["QT_FONT_DPI"] = "96"

if properties.high_resolution:
    os.environ["QT_SCALE_FACTOR"] = "2"


class ApplicationWindow(QMainWindow, Frontend):
    def __init__(self):
        super().__init__()

        self.thread = None
        self.properties = properties

        # General Settings

        # Create main window layout
        self.ui = MainWindowLayout(self)
        self.ui.setup()

        # Settings menu
        self.settings_menu = SettingsMenu(self)
        self.settings_menu.setup()

        # Check backend connection
        success = self.check_connection()

        # Populate settings column
        if not success:
            msg = "Error getting properties from backend. User interface running without backend"
            self.ui.update_logger(msg)
            logger.error(msg)
            self.settings_menu.signal_flag = False
            self.settings_menu.aedt_version.addItem("Backend OFF")
            self.settings_menu.aedt_session.addItem("Backend OFF")
        else:
            # Get default properties
            be_properties = self.get_properties()
            # Get AEDT installed versions
            installed_versions = self.installed_versions()
            # self.settings_menu.signal_flag = False
            self.settings_menu.aedt_session.clear()
            self.settings_menu.aedt_session.addItem("New Session")
            if installed_versions:
                self.settings_menu.connect_aedt.setEnabled(True)
                for ver in installed_versions:
                    self.settings_menu.aedt_version.addItem(ver)
            else:
                self.settings_menu.aedt_version.addItem("AEDT not installed")
            # self.settings_menu.signal_flag = True
            if be_properties.get("aedt_version") in installed_versions:
                self.settings_menu.aedt_version.setCurrentText(be_properties.get("aedt_version"))

        # Custom toolkit setup starts here

        # Home menu
        self.home_menu = HomeMenu(self)
        self.home_menu.setup()

        # Modeler menu
        self.geometry_menu = GeometryMenu(self)
        self.geometry_menu.setup()
        self.ui.left_menu.clicked.connect(self.geometry_menu_clicked)

        # Plot design menu
        self.plot_design_menu = PlotDesignMenu(self)
        self.plot_design_menu.setup()
        self.ui.left_menu.clicked.connect(self.plot_design_menu_clicked)

        # Home page as first page
        self.ui.set_page(self.ui.load_pages.home_page)

    def geometry_menu_clicked(self):
        selected_menu = self.ui.get_selected_menu()
        menu_name = selected_menu.objectName()

        if menu_name == "geometry_menu":
            selected_menu.set_active(True)
            self.ui.set_page(self.geometry_menu.geometry_menu_widget)

            is_left_visible = self.ui.is_left_column_visible()

            self.ui.set_left_column_menu(
                menu=self.geometry_menu.geometry_column_widget,
                title="Primitives Builder",
                icon_path=self.ui.images_load.icon_path("icon_plot_3d.svg"),
            )

            if not is_left_visible:
                self.ui.toggle_left_column()

    def plot_design_menu_clicked(self):
        selected_menu = self.ui.get_selected_menu()
        menu_name = selected_menu.objectName()

        if menu_name == "plot_design_menu":
            selected_menu.set_active(True)
            self.ui.set_page(self.plot_design_menu.plot_design_menu_widget)

            self.ui.set_left_column_menu(
                menu=self.plot_design_menu.plot_design_column_widget,
                title="Plot Design",
                icon_path=self.ui.images_load.icon_path("icon_plot_2d.svg"),
            )

            is_left_visible = self.ui.is_left_column_visible()
            if not is_left_visible:
                self.ui.toggle_left_column()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ApplicationWindow()
    window.show()
    sys.exit(app.exec())
