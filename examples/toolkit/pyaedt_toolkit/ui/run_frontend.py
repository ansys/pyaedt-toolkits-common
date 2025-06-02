import os
import sys

# PySide6 Widgets
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QApplication

# isort: off
# Default user interface properties
from examples.toolkit.pyaedt_toolkit.ui.models import properties
# isort: on

# Toolkit frontend API
from examples.toolkit.pyaedt_toolkit.ui.actions import Frontend

# Windows

# New windows
from examples.toolkit.pyaedt_toolkit.ui.windows.create_geometry.geometry_menu import GeometryMenu
from examples.toolkit.pyaedt_toolkit.ui.windows.plot_design.plot_design_menu import PlotDesignMenu
from examples.toolkit.pyaedt_toolkit.ui.windows.help.help_menu import HelpMenu

# Common windows
from ansys.aedt.toolkits.common.ui.main_window.main_window_layout import MainWindowLayout
from ansys.aedt.toolkits.common.ui.common_windows.home_menu import HomeMenu
from ansys.aedt.toolkits.common.ui.common_windows.settings_column import SettingsMenu
from ansys.aedt.toolkits.common.ui.utils.resolution import set_pyside_resolution

# Import general common frontend modules
from ansys.aedt.toolkits.common.ui.logger_handler import logger

# Backend URL and port
if len(sys.argv) == 3:
    properties.backend_url = sys.argv[1]
    properties.backend_port = int(sys.argv[2])

url = properties.backend_url
port = properties.backend_port

os.environ["QT_API"] = "pyside6"
os.environ["QT_FONT_DPI"] = "96"

set_pyside_resolution(properties, use_tkinter=True)
properties.version = "example_toolkit_version"


class ApplicationWindow(QMainWindow, Frontend):
    def __init__(self):
        super().__init__()

        self.thread = None
        self.properties = properties

        # General Settings

        # Create main window layout
        self.ui = MainWindowLayout(self)
        self.ui.setup()

        # Home menu
        self.home_menu = HomeMenu(self)
        self.home_menu.setup()
        self.ui.left_menu.clicked.connect(self.home_menu_clicked)

        # Settings menu
        self.settings_menu = SettingsMenu(self)
        self.settings_menu.setup()
        self.ui.title_bar.clicked.connect(self.settings_menu_clicked)

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

            self.settings_menu.aedt_session.clear()
            self.settings_menu.aedt_session.addItem("New Session")
            if installed_versions:
                self.settings_menu.connect_aedt.setEnabled(True)
                for ver in installed_versions:
                    self.settings_menu.aedt_version.addItem(ver)
            else:
                self.settings_menu.aedt_version.addItem("AEDT not installed")

            if be_properties.get("aedt_version") in installed_versions:
                self.settings_menu.aedt_version.setCurrentText(be_properties.get("aedt_version"))

        # Custom toolkit setup starts here

        # Modeler menu
        self.geometry_menu = GeometryMenu(self)
        self.geometry_menu.setup()
        self.ui.left_menu.clicked.connect(self.geometry_menu_clicked)

        # Plot design menu
        self.plot_design_menu = PlotDesignMenu(self)
        self.plot_design_menu.setup()
        self.ui.left_menu.clicked.connect(self.plot_design_menu_clicked)

        # Help menu
        self.help_menu = HelpMenu(self)
        self.help_menu.setup()
        self.ui.left_menu.clicked.connect(self.help_menu_clicked)

        # Close column
        self.ui.title_bar.clicked.connect(self.close_menu_clicked)
        self.ui.left_menu.clicked.connect(self.progress_menu_clicked)
        self.ui.left_column.clicked.connect(self.close_menu_clicked)

        # Home page as first page
        self.ui.set_page(self.ui.load_pages.home_page)

    def home_menu_clicked(self):
        selected_menu = self.ui.get_selected_menu()
        menu_name = selected_menu.objectName()
        self.ui.left_menu.select_only_one(selected_menu.objectName())
        if menu_name == "home_menu":
            selected_menu.set_active(True)
            self.ui.set_page(self.ui.load_pages.home_page)

            is_left_visible = self.ui.is_left_column_visible()

            self.ui.set_left_column_menu(
                menu=self.ui.left_column.menus.menu_home,
                title="Home",
                icon_path=self.ui.images_load.icon_path("icon_home.svg"),
            )

            if not is_left_visible:
                self.ui.toggle_left_column()

    def settings_menu_clicked(self):
        selected_menu = self.ui.get_selected_menu()
        menu_name = selected_menu.objectName()
        is_right_visible = self.ui.is_right_column_visible()
        is_left_visible = self.ui.is_left_column_visible()

        if menu_name == "top_settings" and not is_right_visible:
            self.ui.app.settings_menu.show_widgets()
            if is_left_visible:
                self.ui.toggle_left_column()
                self.ui.left_menu.deselect_all()
            self.ui.toggle_right_column()
            self.ui.set_right_column_menu(title="Settings")

    def progress_menu_clicked(self):
        selected_menu = self.ui.get_selected_menu()
        menu_name = selected_menu.objectName()
        self.ui.left_menu.select_only_one(selected_menu.objectName())
        if menu_name == "progress_menu":
            is_progress_visible = self.ui.is_progress_visible()
            if is_progress_visible:
                selected_menu.set_active(False)
            self.ui.toggle_progress()

    def close_menu_clicked(self):
        selected_menu = self.ui.get_selected_menu()
        menu_name = selected_menu.objectName()
        if menu_name != "top_settings" and self.ui.is_left_column_visible():
            selected_menu.set_active(False)
            self.ui.toggle_left_column()
            self.ui.left_menu.deselect_all()
        if menu_name == "top_settings" and self.ui.is_right_column_visible():
            self.ui.toggle_right_column()

    def geometry_menu_clicked(self):
        selected_menu = self.ui.get_selected_menu()
        menu_name = selected_menu.objectName()
        self.ui.left_menu.select_only_one(selected_menu.objectName())
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
        self.ui.left_menu.select_only_one(selected_menu.objectName())
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

    def help_menu_clicked(self):
        selected_menu = self.ui.get_selected_menu()
        menu_name = selected_menu.objectName()
        self.ui.left_menu.select_only_one(selected_menu.objectName())
        if menu_name == "help_menu":
            selected_menu.set_active(True)
            self.ui.set_page(self.help_menu.plot_design_menu_widget)

            self.ui.set_left_column_menu(
                menu=self.help_menu.plot_design_column_widget,
                title="Help",
                icon_path=self.ui.images_load.icon_path("help.svg"),
            )

            is_left_visible = self.ui.is_left_column_visible()
            if not is_left_visible:
                self.ui.toggle_left_column()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ApplicationWindow()
    window.show()
    sys.exit(app.exec())
