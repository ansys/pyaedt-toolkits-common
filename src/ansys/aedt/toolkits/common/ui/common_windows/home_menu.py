from PySide6.QtWidgets import *
from ansys.aedt.toolkits.common.ui.utils.widgets import *


class HomeMenu(object):
    def __init__(self, main_window):
        self.ui = main_window

        # File Mode
        self.mode = "aedt_based"
        self.aedt_mode = None
        self.aedt_mode_label = None
        self.file_mode_label = None

        self.browse = None
        self.file = None

        self.project = None
        self.project_combobox = None

        self.design = None
        self.design_combobox = None

    def setup(self):
        # Mode
        row_returns = self.ui.add_toggle(
            self.ui.left_column.menus.home_vertical_layout,
            height=40,
            width=[100, 50, 100],
            label=["AEDT Mode", "File Mode"],
            font_size=12
        )

        self.ui.left_column.menus.file_mode_select_row = row_returns[0]

        self.aedt_mode_label = row_returns[1]

        self.aedt_mode = row_returns[2]

        self.file_mode_label = row_returns[3]

        self.aedt_mode.clicked.connect(lambda: self.mode_changed())

        # Add line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: {};".format(self.ui.themes["app_color"]["dark_two"]))
        self.ui.left_column.menus.home_vertical_layout.addWidget(line)
        spacer = QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.ui.left_column.menus.home_vertical_layout.addItem(spacer)

        # Browse row
        row_returns = self.ui.add_icon_button(self.ui.left_column.menus.home_vertical_layout,
                                              icon=self.ui.images_load.icon_path("icon_folder_open.svg"),
                                              height=40,
                                              width=[40, 160],
                                              text='Browse...')

        self.ui.left_column.menus.browse_file_group = row_returns[0]
        self.browse = row_returns[1]
        self.file = row_returns[2]

        self.browse.clicked.connect(lambda: self.browse_file())

        # Add line
        spacer = QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.ui.left_column.menus.home_vertical_layout.addItem(spacer)
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: {};".format(
            self.ui.themes["app_color"]["dark_two"]))
        self.ui.left_column.menus.home_vertical_layout.addWidget(line)
        spacer = QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.ui.left_column.menus.home_vertical_layout.addItem(spacer)

        # Project row
        row_returns = self.ui.add_combobox(self.ui.left_column.menus.home_vertical_layout,
                                           height=40,
                                           width=[100, 100],
                                           label="Project",
                                           combobox_list=["No Project"])

        self.ui.left_column.menus.browse_project_group = row_returns[0]
        self.project = row_returns[1]
        self.project_combobox = row_returns[2]

        # Design row
        row_returns = self.ui.add_combobox(self.ui.left_column.menus.home_vertical_layout,
                                           height=40,
                                           width=[100, 100],
                                           label="Design",
                                           combobox_list=["No Design"])

        self.ui.left_column.menus.browse_design_group = row_returns[0]
        self.design = row_returns[1]
        self.design_combobox = row_returns[2]

    def mode_changed(self):

        if self.mode == "file_based":
            self.mode = "aedt_based"
            self.project.setVisible(True)
            self.project_combobox.setVisible(True)
            self.design.setVisible(True)
            self.design_combobox.setVisible(True)
        else:
            self.mode = "file_based"
            self.project.setVisible(False)
            self.project_combobox.setVisible(False)
            self.design.setVisible(False)
            self.design_combobox.setVisible(False)
        self.ui.logger.log(f'Setting Mode to {self.mode}')

    def browse_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        if self.mode == "file_based":
            file, _ = QFileDialog.getOpenFileName(self.ui.app, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*)",
                                                  options=options)
        else:
            file, _ = QFileDialog.getOpenFileName(self.ui.app, "QFileDialog.getOpenFileName()", "",
                                                  "Ansys Electronics Desktop Project Files (*.aedt *.aedtz)",
                                                  options=options)
        if file != "":
            self.file.setText(file)
