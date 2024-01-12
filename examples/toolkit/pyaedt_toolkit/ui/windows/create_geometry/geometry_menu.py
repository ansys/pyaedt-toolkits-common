from PySide6.QtWidgets import *
from examples.toolkit.pyaedt_toolkit.ui.windows.create_geometry.geometry_page import Ui_Geometry


class GeometryMenu(object):
    def __init__(self, main_window):
        self.main_window = main_window
        self.ui = main_window.ui
        self.app = self.ui.app

        # Add page to the default ones
        geometry_menu_index = self.ui.add_page(Ui_Geometry)
        self.ui.load_pages.pages.setCurrentIndex(geometry_menu_index)
        self.geometry_menu_widget = self.ui.load_pages.pages.currentWidget()

        self.geometry_button = self.geometry_menu_widget.findChild(QPushButton, "create_geometry_button")
        self.geometry_button.clicked.connect(self.geometry_button_clicked)

        self.geometry_combo = self.geometry_menu_widget.findChild(QComboBox, "geometry_combo")
        self.multiplier = self.geometry_menu_widget.findChild(QLineEdit, "multiplier")
        self.select_geometry_label = self.geometry_menu_widget.findChild(QLabel, "select_geometry_label")
        self.multiplier_label = self.geometry_menu_widget.findChild(QLabel, "dimension_multiplier_label")

    def setup(self):
        # Modify theme
        app_color = self.app.ui.themes["app_color"]
        text_color = app_color["text_active"]
        background = app_color["dark_three"]
        border_color = app_color["dark_two"]

        # Combo box
        combo_box_style = '''
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
        '''
        custom_style = combo_box_style.format(_color=text_color,
                                              _bg_color=background,
                                              _font_size=self.app.general_settings.font["title_size"])
        self.geometry_combo.setStyleSheet(custom_style)

        # Multiplier line
        line_style = '''
            QLineEdit {{
            border: none;
            padding: 10px;
            color: {_color};
            background-color: {_bg_color};
            selection-background-color: red;
            font-size: {_font_size}pt;
            }}
        '''
        custom_style = line_style.format(_color=text_color,
                                         _bg_color=background,
                                         _font_size=self.app.general_settings.font["title_size"])
        self.multiplier.setStyleSheet(custom_style)

        # Create geometry button
        geometry_button_style = '''
            QPushButton {{
            border: 2px solid {_border_color};
            border-radius: 5px;
            padding: 10px;
            color: {_color};
            background-color: {_bg_color};
            selection-background-color: red;
            font-size: {_font_size}pt;
            box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.3);
            }}
            QPushButton:hover {{
            background-color: {_border_color};
            }}
            '''
        custom_style = geometry_button_style.format(_color=text_color,
                                                    _bg_color=background,
                                                    _font_size=self.app.general_settings.font["title_size"],
                                                    _border_color=border_color)
        self.geometry_button.setStyleSheet(custom_style)

        # Multiplier label button
        multiplier_label_style = '''
                    QLabel {{
                    color: {_color};
                    font-size: {_font_size}pt;
                    font-weight: bold;
                    }}
                    '''
        custom_style = multiplier_label_style.format(_color=text_color,
                                                     _bg_color=background,
                                                     _font_size=self.app.general_settings.font["title_size"])
        self.multiplier_label.setStyleSheet(custom_style)

        # Geometry label button
        select_geometry_label_style = '''
                            QLabel {{
                            color: {_color};
                            font-size: {_font_size}pt;
                            font-weight: bold;
                            }}
                            '''
        custom_style = select_geometry_label_style.format(_color=text_color,
                                                          _bg_color=background,
                                                          _font_size=self.app.general_settings.font["title_size"])
        self.select_geometry_label.setStyleSheet(custom_style)

    def geometry_button_clicked(self):
        if not self.app.check_connection():
            msg = "Backend not running."
            self.ui.logger.log(msg)
            return False

        if self.app.backend_busy():
            msg = "Toolkit running"
            self.ui.logger.log(msg)
            self.app.logger.debug(msg)
            return False

        if self.app.be_properties.active_project:
            selected_project = self.app.home_menu.project_combobox.currentText()
            selected_design = self.app.home_menu.design_combobox.currentText()
            multiplier = self.multiplier.text()
            geometry = self.geometry_combo.currentText()
            self.app.create_geometry_toolkit(selected_project, selected_design, geometry, multiplier)
            self.ui.logger.log("Geometry created.")
        else:
            self.ui.logger.log("Toolkit not connect to AEDT.")

