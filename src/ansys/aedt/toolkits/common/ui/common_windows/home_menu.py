# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from PySide6.QtCore import Qt
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QSpacerItem

from ansys.aedt.toolkits.common.ui.models import general_settings


class HomeMenu(object):
    def __init__(self, main_window):
        self.main_window = main_window
        self.ui = main_window.ui
        self.app = self.ui.app

        # File Mode
        self.mode = "aedt_based"
        self.aedt_mode = None
        self.aedt_mode_label = None
        self.file_mode_label = None
        self.mode_line = None

        self.browse = None
        self.file = None

        self.project = None
        self.project_combobox = None

        self.design = None
        self.design_combobox = None

        welcome_label = self.ui.load_pages.home_page.findChild(QLabel, "label")
        # Add welcome message
        message = general_settings.welcome_message
        welcome_label.setText(message)

    def setup(self):
        # Project row
        row_returns = self.ui.add_combobox(
            self.ui.left_column.menus.home_vertical_layout,
            height=40,
            width=[75, 135],
            label="Project",
            combobox_list=["No Project"],
        )

        self.ui.left_column.menus.browse_project_group = row_returns[0]
        self.project = row_returns[1]
        self.project_combobox = row_returns[2]
        self.project_combobox.currentIndexChanged.connect(lambda: self.update_design())
        self.project_combobox.setEnabled(False)

        # Design row
        row_returns = self.ui.add_combobox(
            self.ui.left_column.menus.home_vertical_layout,
            height=40,
            width=[75, 135],
            label="Design",
            combobox_list=["No Design"],
        )

        self.ui.left_column.menus.browse_design_group = row_returns[0]
        self.design = row_returns[1]
        self.design_combobox = row_returns[2]

        spacer = QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.ui.left_column.menus.home_vertical_layout.addItem(spacer)

        # Add logo to main page depending on the theme, we can change the logo to white or black version
        if not general_settings.logo:
            main_window_logo = self.ui.images_load.image_path("ansys-primary-logo-black.svg")
            if self.ui.themes["theme_name"] == "ansys_dark":
                main_window_logo = self.ui.images_load.image_path("ansys-primary-logo-white.svg")
        else:
            main_window_logo = general_settings.logo
        main_logo = QSvgWidget(main_window_logo)
        self.ui.load_pages.logo_layout.addWidget(main_logo, Qt.AlignCenter, Qt.AlignCenter)

        main_logo.setFixedSize(240, 120)

        # Check backend connection
        success = self.app.check_connection()
        if success:
            backend_properties = self.app.get_properties()
            if backend_properties.get("active_project") and backend_properties.get("active_design"):
                self.update_project()
                self.update_design()

    def update_project(self):
        self.project_combobox.blockSignals(True)
        project_list = self.app.get_aedt_data()
        self.main_window.home_menu.project_combobox.setEnabled(True)
        self.main_window.home_menu.project_combobox.clear()
        self.main_window.home_menu.project_combobox.addItems(project_list)
        self.project_combobox.blockSignals(False)
        return project_list

    def update_design(self):
        self.project_combobox.blockSignals(True)
        design_list = self.app.update_design_names()
        self.main_window.home_menu.design_combobox.clear()
        self.main_window.home_menu.design_combobox.addItems(design_list)
        self.project_combobox.blockSignals(False)
