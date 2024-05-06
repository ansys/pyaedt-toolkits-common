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

import os

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from ansys.aedt.toolkits.common.ui.models import general_settings
from ansys.aedt.toolkits.common.ui.utils.images.load_images import LoadImages
from ansys.aedt.toolkits.common.ui.utils.themes.json_themes import ThemeHandler
from ansys.aedt.toolkits.common.ui.utils.ui_templates.pages.ui_main_pages import Ui_MainPages
from ansys.aedt.toolkits.common.ui.utils.widgets.py_credits.py_credits import PyCredits
from ansys.aedt.toolkits.common.ui.utils.widgets.py_left_column.py_left_column import PyLeftColumn
from ansys.aedt.toolkits.common.ui.utils.widgets.py_left_menu.py_left_menu import PyLeftMenu
from ansys.aedt.toolkits.common.ui.utils.widgets.py_logger.py_logger import PyLogger
from ansys.aedt.toolkits.common.ui.utils.widgets.py_progress.py_progress import PyProgress
from ansys.aedt.toolkits.common.ui.utils.widgets.py_right_column.py_right_column import PyRightColumn
from ansys.aedt.toolkits.common.ui.utils.widgets.py_title_bar.py_title_bar import PyTitleBar
from ansys.aedt.toolkits.common.ui.utils.widgets.py_window.py_window import PyWindow

# Widgets
from ansys.aedt.toolkits.common.ui.utils.windows.common_window_utils import CommonWindowUtils

if os.environ.get("AEDT_TOOLKIT_THEME", False):
    general_settings.theme = os.environ["AEDT_TOOLKIT_THEME"]


def setup_parent_ui(parent):
    """Setup UI for parent."""
    parent.setObjectName("MainWindow")
    parent.resize(*general_settings.startup_size)
    parent.setMinimumSize(*general_settings.minimum_size)


