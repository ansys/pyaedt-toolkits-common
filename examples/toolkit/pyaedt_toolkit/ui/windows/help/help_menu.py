from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QWidget
from windows.plot_design.plot_design_column import Ui_LeftColumn
from windows.plot_design.plot_design_page import Ui_Plot_Design

import tempfile
from ansys.aedt.toolkits.common import __version__

ABOUT_TEXT = f"""<h2>PyAEDT Common Toolkit {__version__}</h2>
<p>Project using <a href='https://wiki.qt.io/Qt_for_Python'> PySide6</a>.</p>
<p>If you have any questions or issues, please open an issue in <a href='https://github.com/ansys/pyaedt-toolkits-common/issues'>pyaedt-toolkits-common Issues</a> page.</p>
<p>Alternatively, you can contact us at <a href='mailto:pyansys.core@ansys.com'>pyansys.core@ansys.com</a>.</p>
<p>Your use of this software is governed by the MIT License. In addition, this package allows you to access a software that is licensed under separate terms ("Separately Licensed Software"). If you chose to install such Separately Licensed Software, you acknowledge that you are responsible for complying with any associated terms and conditions.</p>
<p>Copyright 2023 - 2024 ANSYS, Inc. All rights reserved.</p>
"""
DOCUMENTATION_URL = "https://aedt.common.toolkit.docs.pyansys.com/"
ISSUE_TRACKER_URL = "https://github.com/ansys/pyaedt-toolkits-common/issues"


class HelpMenu(object):
    def __init__(self, main_window):
        # General properties
        self.main_window = main_window
        self.ui = main_window.ui
        self.temp_folder = tempfile.mkdtemp()

        # Add page
        plot_design_menu_index = self.ui.add_page(Ui_Plot_Design)
        self.ui.load_pages.pages.setCurrentIndex(plot_design_menu_index)
        self.plot_design_menu_widget = self.ui.load_pages.pages.currentWidget()

        # Add left column
        new_column_widget = QWidget()
        new_ui = Ui_LeftColumn()
        new_ui.setupUi(new_column_widget)
        self.ui.left_column.menus.menus.addWidget(new_column_widget)
        self.plot_design_column_widget = new_column_widget
        self.plot_design_column_vertical_layout = new_ui.plot_design_vertical_layout

        # Specific properties
        self.plot_design_label = self.plot_design_menu_widget.findChild(QLabel, "plot_design_label")
        self.plot_design_grid = self.plot_design_menu_widget.findChild(QGridLayout, "plot_design_grid")

        self.plot_design_button_layout = None
        self.plot_design_button = None
        self.online_documentation_button = None
        self.issue_tracker_button = None

    def setup(self):
        # Modify theme
        app_color = self.main_window.ui.themes["app_color"]
        text_color = app_color["text_active"]
        background = app_color["dark_three"]

        # Label button
        plot_design_label_style = """
        QLabel {{
        color: {_color};
        font-size: {_font_size}pt;
        font-weight: bold;
        }}
        """
        custom_style = plot_design_label_style.format(
            _color=text_color, _bg_color=background, _font_size=self.main_window.properties.font["title_size"]
        )
        self.plot_design_label.setStyleSheet(custom_style)

        # Set column

        # About button
        row_returns = self.ui.add_n_buttons(
            self.plot_design_column_vertical_layout, num_buttons=1,
            height=40,
            width=[200],
            text=["About"],
            font_size=self.main_window.properties.font["title_size"]
        )
        self.plot_design_button_layout = row_returns[0]
        self.plot_design_button = row_returns[1]
        self.plot_design_button_layout.addWidget(self.plot_design_button)
        self.plot_design_button.clicked.connect(self.about_button_clicked)

        # Documentation button
        row_returns = self.ui.add_n_buttons(
            self.plot_design_column_vertical_layout, num_buttons=1,
            height=40,
            width=[200],
            text=["Documentation website"],
            font_size=self.main_window.properties.font["title_size"]
        )
        self.plot_design_button_layout = row_returns[0]
        self.online_documentation_button = row_returns[1]
        self.plot_design_button_layout.addWidget(self.online_documentation_button)
        self.online_documentation_button.clicked.connect(self.visit_website)

        # Issue tracker button
        row_returns = self.ui.add_n_buttons(
            self.plot_design_column_vertical_layout, num_buttons=1,
            height=40,
            width=[200],
            text=["Issue tracker"],
            font_size=self.main_window.properties.font["title_size"]
        )
        print(row_returns)
        self.plot_design_button_layout = row_returns[0]
        self.issue_tracker_button = row_returns[1]
        self.plot_design_button_layout.addWidget(self.issue_tracker_button)
        self.issue_tracker_button.clicked.connect(self.report_issue)

    def about_button_clicked(self):
        """Display the PyAEDT Common Toolkit 'About' information."""

        mbox = QtWidgets.QMessageBox.about(self.main_window, "About", ABOUT_TEXT)

    def visit_website(self):
        """Access the PyAEDT Common Toolkit documentation."""
        url = QtCore.QUrl(DOCUMENTATION_URL)
        QtGui.QDesktopServices.openUrl(url)

    def report_issue(self):
        """Access the PyAEDT Common Toolkit issues tracker."""
        url = QtCore.QUrl(ISSUE_TRACKER_URL)
        QtGui.QDesktopServices.openUrl(url)
