from PySide6.QtCore import QThread
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget
from examples.toolkit.pyaedt_toolkit.ui.windows.create_geometry.geometry_page import Ui_Geometry
from examples.toolkit.pyaedt_toolkit.ui.windows.create_geometry.geometry_column import Ui_LeftColumn

# toolkit PySide6 Widgets
from ansys.aedt.toolkits.common.ui.utils.widgets import PyLabel


class CreateGeometryThread(QThread):
    finished_signal = Signal(bool)

    def __init__(self, app, selected_project, selected_design, geometry, multiplier):
        super().__init__()
        self.geometry_menu = app
        self.app = app.app
        self.selected_project = selected_project
        self.selected_design = selected_design
        self.geometry = geometry
        self.multiplier = multiplier

    def run(self):
        self.app.ui.progress.progress = 50

        success = self.app.create_geometry_toolkit(
            self.selected_project, self.selected_design, self.geometry, self.multiplier
        )
        self.finished_signal.emit(success)


class GeometryMenu(object):
    def __init__(self, main_window):
        # General properties
        self.main_window = main_window
        self.ui = main_window.ui
        self.app = self.ui.app

        # Add page
        geometry_menu_index = self.ui.add_page(Ui_Geometry)
        self.ui.load_pages.pages.setCurrentIndex(geometry_menu_index)
        self.geometry_menu_widget = self.ui.load_pages.pages.currentWidget()

        # Add left column
        new_column_widget = QWidget()
        new_ui = Ui_LeftColumn()
        new_ui.setupUi(new_column_widget)
        self.ui.left_column.menus.menus.addWidget(new_column_widget)
        self.geometry_column_widget = new_column_widget
        self.geometry_column_vertical_layout = new_ui.geometry_vertical_layout

        # Specific properties
        self.geometry_combo = self.geometry_menu_widget.findChild(QComboBox, "geometry_combo")
        self.multiplier = self.geometry_menu_widget.findChild(QLineEdit, "multiplier")
        self.select_geometry_label = self.geometry_menu_widget.findChild(QLabel, "select_geometry_label")
        self.multiplier_label = self.geometry_menu_widget.findChild(QLabel, "dimension_multiplier_label")
        self.geometry_button_layout = None
        self.geometry_button = None
        self.geometry_thread = None

    def setup(self):
        # Modify theme
        app_color = self.app.ui.themes["app_color"]
        text_color = app_color["text_active"]
        background = app_color["dark_three"]

        # Common UI API
        geometry_button_layout = self.geometry_menu_widget.findChild(QVBoxLayout, "button_layout")

        # Create geometry button
        row_returns = self.ui.add_n_buttons(
            geometry_button_layout, num_buttons=1, height=100, width=[300], text=["Create Geometry"], font_size=20
        )

        self.geometry_button_layout = row_returns[0]
        self.geometry_button = row_returns[1]
        self.geometry_button_layout.addWidget(self.geometry_button)
        self.geometry_button.clicked.connect(self.geometry_button_clicked)

        # UI from Designer

        # Combo box
        combo_box_style = """
            QComboBox {{
                border: none;
                padding: 10px;
                color: {_color};
                background-color: {_bg_color};
                selection-background-color: red;
                font-size: {_font_size}pt;
            }}
            QComboBox QAbstractItemView {{
                border: none;
                background-color: {_bg_color};
                color: {_color};
            }}
        """
        custom_style = combo_box_style.format(
            _color=text_color, _bg_color=background, _font_size=self.app.properties.font["title_size"]
        )
        self.geometry_combo.setStyleSheet(custom_style)

        # Multiplier line
        line_style = """
            QLineEdit {{
            border: none;
            padding: 10px;
            color: {_color};
            background-color: {_bg_color};
            selection-background-color: red;
            font-size: {_font_size}pt;
            }}
        """
        custom_style = line_style.format(
            _color=text_color, _bg_color=background, _font_size=self.app.properties.font["title_size"]
        )
        self.multiplier.setStyleSheet(custom_style)

        # Multiplier label button
        multiplier_label_style = """
                    QLabel {{
                    color: {_color};
                    font-size: {_font_size}pt;
                    font-weight: bold;
                    }}
                    """
        custom_style = multiplier_label_style.format(
            _color=text_color, _bg_color=background, _font_size=self.app.properties.font["title_size"]
        )
        self.multiplier_label.setStyleSheet(custom_style)

        # Geometry label button
        select_geometry_label_style = """
                            QLabel {{
                            color: {_color};
                            font-size: {_font_size}pt;
                            font-weight: bold;
                            }}
                            """
        custom_style = select_geometry_label_style.format(
            _color=text_color, _bg_color=background, _font_size=self.app.properties.font["title_size"]
        )
        self.select_geometry_label.setStyleSheet(custom_style)

        # Set Column
        msg = "Press 'Create Geometry' button"
        label_widget = PyLabel(
            text=msg,
            font_size=self.ui.app.properties.font["title_size"],
            color=self.ui.themes["app_color"]["text_description"])
        self.geometry_column_vertical_layout.addWidget(label_widget)

    def geometry_button_clicked(self):
        if not self.app.check_connection():
            msg = "Backend not running."
            self.ui.logger.log(msg)
            return False

        if self.geometry_thread and self.geometry_thread.isRunning() or self.app.backend_busy():
            msg = "Toolkit running"
            self.ui.logger.log(msg)
            self.app.logger.debug(msg)
            return False

        be_properties = self.app.get_properties()

        if be_properties.get("active_project"):
            self.ui.progress.progress = 0
            selected_project = self.app.home_menu.project_combobox.currentText()
            selected_design = self.app.home_menu.design_combobox.currentText()
            multiplier = self.multiplier.text()
            geometry = self.geometry_combo.currentText()

            # Start a separate thread for the backend call
            self.geometry_thread = CreateGeometryThread(
                app=self,
                selected_project=selected_project,
                selected_design=selected_design,
                geometry=geometry,
                multiplier=multiplier,
            )
            self.geometry_thread.finished_signal.connect(self.geometry_created_finished)

            msg = "Creating geometry."
            self.ui.logger.log(msg)

            self.geometry_thread.start()

        else:
            self.ui.logger.log("Toolkit not connect to AEDT.")

    def geometry_created_finished(self, success):
        self.ui.progress.progress = 100

        if success:
            msg = "Geometry created."
            self.ui.logger.log(msg)
        else:
            msg = f"Failed backend call: {self.app.url}"
            self.ui.logger.log(msg)
