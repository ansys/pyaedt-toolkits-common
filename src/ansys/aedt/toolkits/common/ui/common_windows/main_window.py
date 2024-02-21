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

from ansys.aedt.toolkits.common.ui.models import general_settings


class MainWindow(object):
    def __init__(self, app):
        self._app = app
        # App title
        self._app.setWindowTitle(general_settings.app_name)

    def setup(self, main_window_logo=None):
        # Add title
        if not hasattr(general_settings, "main_title"):
            title = "toolkit"
        else:
            title = general_settings.main_title
        self._app.ui.title_bar.set_title(title)

        # Add menus
        self._app.ui.left_menu.add_menus(general_settings.add_left_menus)
        self._app.ui.title_bar.add_menus(general_settings.add_title_bar_menus)

        # Set left menu signal
        self._app.ui.left_menu.clicked.connect(self.main_clicked)

        # Set left column signal
        self._app.ui.left_column.clicked.connect(self.main_clicked)

        # Set title bar menu signal
        self._app.ui.title_bar.clicked.connect(self.main_clicked)

        # Set right column signal
        self._app.ui.right_column.clicked.connect(self.main_clicked)

        # Load main page
        self._app.ui.set_page(self._app.ui.load_pages.home_page)

        # Add logo to main page
        if not main_window_logo:
            main_window_logo = self._app.ui.images_load.image_path("ANSS_BIG.D.svg")
        main_logo = QSvgWidget(main_window_logo)
        self._app.ui.load_pages.logo_layout.addWidget(main_logo, Qt.AlignCenter, Qt.AlignCenter)

        welcome_label = self._app.ui.load_pages.home_page.findChild(QLabel, "label")
        # Add welcome message
        if hasattr(general_settings, "welcome_message"):
            message = general_settings.welcome_message
            welcome_label.setText(message)

    def get_selected_menu(self):
        if self._app.ui.title_bar.sender() is not None:
            return self._app.ui.title_bar.sender()
        elif self._app.ui.left_menu.sender() is not None:
            return self._app.ui.left_menu.sender()
        elif self._app.ui.left_column.sender() is not None:
            return self._app.ui.left_column.sender()
        elif self._app.ui.right_column.sender() is not None:
            return self._app.ui.right_column.sender()

    def main_clicked(self):
        selected_menu = self.get_selected_menu()

        is_left_visible = self._app.ui.is_left_column_visible()
        is_right_visible = self._app.ui.is_right_column_visible()
        is_progress_visible = self._app.ui.is_progress_visible()

        self._app.ui.left_menu.select_only_one(selected_menu.objectName())

        if selected_menu.objectName() == "home_menu":
            selected_menu.set_active(True)
            self._app.ui.set_page(self._app.ui.load_pages.home_page)
            if not is_left_visible:
                self._app.ui.toggle_left_column()
            self._app.ui.set_left_column_menu(
                menu=self._app.ui.left_column.menus.menu_home,
                title="Home",
                icon_path=self._app.ui.images_load.icon_path("icon_home.svg"),
            )

        elif selected_menu.objectName() == "top_settings" and not is_right_visible:
            if is_left_visible:
                self._app.ui.toggle_left_column()
            self._app.ui.toggle_right_column()
            self._app.ui.set_right_column_menu(title="Settings")

        elif selected_menu.objectName() == "progress_menu":
            if is_progress_visible:
                selected_menu.set_active(False)
            self._app.ui.toggle_progress()

        elif selected_menu.objectName() == "close_left_column" or is_right_visible:
            if self._app.ui.is_left_column_visible():
                selected_menu.set_active(False)
                self._app.ui.toggle_left_column()
            elif self._app.ui.is_right_column_visible:
                self._app.ui.toggle_right_column()
