import time

from PySide6.QtCore import QThread
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QWidget
from examples.toolkit.pyaedt_toolkit.ui.windows.plot_design.plot_design_column import Ui_LeftColumn
from examples.toolkit.pyaedt_toolkit.ui.windows.plot_design.plot_design_page import Ui_Plot_Design

import tempfile
from pyvistaqt import BackgroundPlotter
import base64
import pyvista as pv
import os


class PlotDesignThread(QThread):
    finished_signal = Signal(bool)

    def __init__(self, app, selected_project, selected_design):
        super().__init__()
        self.plot_design_menu = app
        self.app = app.app
        self.selected_project = selected_project
        self.selected_design = selected_design
        self.model_info = None

    def run(self):

        self.model_info = self.app.get_aedt_model(
            self.selected_project, self.selected_design, air_objects=True
        )

        self.finished_signal.emit(self.model_info)


class PlotDesignMenu(object):
    def __init__(self, main_window):
        # General properties
        self.main_window = main_window
        self.ui = main_window.ui
        self.app = self.ui.app
        self.temp_folder = tempfile.mkdtemp()

        # Add page
        plot_design_menu_index = self.ui.add_page(Ui_Plot_Design)
        self.ui.load_pages.pages.setCurrentIndex(plot_design_menu_index)
        self.plot_design_menu_widget = self.ui.load_pages.pages.currentWidget()

        # Add left column
        new_column_widget = QWidget()
        new_ui = Ui_LeftColumn()
        new_ui.setupUi(new_column_widget)
        self.ui.left_column.menus.menus.addWidget(new_column_widget)
        self.plot_design_column_widget = new_column_widget
        self.plot_design_column_vertical_layout = new_ui.plot_design_vertical_layout

        # Specific properties
        self.plot_design_label = self.plot_design_menu_widget.findChild(QLabel, "plot_design_label")
        self.plot_design_grid = self.plot_design_menu_widget.findChild(QGridLayout, "plot_design_grid")

        self.plot_design_button_layout = None
        self.plot_design_button = None
        self.get_model_thread = None

    def setup(self):
        # Modify theme
        app_color = self.app.ui.themes["app_color"]
        text_color = app_color["text_active"]
        background = app_color["dark_three"]

        # Geometry label button
        plot_design_label_style = """
                                    QLabel {{
                                    color: {_color};
                                    font-size: {_font_size}pt;
                                    font-weight: bold;
                                    }}
                                    """
        custom_style = plot_design_label_style.format(
            _color=text_color, _bg_color=background, _font_size=self.app.properties.font["title_size"]
        )
        self.plot_design_label.setStyleSheet(custom_style)

        # Set column
        # Create geometry button
        row_returns = self.ui.add_n_buttons(
            self.plot_design_column_vertical_layout, num_buttons=1,
            height=40,
            width=[200],
            text=["Plot design"],
            font_size=self.app.properties.font["title_size"]
        )

        self.plot_design_button_layout = row_returns[0]
        self.plot_design_button = row_returns[1]
        self.plot_design_button_layout.addWidget(self.plot_design_button)
        self.plot_design_button.clicked.connect(self.plot_design_button_clicked)

        # Test 3D PLOT without backend
        # plotter = BackgroundPlotter(show=False)
        #
        # cad_mesh = pv.read(r"C:\AnsysDev\repos\pyaedt-toolkits-common\examples\ui\widget_example\Box1.obj")
        #
        # plotter.add_mesh(cad_mesh)
        #
        # plotter.view_isometric()
        # plotter.add_axes_at_origin(labels_off=True, line_width=5)
        # plotter.show_grid()
        # self.plot_design_grid.addWidget(plotter, 0, 0)

    def plot_design_button_clicked(self):

        if not self.app.check_connection():
            msg = "Backend not running."
            self.ui.update_logger(msg)
            return False

        if self.get_model_thread and self.get_model_thread.isRunning() or self.app.backend_busy():
            msg = "Toolkit running"
            self.ui.update_logger(msg)
            self.app.logger.debug(msg)
            return False

        be_properties = self.app.get_properties()

        if be_properties.get("active_project"):
            self.ui.update_progress(0)
            selected_project = self.app.home_menu.project_combobox.currentText()
            selected_design = self.app.home_menu.design_combobox.currentText()
            # Start a separate thread for the backend call
            self.get_model_thread = PlotDesignThread(
                app=self,
                selected_project=selected_project,
                selected_design=selected_design,
            )
            self.get_model_thread.finished_signal.connect(self.get_model_finished)

            msg = "Exporting model."
            self.ui.update_logger(msg)

            self.get_model_thread.start()

        else:
            self.ui.update_logger("Toolkit not connect to AEDT.")

    def get_model_finished(self):
        self.ui.update_progress(100)

        self.app.ui.clear_layout(self.plot_design_grid)

        if self.get_model_thread.model_info:
            model_info = self.get_model_thread.model_info

            plotter = BackgroundPlotter(show=False)

            for element in model_info:
                # Decode response
                encoded_data = model_info[element][0]
                encoded_data_bytes = bytes(encoded_data, "utf-8")
                decoded_data = base64.b64decode(encoded_data_bytes)
                # Create obj file locally
                file_path = os.path.join(self.temp_folder, element + ".obj")
                with open(file_path, "wb") as f:
                    f.write(decoded_data)
                # Create PyVista object
                if not os.path.exists(file_path):
                    break

                cad_mesh = pv.read(file_path)

                plotter.add_mesh(
                    cad_mesh, color=model_info[element][1], show_scalar_bar=False, opacity=model_info[element][2]
                )

            plotter.view_isometric()
            plotter.set_background(color=self.app.ui.themes["app_color"]["bg_one"])
            plotter.add_axes_at_origin(labels_off=True, line_width=5)
            plotter.show_grid(color=self.app.ui.themes["app_color"]["dark_two"])

            self.plot_design_grid.addWidget(plotter, 0, 0)

            msg = "Model exported."
            self.ui.update_logger(msg)
        else:
            msg = f"Failed backend call: {self.app.url}"
            self.ui.update_logger(msg)
