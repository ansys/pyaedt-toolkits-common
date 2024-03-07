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

from PySide6.QtCore import QObject
from PySide6.QtCore import QThread
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFileDialog


class AedtLauncherThread(QThread):
    finished_signal = Signal(bool)

    def __init__(self, app, version, session, non_graphical):
        super().__init__()
        self.app = app
        self.version = version
        self.session = session
        self.non_graphical = non_graphical

    def run(self):
        self.app.launch_aedt(self.version, self.session, self.non_graphical)
        aedt_launched = self.app.wait_thread(120)
        self.finished_signal.emit(aedt_launched)


class SettingsMenu(QObject):
    def __init__(self, main_window):
        super(SettingsMenu, self).__init__()
        self.main_window = main_window
        self.ui = main_window.ui
        self.app = self.ui.app

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

    def setup(self):
        # Version row
        row_returns = self.ui.add_combobox(
            self.ui.right_column.menus.settings_vertical_layout,
            height=40,
            width=[75, 135],
            label="AEDT Version",
            combobox_list=[],
        )

        self.ui.right_column.menus.browse_aedt_version = row_returns[0]

        self.aedt_version_label = row_returns[1]

        self.aedt_version = row_returns[2]

        self.aedt_version.currentTextChanged.connect(lambda: self.process_id())

        # Add line
        self.ui.add_vertical_line(
            self.ui.right_column.menus.settings_vertical_layout, top_spacer=[0, 10], bot_spacer=[0, 10]
        )

        # Session row
        row_returns = self.ui.add_combobox(
            self.ui.right_column.menus.settings_vertical_layout,
            height=40,
            width=[75, 135],
            label="AEDT Session",
            combobox_list=[],
        )

        self.ui.right_column.menus.browse_aedt_session = row_returns[0]
        self.aedt_session_label = row_returns[1]
        self.aedt_session = row_returns[2]

        # Add line
        self.ui.add_vertical_line(self.ui.right_column.menus.settings_vertical_layout, [0, 10], [0, 20])

        # Non-graphical
        row_returns = self.ui.add_toggle(
            self.ui.right_column.menus.settings_vertical_layout,
            height=40,
            width=[100, 50, 100],
            label=["Graphical", "Non-graphical"],
            font_size=12,
        )

        self.ui.left_column.menus.non_graphical_select_row = row_returns[0]
        self.graphical_label = row_returns[1]
        self.graphical_mode = row_returns[2]
        self.non_graphical_label = row_returns[3]

        # Add line
        self.ui.add_vertical_line(
            self.ui.right_column.menus.settings_vertical_layout, top_spacer=[0, 10], bot_spacer=[0, 10]
        )

        # Browse row
        row_returns = self.ui.add_icon_button(
            self.ui.right_column.menus.settings_vertical_layout,
            icon=self.ui.images_load.icon_path("icon_folder_open.svg"),
            height=40,
            width=[40, 160],
            text="Browse...",
        )

        self.ui.right_column.menus.browse_file_group = row_returns[0]
        self.browse = row_returns[1]
        self.file = row_returns[2]

        self.browse.clicked.connect(lambda: self.browse_file())

        # Add line
        self.ui.add_vertical_line(
            self.ui.right_column.menus.settings_vertical_layout, top_spacer=[0, 10], bot_spacer=[0, 10]
        )

        # Launch AEDT
        row_returns = self.ui.add_n_buttons(
            self.ui.right_column.menus.settings_vertical_layout,
            num_buttons=1,
            height=40,
            width=[200],
            text=["Connect to AEDT"],
        )

        self.ui.right_column.menus.connect_aedt_layout = row_returns[0]
        self.connect_aedt = row_returns[1]

        # Disable launch AEDT
        self.connect_aedt.setEnabled(False)

        self.connect_aedt.clicked.connect(self.launch_aedt)

    def process_id(self):
        if self.signal_flag:
            self.aedt_session.clear()
            self.aedt_session.addItem("New Session")
            non_graphical_pos = self.graphical_mode.position
            non_graphical = non_graphical_pos == 24.0
            if self.aedt_version.currentText() and self.aedt_version.currentText() != "AEDT not installed":
                sessions = self.app.find_process_ids(self.aedt_version.currentText(), non_graphical)
                for pid in sessions:
                    if sessions[pid] == -1:
                        self.aedt_session.addItem("Process {}".format(pid))
                    else:
                        self.aedt_session.addItem("Grpc on port {}".format(sessions[pid]))

    def launch_aedt(self):
        selected_session = self.aedt_session.currentText()
        selected_version = self.aedt_version.currentText()
        non_graphical_pos = self.graphical_mode.position
        non_graphical = non_graphical_pos == 24.0

        self.aedt_thread = AedtLauncherThread(self.app, selected_version, selected_session, non_graphical)

        # Connect the AedtLauncher's finished signal to a slot
        self.aedt_thread.finished_signal.connect(self.handle_aedt_thread_finished)

        # Submit the AedtLauncher instance to the thread pool
        # QThreadPool.globalInstance().start(self.aedt_thread)

        self.aedt_thread.start()

        self.connect_aedt.setEnabled(False)
        self.aedt_version.setEnabled(False)
        self.aedt_session.setEnabled(False)

    def handle_aedt_thread_finished(self, aedt_launched):
        # This method will be called when the thread finishes
        if aedt_launched:
            file = self.file.text()
            if file:
                aedt_file = os.path.normpath(file)
                self.app.open_project(aedt_file)
            self.app.home_menu.update_project()
            self.app.home_menu.update_design()
            self.ui.update_logger("AEDT session connected")
        else:
            self.ui.update_logger("AEDT not launched")
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
