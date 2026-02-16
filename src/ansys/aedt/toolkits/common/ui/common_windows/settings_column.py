from PySide6.QtCore import QObject, QThread, QTimer
from PySide6.QtWidgets import *
import os


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

        self.check_status_timer = QTimer(self)
        self.check_status_timer.timeout.connect(self.check_status)
        self.check_status_timer.start(200)
        self.check_status_timer.stop()

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
            combobox_list=[])

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
            font_size=12
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
        row_returns = self.ui.add_icon_button(self.ui.right_column.menus.settings_vertical_layout,
                                              icon=self.ui.images_load.icon_path("icon_folder_open.svg"),
                                              height=40,
                                              width=[40, 160],
                                              text='Browse...')

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
            text=["Connect to AEDT"])

        self.ui.right_column.menus.connect_aedt_layout = row_returns[0]
        self.connect_aedt = row_returns[1]

        # Disable launch AEDT
        self.connect_aedt.setEnabled(False)

        self.connect_aedt.clicked.connect(self.launch_aedt)

    def process_id(self):
        if self.signal_flag:
            self.aedt_session.clear()
            self.aedt_session.addItem("New Session")
            if self.aedt_version.currentText() and self.aedt_version.currentText() != "AEDT not installed":
                sessions = self.app.find_process_ids(self.aedt_version.currentText())
                for session in sessions:
                    if session[1] == -1:
                        self.aedt_session.addItem("Process {}".format(session[0], session[1]))
                    else:
                        self.aedt_session.addItem("Process {} on Grpc {}".format(session[0], session[1]))

    def launch_aedt(self):
        selected_session = self.aedt_session.currentText()
        selected_version = self.aedt_version.currentText()
        non_graphical_pos = self.graphical_mode.position
        non_graphical = non_graphical_pos == 24.0

        self.check_status_timer.stop()

        self.aedt_thread = QThread()

        self.aedt_thread.started.connect(lambda: self.app.launch_aedt(selected_version,
                                                                      selected_session,
                                                                      non_graphical))

        self.check_status_timer.start()

        # Start the new thread
        self.aedt_thread.start()

        self.connect_aedt.setEnabled(False)
        self.aedt_version.setEnabled(False)
        self.aedt_session.setEnabled(False)

    def update_project(self):
        project_list = self.app.get_aedt_data()
        self.main_window.home_menu.project_combobox.setEnabled(True)
        self.main_window.home_menu.project_combobox.clear()
        self.main_window.home_menu.project_combobox.addItems(project_list)

    def update_design(self):
        design_list = self.app.update_design_names()
        self.main_window.home_menu.design_combobox.clear()
        self.main_window.home_menu.design_combobox.addItems(design_list)

    def check_status(self):
        backend_busy = self.app.backend_busy()
        if not backend_busy and self.aedt_thread:
            self.aedt_thread.terminate()
            self.aedt_thread = None
            self.check_status_timer.stop()
            file = self.file.text()
            if file:
                aedt_file = os.path.normpath(file)
                self.app.open_project(aedt_file)
            self.update_project()
            self.update_design()
            self.ui.progress.progress = 100
            self.ui.logger.log("AEDT session connected")

    def browse_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        file, _ = QFileDialog.getOpenFileName(self.ui.app, "QFileDialog.getOpenFileName()", "",
                                              "Ansys Electronics Desktop Project Files (*.aedt *.aedtz)",
                                              options=options)
        if file != "":
            self.file.setText(file)
