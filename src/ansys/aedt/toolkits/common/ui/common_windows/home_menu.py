from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QSpacerItem


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
        self.project_combobox.currentIndexChanged.connect(lambda: self.update_project_info())
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

    def update_project_info(self):
        active_project = self.main_window.home_menu.project_combobox.currentText()
        design_list = self.app.update_design_names(active_project)
        self.main_window.home_menu.design_combobox.clear()
        self.main_window.home_menu.design_combobox.addItems(design_list)
        pass
