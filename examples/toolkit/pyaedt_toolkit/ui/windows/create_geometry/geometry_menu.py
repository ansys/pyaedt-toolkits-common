from PySide6.QtWidgets import *
from examples.toolkit.pyaedt_toolkit.ui.windows.create_geometry.geometry_page import Ui_Geometry


class GeometryMenu(object):
    def __init__(self, main_window):
        self.main_window = main_window
        self.ui = main_window.ui
        self.app = self.ui.app

        geometry_menu_index = self.ui.add_page(Ui_Geometry)
        self.ui.load_pages.pages.setCurrentIndex(geometry_menu_index)
        self.geometry_menu_widget = self.ui.load_pages.pages.currentWidget()

    def setup(self):
        # Modify theme
        app_color = self.app.ui.themes["app_color"]
        text_color = app_color["text_active"]
        background = app_color["dark_three"]
        # text_size

        # Combo box
        geometry_combo = self.geometry_menu_widget.findChild(QComboBox, "geometry_combo")
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
        geometry_combo.setStyleSheet(custom_style)

        # Multiplier line
        multiplier = self.geometry_menu_widget.findChild(QLineEdit, "multiplier")
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
        multiplier.setStyleSheet(custom_style)

        # Create geometry button
        geometry_button = self.geometry_menu_widget.findChild(QPushButton, "create_geometry_button")
        geometry_button_style = '''
            QPushButton {{
            border: none;
            padding: 10px;
            color: {_color};
            background-color: {_bg_color};
            selection-background-color: red;
            font-size: {_font_size}pt;
            }}
            '''
        custom_style = geometry_button_style.format(_color=text_color,
                                                    _bg_color=background,
                                                    _font_size=self.app.general_settings.font["title_size"])
        geometry_button.setStyleSheet(custom_style)

        # Multiplier label button
        multiplier_label = self.geometry_menu_widget.findChild(QLabel, "dimension_multiplier_label")
        multiplier_label_style = '''
                    QLabel {{
                    font-size: {_font_size}pt;
                    font-weight: bold;
                    }}
                    '''
        custom_style = multiplier_label_style.format(_color=text_color,
                                                     _bg_color=background,
                                                     _font_size=self.app.general_settings.font["title_size"])
        multiplier_label.setStyleSheet(custom_style)

        # Geometry label button
        select_geometry_label = self.geometry_menu_widget.findChild(QLabel, "select_geometry_label")
        select_geometry_label_style = '''
                            QLabel {{
                            font-size: {_font_size}pt;
                            font-weight: bold;
                            }}
                            '''
        custom_style = select_geometry_label_style.format(_color=text_color,
                                                          _bg_color=background,
                                                          _font_size=self.app.general_settings.font["title_size"])
        select_geometry_label.setStyleSheet(custom_style)

        return True
