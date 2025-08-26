# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
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
import time

from PySide6.QtCore import QObject
from PySide6.QtCore import QThread
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QFileDialog


class AedtLauncherThread(QThread):
    finished = Signal(bool)
    progress_update = Signal(int)
    log_update = Signal(str)

    def __init__(self, main_window, version, session, non_graphical):
        super().__init__()
        self.main_window = main_window
        self.app = main_window.ui.app
        self.version = version
        self.session = session
        self.non_graphical = non_graphical
        self.aedt_launched = False

    def run(self):
        """
        Launch AEDT.

        This method handles the main logic for opening AEDT.
        """
        self.main_window.set_properties({"state": "AEDT launcher started", "progress": 5})

        self.app.launch_aedt(self.version, self.session, self.non_graphical)

        finished = False

        while not finished:
            if not self.main_window.backend_busy():
                finished = True
                properties = self.main_window.get_properties()
                actual_log = properties["state"]
                self.log_update.emit(actual_log)
                self.progress_update.emit(properties["progress"])
            time.sleep(1)

        self.aedt_launched = True
        self.finished.emit(self.aedt_launched)


class SettingsMenu(QObject):
    def __init__(self, main_window):
        super(SettingsMenu, self).__init__()
        self.main_window = main_window
        self.ui = main_window.ui
        self.app = self.ui.app
        self.app_color = self.main_window.ui.themes["app_color"]
        self.aedt_version_label = None
        self.aedt_version = None

        self.aedt_session_label = None
        self.aedt_session = None

        self.non_graphical_label = None
        self.graphical_label = None
        self.graphical_mode = None

        self.browse = None
        self.file = None

        self.connect_aedt = None

        self.signal_flag = True

        self.aedt_thread = None

        self.line1 = None
        self.line2 = None
        self.line3 = None
        self.line4 = None

    def setup(self):
        font_size = self.main_window.properties.font["combo_size"]
        # Version row
        row_returns = self.ui.add_combobox(
            self.ui.right_column.menus.settings_vertical_layout,
            height=40,
            width=[100, 135],
            label="AEDT Version",
            combobox_list=[],
            font_size=font_size,
        )

        self.ui.right_column.menus.browse_aedt_version = row_returns[0]

        self.aedt_version_label = row_returns[1]

        self.aedt_version = row_returns[2]

        self.aedt_version.currentTextChanged.connect(lambda: self.process_id())
        # Add line
        self.line1 = self.ui.add_vertical_line(
            self.ui.right_column.menus.settings_vertical_layout, top_spacer=[0, 10], bot_spacer=[0, 10]
        )

        # Session row
        row_returns = self.ui.add_combobox(
            self.ui.right_column.menus.settings_vertical_layout,
            height=40,
            width=[100, 135],
            label="AEDT Session",
            combobox_list=[],
            font_size=font_size,
        )

        self.ui.right_column.menus.browse_aedt_session = row_returns[0]
        self.aedt_session_label = row_returns[1]
        self.aedt_session = row_returns[2]
        self.aedt_session.showPopup = self.update_process_id

        # Add line
        self.line2 = self.ui.add_vertical_line(self.ui.right_column.menus.settings_vertical_layout, [0, 10], [0, 10])

        # Non-graphical
        row_returns = self.ui.add_toggle(
            self.ui.right_column.menus.settings_vertical_layout,
            height=30,
            width=[100, 135, 100],
            label=["Graphical", "Non-graphical"],
            font_size=font_size,
            bg_color=self.app_color["label_off"],
            active_color=self.app_color["label_on"],
        )

        self.ui.left_column.menus.non_graphical_select_row = row_returns[0]
        self.graphical_label = row_returns[1]
        self.graphical_mode = row_returns[2]
        self.non_graphical_label = row_returns[3]

        # Add line
        self.line3 = self.ui.add_vertical_line(
            self.ui.right_column.menus.settings_vertical_layout, top_spacer=[0, 10], bot_spacer=[0, 10]
        )

        # Browse row
        row_returns = self.ui.add_icon_button(
            self.ui.right_column.menus.settings_vertical_layout,
            icon=self.ui.images_load.icon_path("icon_folder_open.svg"),
            height=40,
            width=[40, 250],
            text="Browse...",
        )

        self.ui.right_column.menus.browse_file_group = row_returns[0]
        self.browse = row_returns[1]
        self.file = row_returns[2]

        self.browse.clicked.connect(lambda: self.browse_file())

        # Add line
        self.line4 = self.ui.add_vertical_line(
            self.ui.right_column.menus.settings_vertical_layout, top_spacer=[0, 10], bot_spacer=[0, 10]
        )

        # Launch AEDT
        row_returns = self.ui.add_n_buttons(
            self.ui.right_column.menus.settings_vertical_layout,
            num_buttons=1,
            height=80,
            width=[200],
            text=["Connect to AEDT"],
            font_size=font_size,
        )

        self.ui.right_column.menus.connect_aedt_layout = row_returns[0]
        self.connect_aedt = row_returns[1]

        # Disable launch AEDT
        self.connect_aedt.setEnabled(False)

        # Check backend connection
        success = self.app.check_connection()
        if success:
            backend_properties = self.app.get_properties()
            if backend_properties.get("selected_process") != 0:
                self.connect_aedt_directly()
            else:
                self.connect_aedt.clicked.connect(self.launch_aedt)

    def process_id(self):
        if self.signal_flag:
            self.aedt_session.clear()
            self.aedt_session.addItem("New Session")
            non_graphical = self.graphical_mode.isChecked()
            if self.aedt_version.currentText() and self.aedt_version.currentText() != "AEDT not installed":
                sessions = self.app.find_process_ids(self.aedt_version.currentText(), non_graphical)
                for pid in sessions:
                    if sessions[pid] == -1:
                        self.aedt_session.addItem("Process {}".format(pid))
                    else:
                        self.aedt_session.addItem("Grpc on port {}".format(sessions[pid]))

    def update_process_id(self):
        success = self.app.check_connection()
        if not success:
            msg = "Error getting properties from backend. User interface running without backend"
            self.ui.update_logger(msg)
            return
        non_graphical = self.graphical_mode.isChecked()
        item_count = self.aedt_session.count()

        # Retrieve all items as a list
        aedt_sessions_items = [self.aedt_session.itemText(i) for i in range(item_count)]
        if self.aedt_version.currentText() and self.aedt_version.currentText() != "AEDT not installed":
            sessions = self.app.find_process_ids(self.aedt_version.currentText(), non_graphical)
            for session in aedt_sessions_items:
                try:
                    session_id = int(session.split(" ")[-1])
                    if session_id not in sessions and session_id not in sessions.values():
                        self.aedt_session.removeItem(aedt_sessions_items.index(session))
                except ValueError:
                    pass
            for pid in sessions:
                if sessions[pid] == -1:
                    if "Process {}".format(pid) not in aedt_sessions_items:
                        self.aedt_session.addItem("Process {}".format(pid))
                elif "Grpc on port {}".format(sessions[pid]) not in aedt_sessions_items:
                    if "Process {}".format(pid) in aedt_sessions_items:
                        index = aedt_sessions_items.index("Process {}".format(pid))
                        self.aedt_session.removeItem(index)
                    self.aedt_session.addItem("Grpc on port {}".format(sessions[pid]))
        QComboBox.showPopup(self.aedt_session)

    def connect_aedt_directly(
        self,
    ):
        self.connect_aedt.setEnabled(False)
        self.aedt_version.setEnabled(False)
        self.aedt_session.setEnabled(False)
        self.aedt_thread = True
        self.connect_aedt.setEnabled(False)
        self.ui.title_bar.menu.setEnabled(False)
        self.ui.update_logger("AEDT session connected")

    def launch_aedt(self):
        selected_session = self.aedt_session.currentText()
        selected_version = self.aedt_version.currentText()
        non_graphical = self.graphical_mode.isChecked()
        self.aedt_thread = AedtLauncherThread(self.main_window, selected_version, selected_session, non_graphical)

        self.aedt_thread.start()

        self.aedt_thread.log_update.connect(self.ui.update_logger)
        self.aedt_thread.progress_update.connect(self.ui.update_progress)
        self.aedt_thread.finished.connect(self.handle_aedt_thread_finished)

        if self.main_window.properties.block_settings_after_load:
            self.connect_aedt.setEnabled(False)
            self.aedt_session.setEnabled(False)
        self.aedt_version.setEnabled(False)

    @Slot(bool)
    def handle_aedt_thread_finished(self, aedt_launched):
        # This method will be called when the thread finishes
        if aedt_launched:
            file = self.file.text()
            if file:
                aedt_file = os.path.normpath(file)
                self.app.open_project(aedt_file)
            self.app.home_menu.update_project()
            self.app.home_menu.update_design()
            if self.ui.is_right_column_visible():
                self.ui.toggle_right_column()
            if self.main_window.properties.block_settings_after_load:
                self.ui.title_bar.menu.setEnabled(False)
            self.ui.update_logger("AEDT session connected")
        else:
            self.ui.update_logger("AEDT not launched")

        self.aedt_thread.wait()
        self.aedt_thread.quit()
        self.ui.update_progress(100)

    def browse_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getOpenFileName(
            self.ui.app,
            "QFileDialog.getOpenFileName()",
            "",
            "Ansys Electronics Desktop Project Files (*.aedt *.aedtz)",
            options=options,
        )
        if file != "":
            self.file.setText(file)

    def hide_widgets(self):
        self.aedt_session.setVisible(False)
        self.aedt_session_label.setVisible(False)
        self.aedt_version.setVisible(False)
        self.aedt_version_label.setVisible(False)
        self.browse.setVisible(False)
        self.connect_aedt.setVisible(False)
        self.file.setVisible(False)
        self.graphical_label.setVisible(False)
        self.non_graphical_label.setVisible(False)
        self.graphical_mode.setVisible(False)

        self.line1.setVisible(False)
        self.line2.setVisible(False)
        self.line3.setVisible(False)
        self.line4.setVisible(False)

    def show_widgets(self):
        self.aedt_session.setVisible(True)
        self.aedt_session_label.setVisible(True)
        self.aedt_version.setVisible(True)
        self.aedt_version_label.setVisible(True)
        self.browse.setVisible(True)
        self.connect_aedt.setVisible(True)
        self.file.setVisible(True)
        self.graphical_label.setVisible(True)
        self.non_graphical_label.setVisible(True)
        self.graphical_mode.setVisible(True)

        self.line1.setVisible(True)
        self.line2.setVisible(True)
        self.line3.setVisible(True)
        self.line4.setVisible(True)
