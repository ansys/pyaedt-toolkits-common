from PySide6.QtCore import QThread
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget
from examples.toolkit.pyaedt_toolkit.ui.windows.plot_design.plot_design_column import Ui_LeftColumn


class PlotDesignMenu(object):
    def __init__(self, main_window):
        # General properties
        self.main_window = main_window
        self.ui = main_window.ui
        self.app = self.ui.app

        # Add page from common toolkit
        self.ui.load_pages.pages.addWidget(self.ui.load_pages.empty_page)
        plot_design_index = self.ui.load_pages.pages.indexOf(self.ui.load_pages.empty_page)
        self.ui.load_pages.pages.setCurrentIndex(plot_design_index)
        self.plot_design_menu_widget = self.ui.load_pages.pages.currentWidget()

        # Add left column
        new_column_widget = QWidget()
        new_ui = Ui_LeftColumn()
        new_ui.setupUi(new_column_widget)
        self.ui.left_column.menus.menus.addWidget(new_column_widget)
        self.plot_design_column_widget = new_column_widget
        self.plot_design_column_vertical_layout = new_ui.plot_design_vertical_layout

        # Specific properties
        self.plot_design_button_layout = None
        self.plot_design_button = None

    def setup(self):

        # Set column
        # Create geometry button
        row_returns = self.ui.add_n_buttons(
            self.plot_design_column_vertical_layout, num_buttons=1,
            height=40,
            width=[200],
            text=["Plot design"],
            font_size=self.app.properties.font["title_size"]
        )

        self.plot_design_button_layout = row_returns[0]
        self.plot_design_button = row_returns[1]
        self.plot_design_button_layout.addWidget(self.plot_design_button)
        self.plot_design_button.clicked.connect(self.plot_design_button_clicked)

    def plot_design_button_clicked(self):
        if not self.app.check_connection():
            msg = "Backend not running."
            self.ui.logger.log(msg)
            return False

        if self.geometry_thread and self.geometry_thread.isRunning() or self.app.backend_busy():
            msg = "Toolkit running"
            self.ui.logger.log(msg)
            self.app.logger.debug(msg)
            return False

        be_properties = self.app.get_properties()

        if be_properties.get("active_project"):
            self.ui.progress.progress = 0
        pass
