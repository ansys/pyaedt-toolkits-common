class SettingsMenu(object):
    def __init__(self, main_window):
        self.ui = main_window
        self.app = self.ui.app

        self.aedt_version_label = None
        self.aedt_version = None

        self.aedt_session_label = None
        self.aedt_session = None

        self.connect_aedt = None

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

        # Launch AEDT

        row_returns = self.ui.add_n_buttons(
            self.ui.right_column.menus.settings_vertical_layout,
            num_buttons=1,
            height=40,
            width=[200],
            text=["Connect to AEDT"])

        self.ui.right_column.menus.connect_aedt_layout = row_returns[0]
        self.connect_aedt = row_returns[1]

        self.connect_aedt.clicked.connect(lambda: self.app.launch_aedt())