class MainWindowLayout(CommonWindowUtils):
    """Class representing the main window of the application."""

    def __init__(self, app):
        CommonWindowUtils.__init__(self)

        self.app = app

        self.app.setWindowTitle(general_settings.app_name)

        # Load available themes
        self.themes = ThemeHandler().items

        # Load available images
        self.images_load = LoadImages()

        icon = self.__load_icon()
        self.app.setWindowIcon(icon)

        # Main window init
        self.main_window_layout = None
        self.main_window = None

        # Central menu
        self.central_frame = None
        self.central_layout = None
        self.central_widget = None

        # Left menu
        self.left_menu_frame = None
        self.left_menu_layout = None
        self.left_menu = None

        # Left column
        self.left_column_frame = None
        self.left_column_layout = None
        self.left_column = None

        # Title
        self.title_bar_frame = None
        self.title_bar_layout = None
        self.title_bar = None

        # Content
        self.content_frame = None
        self.content_layout = None
        self.load_pages = None

        # Progress
        self.progress_frame = None
        self.progress_layout = None
        self.progress = None
        self.logger = None

        # Credits
        self.credits_frame = None
        self.credits_layout = None
        self.credits = None

        # Right Column
        self.right_column_frame = None
        self.right_column_layout = None
        self.right_column = None

    def setup(self):
        """Setup UI for parent widget."""
        setup_parent_ui(self.app)
        self.__setup_main_window_layout()
        self.__setup_central_layout()
        self.__setup_title_layout()
        self.__setup_content_layout()
        self.__setup_progress_layout()
        self.__setup_credits_layout()
        self.__setup_left_menu_layout()
        self.__setup_left_column_layout()
        self.__setup_right_column_layout()

        # Add frames to main window
        if self.main_window:
            # Left menu
            self.main_window.layout.addWidget(self.left_menu_frame)
            self.main_window.layout.addWidget(self.left_column_frame)

            # Central menu
            self.central_layout.addWidget(self.title_bar_frame)
            self.central_layout.addWidget(self.content_frame)
            self.central_layout.addWidget(self.progress_frame)
            self.central_layout.addWidget(self.credits_frame)
            self.main_window.layout.addWidget(self.central_frame)

            # Right column
            self.main_window.layout.addWidget(self.right_column_frame)

            # Import to set the UI
            self.app.setCentralWidget(self.main_window)

    def __setup_main_window_layout(self):
        """Setup main window."""
        color = self.themes["app_color"]
        self.main_window_layout = QHBoxLayout()
        self.main_window_layout.setContentsMargins(0, 0, 0, 0)
        self.main_window = PyWindow(
            parent=self.app,
            bg_color=color["bg_one"],
            border_color=color["bg_two"],
            text_color=color["text_foreground"],
            border_radius=0,
            border_size=0,
        )
        self.main_window_layout.addWidget(self.main_window)

    def __setup_central_layout(self):
        """Setup central widget."""
        self.central_frame = QFrame(self.main_window)
        self.central_layout = QVBoxLayout()
        self.central_frame.setLayout(self.central_layout)
        self.central_layout.setContentsMargins(3, 3, 3, 3)
        self.central_layout.setSpacing(6)

        self.central_widget = QWidget(self.main_window)
        style = f"""
        color: {self.themes["app_color"]["text_foreground"]};
        font: {general_settings.font["text_size"]}pt "{general_settings.font["family"]}";
        """
        self.central_widget.setStyleSheet(style)
        self.central_layout.addWidget(self.central_widget)

    def __setup_title_layout(self):
        self.title_bar_frame = QFrame(self.central_widget)
        self.title_bar_frame.setMinimumHeight(40)
        self.title_bar_frame.setMaximumHeight(40)
        self.title_bar_layout = QVBoxLayout()
        self.title_bar_frame.setLayout(self.title_bar_layout)
        self.title_bar_layout.setContentsMargins(0, 0, 0, 0)

        logo = self.images_load.image_path("ansys-primary-logo-black.svg")
        if self.themes["theme_name"] == "ansys_dark":
            logo = self.images_load.image_path("ansys-primary-logo-white.svg")

        self.title_bar = PyTitleBar(
            parent=self.main_window,
            app_parent=self.app,
            logo_width=70,
            logo_image=self.images_load.image_path(logo),
            bg_color=self.themes["app_color"]["bg_two"],
            div_color=self.themes["app_color"]["bg_three"],
            btn_bg_color=self.themes["app_color"]["bg_two"],
            btn_bg_color_hover=self.themes["app_color"]["bg_three"],
            btn_bg_color_pressed=self.themes["app_color"]["bg_one"],
            icon_color=self.themes["app_color"]["icon_color"],
            icon_color_hover=self.themes["app_color"]["icon_hover"],
            icon_color_pressed=self.themes["app_color"]["icon_pressed"],
            icon_color_active=self.themes["app_color"]["icon_active"],
            context_color=self.themes["app_color"]["context_color"],
            dark_one=self.themes["app_color"]["dark_one"],
            text_foreground=self.themes["app_color"]["text_foreground"],
            radius=8,
            font_family=general_settings.font["family"],
            title_size=general_settings.font["title_size"],
        )
        self.title_bar_layout.addWidget(self.title_bar)

        # Set title bar menu signal
        self.title_bar.clicked.connect(self.main_clicked)

        title = general_settings.main_title
        self.title_bar.set_title(title)

        self.title_bar.add_menus(general_settings.add_title_bar_menus)

    def __setup_progress_layout(self):
        """Setup progress frame."""
        self.progress_frame = QFrame(self.central_widget)

        progress_menu_minimum = general_settings.progress_size["minimum"]

        self.progress_layout = QHBoxLayout()
        self.progress_frame.setLayout(self.progress_layout)
        self.progress_layout.setContentsMargins(0, 0, 0, 0)
        self.progress_frame.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.progress_frame.setMinimumHeight(progress_menu_minimum)
        self.progress_frame.setMaximumHeight(progress_menu_minimum)

        self.progress = PyProgress(
            progress=0,
            progress_color=self.themes["app_color"]["icon_color"],
            background_color=self.themes["app_color"]["bg_one"],
            text_color=self.themes["app_color"]["text_active"],
            font_size=general_settings.font["title_size"],
            font_family=general_settings.font["family"],
            width=10,
        )

        self.logger = PyLogger(
            text_color=self.themes["app_color"]["text_active"],
            background_color=self.themes["app_color"]["bg_two"],
            height=general_settings.progress_size["maximum"],
            font_size=general_settings.font["title_size"],
            font_family=general_settings.font["family"],
        )

        self.progress_layout.addWidget(self.logger)
        self.update_logger("{} logger".format(general_settings.app_name))
        self.progress_layout.addWidget(self.progress)

    def __setup_credits_layout(self):
        """Setup credits frame."""
        self.credits_frame = QFrame(self.central_widget)
        self.credits_frame.setMinimumHeight(26)
        self.credits_frame.setMaximumHeight(26)
        self.credits_layout = QVBoxLayout()
        self.credits_frame.setLayout(self.credits_layout)
        self.credits_layout.setContentsMargins(0, 0, 0, 0)
        self.credits = PyCredits(
            bg=self.themes["app_color"]["bg_two"],
            text=general_settings.copyright,
            version=general_settings.version,
            font_family=general_settings.font["family"],
            text_size=general_settings.font["text_size"],
            text_description_color=self.themes["app_color"]["text_description"],
        )
        self.credits_layout.addWidget(self.credits)

    def __setup_left_menu_layout(self):
        """Setup left menu."""
        self.left_menu_frame = QFrame(self.main_window)
        self.left_menu_layout = QHBoxLayout()
        self.left_menu_frame.setLayout(self.left_menu_layout)
        left_menu_margin = general_settings.left_menu_content_margins
        left_menu_minimum = general_settings.left_menu_size["minimum"]
        self.left_menu_frame.setMaximumSize(left_menu_minimum + (left_menu_margin * 2), 17280)
        self.left_menu_frame.setMinimumSize(left_menu_minimum + (left_menu_margin * 2), 0)
        self.left_menu_layout.setContentsMargins(left_menu_margin, left_menu_margin, left_menu_margin, left_menu_margin)
        self.left_menu = PyLeftMenu(
            parent=self.left_menu_frame,
            app_parent=self.app,
            dark_one=self.themes["app_color"]["dark_one"],
            dark_three=self.themes["app_color"]["dark_three"],
            dark_four=self.themes["app_color"]["dark_four"],
            bg_one=self.themes["app_color"]["bg_one"],
            icon_color=self.themes["app_color"]["icon_color"],
            icon_color_hover=self.themes["app_color"]["icon_hover"],
            icon_color_pressed=self.themes["app_color"]["icon_pressed"],
            icon_color_active=self.themes["app_color"]["icon_active"],
            context_color=self.themes["app_color"]["context_color"],
            text_foreground=self.themes["app_color"]["text_foreground"],
            text_active=self.themes["app_color"]["text_active"],
        )

        # Add left menu widget to left menu layout
        self.left_menu_layout.addWidget(self.left_menu)

        # Set left menu signal
        self.left_menu.clicked.connect(self.main_clicked)

        self.left_menu.add_menus(general_settings.add_left_menus)

    def __setup_left_column_layout(self):
        """Setup left column."""
        self.left_column_frame = QFrame(self.main_window)
        self.left_column_layout = QVBoxLayout()
        self.left_column_frame.setLayout(self.left_column_layout)
        self.left_column_frame.setMaximumWidth(general_settings.left_column_size["minimum"])
        self.left_column_frame.setMinimumWidth(general_settings.left_column_size["minimum"])
        self.left_column_frame.setStyleSheet(f"background: {self.themes['app_color']['bg_two']}")
        self.left_column_layout.setContentsMargins(0, 0, 0, 0)

        # Left column widget
        self.left_column = PyLeftColumn(
            text_title="Settings Left Frame",
            text_title_size=general_settings.font["title_size"],
            text_title_color=self.themes["app_color"]["text_foreground"],
            icon_path=self.images_load.icon_path("icon_settings.svg"),
            dark_one=self.themes["app_color"]["dark_one"],
            bg_color=self.themes["app_color"]["bg_three"],
            btn_color=self.themes["app_color"]["bg_three"],
            btn_color_hover=self.themes["app_color"]["bg_two"],
            btn_color_pressed=self.themes["app_color"]["bg_one"],
            icon_color=self.themes["app_color"]["icon_color"],
            icon_color_hover=self.themes["app_color"]["icon_hover"],
            context_color=self.themes["app_color"]["context_color"],
            icon_color_pressed=self.themes["app_color"]["icon_pressed"],
            icon_close_path=self.images_load.icon_path("icon_close.svg"),
        )

        # Add left column widget to left menu layout
        self.left_column_layout.addWidget(self.left_column)

        # Set left column signal
        self.left_column.clicked.connect(self.main_clicked)

    def __setup_right_column_layout(self):
        """Setup right column."""
        self.right_column_frame = QFrame(self.main_window)
        self.right_column_layout = QVBoxLayout()
        self.right_column_frame.setLayout(self.right_column_layout)
        self.right_column_frame.setMaximumWidth(general_settings.right_column_size["minimum"])
        self.right_column_frame.setMinimumWidth(general_settings.right_column_size["minimum"])
        self.right_column_frame.setStyleSheet(f"background: {self.themes['app_color']['bg_two']}")
        self.right_column_layout.setContentsMargins(0, 0, 0, 0)

        # Left column widget
        self.right_column = PyRightColumn(
            text_title="Settings Right Frame",
            text_title_size=general_settings.font["title_size"],
            text_title_color=self.themes["app_color"]["text_foreground"],
            icon_path=self.images_load.icon_path("icon_settings.svg"),
            dark_one=self.themes["app_color"]["dark_one"],
            bg_color=self.themes["app_color"]["bg_three"],
            btn_color=self.themes["app_color"]["bg_three"],
            btn_color_hover=self.themes["app_color"]["bg_two"],
            btn_color_pressed=self.themes["app_color"]["bg_one"],
            icon_color=self.themes["app_color"]["icon_color"],
            icon_color_hover=self.themes["app_color"]["icon_hover"],
            context_color=self.themes["app_color"]["context_color"],
            icon_color_pressed=self.themes["app_color"]["icon_pressed"],
        )

        # Add left column widget to left menu layout
        self.right_column_layout.addWidget(self.right_column)

        # Set right column signal
        self.right_column.clicked.connect(self.main_clicked)

    def __setup_content_layout(self):
        """Setup content area."""

        self.content_frame = QFrame(self.central_widget)
        self.content_layout = QVBoxLayout()

        self.content_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.load_pages = Ui_MainPages()
        self.load_pages.setupUi(self.content_frame)
        self.content_layout.addWidget(self.content_frame)

    def add_page(self, page_ui):
        """Create a new page to the user interface."""
        new_page = QWidget()
        new_ui = page_ui()
        new_ui.setupUi(new_page)

        # Add the new page to the existing layout
        self.load_pages.pages.addWidget(new_page)
        index = self.load_pages.pages.indexOf(new_page)
        return index

    def get_selected_menu(self):
        if self.title_bar.sender() is not None:
            return self.title_bar.sender()
        elif self.left_menu.sender() is not None:
            return self.left_menu.sender()
        elif self.left_column.sender() is not None:
            return self.left_column.sender()
        elif self.right_column.sender() is not None:
            return self.right_column.sender()

    def main_clicked(self):
        selected_menu = self.get_selected_menu()

        is_left_visible = self.is_left_column_visible()
        is_right_visible = self.is_right_column_visible()
        is_progress_visible = self.is_progress_visible()

        self.left_menu.select_only_one(selected_menu.objectName())

        if selected_menu.objectName() == "home_menu":
            selected_menu.set_active(True)
            self.set_page(self.load_pages.home_page)
            self.set_left_column_menu(
                menu=self.left_column.menus.menu_home,
                title="Home",
                icon_path=self.images_load.icon_path("icon_home.svg"),
            )

            if not is_left_visible:
                self.toggle_left_column()

        elif selected_menu.objectName() == "top_settings" and not is_right_visible:
            if is_left_visible:
                self.toggle_left_column()
            self.toggle_right_column()
            self.set_right_column_menu(title="Settings")

        elif selected_menu.objectName() == "progress_menu":
            if is_progress_visible:
                selected_menu.set_active(False)
            self.toggle_progress()

        elif selected_menu.objectName() == "close_left_column" or is_right_visible:
            if self.is_left_column_visible():
                selected_menu.set_active(False)
                self.toggle_left_column()
            elif self.is_right_column_visible:
                self.toggle_right_column()

    def __load_icon(self):
        icon = QtGui.QIcon()
        if not general_settings.icon:
            icon.addFile(
                self.images_load.image_path("logo.png"),
                QtCore.QSize(),
                QtGui.QIcon.Normal,
                QtGui.QIcon.On,
            )
        else:
            icon.addFile(
                general_settings.icon,
                QtCore.QSize(),
                QtGui.QIcon.Normal,
                QtGui.QIcon.On,
            )
        return icon
