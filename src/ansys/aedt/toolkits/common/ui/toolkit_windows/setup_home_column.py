from PySide6.QtWidgets import *
from ansys.aedt.toolkits.common.ui.utils.widgets import *


class SetupHomeMenu(object):
    def __init__(self, main_window):
        self.ui = main_window

        # File Mode
        self.mode = "file_based"
        self.left_btn_mode = None
        self.aedt_mode_label = None
        self.file_mode_label = None

    def setup(self):
        row_returns = self.ui.add_toggle(
            self.ui.left_column.menus.home_vertical_layout,
            height=40,
            width=[100, 50, 100],
            label=["AEDT Mode", "File Mode"],
            font_size=12
        )

        self.ui.left_column.menus.file_mode_select_row = row_returns[0]

        self.file_mode_label = row_returns[1]

        self.left_btn_mode = row_returns[2]

        self.aedt_mode_label = row_returns[3]

        self.left_btn_mode.clicked.connect(lambda: self.mode_changed())

        # Row 2
        row_returns = self.ui.add_icon_button(self.ui.left_column.menus.home_vertical_layout,
                                              icon=self.ui.images_load.icon_path("icon_folder_open.svg"),
                                              height=40,
                                              width=[40, 160],
                                              text='Browse...')

        self.ui.left_column.menus.browse_file_group = row_returns[0]
        self.left_btn_browse = row_returns[1]
        self.file_line_edit = row_returns[2]

        self.left_btn_browse.clicked.connect(lambda: self.browse_file())

        # Project Row
        # row_returns = self.add_rows.add_label_combobox(self.ui.left_column.menus.home_vertical_layout,
        #                                          height=40,
        #                                          width=[100, 100],
        #                                          label="Project",
        #                                          combobox_list=["No Project"])
        #
        # self.ui.left_column.menus.browse_project_group = row_returns[0]
        # self.project_label = row_returns[1]
        # self.project_combobox = row_returns[2]
        #
        # # Design
        # row_returns = self.add_rows.add_label_combobox(
        #                                          self.ui.left_column.menus.home_vertical_layout,
        #                                          height=40,
        #                                          width=[100, 100],
        #                                          label="Design",
        #                                          combobox_list=["No Design"])
        #
        # self.ui.left_column.menus.browse_design_group = row_returns[0]
        # self.design_label = row_returns[1]
        # self.design_combobox = row_returns[2]
        #
        # self.ui.left_column.menus.browse_design_group = QHBoxLayout()
        #
        # # Load Row
        # self.add_rows.add_horizontal_spacer(self.ui.left_column.menus.menu_home,
        #                               self.ui.left_column.menus.home_vertical_layout)
        #
        # row_returns = self.add_rows.add_n_buttons(layout=self.ui.left_column.menus.home_vertical_layout,
        #                                     num_buttons=1,
        #                                     height=40,
        #                                     width=[200],
        #                                     text=['Load Model'])
        #
        # self.ui.left_column.menus.load_row = row_returns[0]
        # self.left_btn_load = row_returns[1]

        # self.left_btn_load.clicked.connect(lambda: self.load_model())

        # set intial state of GUI
        # self.left_btn_browse.setVisible(True)
        # self.file_line_edit.setVisible(True)
        # self.project_label.setVisible(False)
        # self.project_combobox.setVisible(False)
        # self.design_label.setVisible(False)
        # self.design_combobox.setVisible(False)

    def mode_changed(self):

        if self.mode == "file_based":
            self.mode = "aedt_based"
            print(f'Setting Mode to {self.mode}')
            # self.ui.left_column.menus.browse_file_layout2.setVisible(False)
            self.left_btn_browse.setVisible(False)
            self.file_line_edit.setVisible(False)
            # self.aedt_ver_label.setVisible(True)
            # self.aedt_ver_combobox.setVisible(True)
            # self.aedt_sess_label.setVisible(True)
            # self.aedt_sess_combobox.setVisible(True)
            # self.left_btn_connect_aedt.setVisible(True)
            self.project_label.setVisible(True)
            self.project_combobox.setVisible(True)
            self.design_label.setVisible(True)
            self.design_combobox.setVisible(True)
            # self.ui.left_column.menus.browse_aedt_sess_group.setVisible(True)
            # self.ui.left_column.menus.browse_design_group.setVisible(True)
            # self.ui.left_column.menus.browse_project_group.setVisible(True)
        else:
            self.mode = "file_based"
            print(f'Setting Mode to {self.mode}')
            self.left_btn_browse.setVisible(True)
            self.file_line_edit.setVisible(True)
            # self.aedt_ver_label.setVisible(True)
            # self.aedt_ver_combobox.setVisible(False)
            # self.aedt_sess_label.setVisible(False)
            # self.aedt_sess_combobox.setVisible(False)
            # self.left_btn_connect_aedt.setVisible(False)
            self.project_label.setVisible(False)
            self.project_combobox.setVisible(False)
            self.design_label.setVisible(False)
            self.design_combobox.setVisible(False)
            # self.ui.left_column.menus.browse_file_layout2.setVisible(True)
            # self.ui.left_column.menus.browse_file_group.setVisible(True)
            # self.ui.left_column.menus.browse_aedt_sess_group.setVisible(False)
            # self.ui.left_column.menus.browse_design_group.setVisible(False)
            # self.ui.left_column.menus.browse_project_group.setVisible(False)

    def browse_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.cad_file_path, _ = QFileDialog.getOpenFileName(self.ui, "QFileDialog.getOpenFileName()", "",
                                                            "STL Files (*.stl);;OBJ Files (*.obj);;All Files (*)",
                                                            options=options)
        if self.cad_file_path == "":
            self.cad_file_path = None
        # self.ui.codebook_text.setText(fileName)
        if self.mode == "file_based":
            self.file_line_edit.setText(self.cad_file_path)
